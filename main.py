import os
import tarfile
import subprocess
import shutil
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, Path, Query, Body, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "3a420781b6e8b5d7407588cb82aa642f02679988c3e1f4ad95102ac7aab596bb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Env variables
DEBUG = False

# Metadata will show up as descriptions along with each tag
tags_metadata = [
    {
        "name": "docs",
        "description": "Links to generated documentations.",
    },
    {
        "name": "submit",
        "description": 'Comes in two _flavors_. Submits code as: **string or tarfiles**',
    },
    {
        "name": "cluster",
        "description": 'Comes in two _flavors_. Clusters specific **files or all files in a folder**',
    },
    {
        "name": "delete",
        "description": 'Comes in two _flavors_. Deletes **submission folder** or a **file**',
    },
    {
        "name": "feedback",
        "description": 'Give feedback on codes passed as a **string**',
    },
    {
        "name": "index",
        "description": 'Comes in two _flavors_. Gets submission folders or all the files in a given submission folder',
    },
    {
        "name": "login",
        "description": 'Key in details for authorization',
    },
    {
        "name": "user",
        "description": 'gets user information',
    },
]

# context to manage pasaword like verifying and generating etc.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake DB that stores temporary username and password
fake_users_db = {
    "chester": {
        "username": "chester",
        "full_name": "Chester Koh Boon Hong",
        "email": "chester_koh@mymail.sutd.edu.sg",
        "hashed_password": "$2b$12$t5u4t2HgemA21uhsRrk24.0MoXZSq2lYZJu/5GQpqLx42IT7NRQJm",  # pass: secret
        "disabled": True,
    },
    "poskitt": {
        "username": "poskitt",
        "full_name": "Christopher Michael POSKITT",
        "email": " cposkitt@smu.edu.sg",
        "hashed_password": '$2b$12$Yr8U8/aSsLvTHAkkYQHTYe9ZrmcCG39X6/VC/oEcS9MaHwfRbUpuu',  # pass: securepassword
        "disabled": False,
    },
    "oka": {
        "username": "oka",
        "full_name": "Oka Kurniawan",
        "email": " oka_kurniawan@sutd.edu.sg",
        "hashed_password": '$2b$12$nVQ3ghFwkedWA.m548shW.pSh0S4XMoeZV1tBBit7wcdEvv/zEAyS',  # pass: firewall
        "disabled": False,
    },
    "cyrille": {
        "username": "cyrille",
        "full_name": "Cyrille Pierre Joseph Jegourel",
        "email": " cyrille_jegourel@sutd.edu.sg",
        "hashed_password": '$2b$12$PPlvfQ4YMT8spVfeSnJQ7.jVTvcEc30zt3mKmNpAeKFy5xuQbOx5K',  # pass: pyramid
        "disabled": False,
    },
    "norman": {
        "username": "norman",
        "full_name": "Norman Lee Tiong Seng",
        "email": " norman_lee@sutd.edu.sg",
        "hashed_password": '$2b$12$aEf7Ak/UVMmhIYjjZAAL7.eV8mHYLzMIx9G.dEJgdNBFBYiFQ0HRe',  # pass: megashield
        "disabled": False,
    },
    "nachamma": {
        "username": "nachamma",
        "full_name": "Nachamma Sockalingam",
        "email": " nachamma@sutd.edu.sg",
        "hashed_password": '$2b$12$t3z6Cf2A0z3RCNkdbfFOSuIMTgQHeNK30lEV48nnlkFjSKlvVrHtK',  # pass: secretpass
        "disabled": False,
    },
    "charles": {
        "username": "charles",
        "full_name": "Lim Thian Yew",
        "email": " thianyew_lim@mymail.sutd.edu.sg",
        "hashed_password": '$2b$12$ZLChEImf1DvyKloy1IcPxOaKpKmKgqwrBJaEJpMU9mm6yOXvz2c02',  # pass: xmen
        "disabled": False,
    },
    "ismam": {
        "username": "ismam",
        "full_name": "Ismam Al Hoque",
        "email": " ismam_hoque@sutd.edu.sg",
        "hashed_password": '$2b$12$OYfF6f0z/P5ebNhO6OyQS.V0FFgzPAaXQAWeevA3X1Zwwq8sc3.9q',  # pass: barelypass
        "disabled": False,
    },
}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# app = FastAPI()
app = FastAPI(root_path='/clara',
              title="Clara API Server",
              description="An API for connecting with a  server which executes Clara",
              openapi_tags=tags_metadata)


# Data models

# Data models for auth
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


# Data models for api
class SubmissionFolder(BaseModel):
    submission_folder: str = Field(..., description="path to correct submissions", example="sub_code/year/category/Qn")


class FullPath(SubmissionFolder):
    sid: str = Field(..., description="The student ID", example="1000749")


class Submission(FullPath):
    code: str = Field(..., description="The code to be submitted", example="print('hello clara!')")


class MetadataBase(SubmissionFolder):
    entryfnc: str = Field(..., description="The name of the entry function", example="computeDeriv")
    args: str = Field(..., description="The argument parameters without spaces", example="[[[4.5]],[[1.0,3.0,5.5]]]")


class ClusterMetadata(MetadataBase):
    filenames: List[str] = Field(..., description="The files to be clustered", example='["c1.py","c2.py"]')


class FeedbackModel(MetadataBase):
    # feedtype: Optional[str] = Field('python', description="python, simple or repair", example='python')
    # ext: Optional[str] = Field('.py', description="File extenstions: .java, .py or .c", example='.py')
    code: str = Field(..., description="The incorrect code for feedback", example='print("hello clara!")')


# utils

# Utils for auth
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# can be used to generate hash, not used directly in the project
def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# makes directory for submission and saves the solution
def save_file(path, name, sol):
    os.makedirs(path, exist_ok=True)
    _, ext = os.path.splitext(name)
    if ext == '':
        with open(path + '/' + name + '.py', 'w') as writer:
            writer.write(sol)
    else:
        with open(path + '/' + name, 'w') as writer:
            writer.write(sol)


# make a index.txt file to save all the submission folders
def make_index(path):
    _, truncated = path.split(os.getcwd() + '/submissions/')
    if os.path.isfile('index.txt'):
        with open('index.txt', 'r') as reader:
            if truncated + '\n' in reader.readlines():
                return
    with open('index.txt', 'a') as writer:
        writer.write(truncated + '\n')


# makes cluster directory, executes clara cluster command and returns the result success or otherwise
def cluster(cluster_path, path, entryfnc, args):
    os.makedirs(cluster_path, exist_ok=True)
    command = f'clara cluster {path} --clusterdir {cluster_path} --entryfnc {entryfnc} --args {args} ' \
              f'--ignoreio 1'.split()
    out = subprocess.run(command, capture_output=True)
    if out.stdout == b'':
        if DEBUG:
            return out.stderr.decode()
        else:
            return 'cluster command failed'
    else:
        return out.stdout.decode()


@app.get("/", tags=["docs"])
def swagger_doc():
    return RedirectResponse('./docs')


# Another documentation Clara API
@app.get("/redocs", tags=["docs"])
def redoc():
    return RedirectResponse('./redoc')


# Path for login and get token
@app.post("/login", response_model=Token, tags=["login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User, tags=["user"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post('/submit_snippet/', tags=["submit"], status_code=201)
def submit_snippet(submission: Submission, current_user: User = Depends(get_current_active_user)):
    sol = submission.code
    path = os.getcwd() + '/submissions/' + submission.submission_folder
    save_file(path, submission.sid, sol)
    make_index(path)
    return f'Submission of {submission.sid}.py is successful'


# make submission folder, read and decode the file and submit it
@app.post("/submit_compressed_file/", tags=["submit"], status_code=201)
async def submit_compressed_file(submission_folder: str = Query(..., description="submission folder path",
                                                                example="sub_code/year/category/Qn"),
                                 file: UploadFile = File(..., description="The file to be submitted"),
                                 current_user: User = Depends(get_current_active_user)):
    path = os.getcwd() + '/submissions/' + submission_folder
    os.makedirs('compressed_files', exist_ok=True)
    with open('compressed_files/' + file.filename, 'wb') as writer:
        writer.write(await file.read())
    with tarfile.open('compressed_files/' + file.filename) as tar:
        tar.extractall(path)
    os.remove('compressed_files/' + file.filename)
    make_index(path)
    return f'{file.filename} submitted successfully at {submission_folder}'


# define cluster folder, and get filenames for clustering  and pass to clara function
@app.put('/cluster_files', tags=["cluster"], status_code=202)
def cluster_files(cluster_metadata: ClusterMetadata, current_user: User = Depends(get_current_active_user)):
    cluster_path = os.getcwd() + '/clusters/' + cluster_metadata.submission_folder
    folder_path = os.getcwd() + f"/submissions/{cluster_metadata.submission_folder}/"
    if not os.path.exists(folder_path):
        return f"{cluster_metadata.submission_folder} does not exit"
    path = ""
    for filename in cluster_metadata.filenames:
        path += os.getcwd() + f"/submissions/{cluster_metadata.submission_folder}/" + filename + " "
    return cluster(cluster_path, path, cluster_metadata.entryfnc, cluster_metadata.args)


# define cluster folder, and get all filenames from the selected folder and pass to clara function
@app.put('/cluster_folder', tags=["cluster"], status_code=202)
def cluster_folder(cluster_metadata: MetadataBase, current_user: User = Depends(get_current_active_user)):
    cluster_path = os.getcwd() + '/clusters/' + cluster_metadata.submission_folder
    folder_path = os.getcwd() + f"/submissions/{cluster_metadata.submission_folder}/"
    path = ""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            path += folder_path + filename + " "
    else:
        return f"{cluster_metadata.submission_folder} does not exit"
    return cluster(cluster_path, path, cluster_metadata.entryfnc, cluster_metadata.args)


# generates path to cluster folder from submission path, gets all the file_path form the selected folder and pass to the
# clara function along with the incorrect file generated from the code snippet
@app.put('/feedback_snippet/', tags=["feedback"])
def feedback_snippet(feedback_metadata: FeedbackModel, current_user: User = Depends(get_current_active_user)):
# def feedback_snippet(feedback_metadata: FeedbackModel):
    cluster_path = os.getcwd() + '/clusters' + f"/{feedback_metadata.submission_folder}/"
    path = ""
    if not os.path.exists(cluster_path):
        return f'{feedback_metadata.submission_folder} does not exist'
    # for filename in [f for f in os.listdir(cluster_path) if f'{feedback_metadata.ext}' in f]:
    for filename in [f for f in os.listdir(cluster_path) if os.path.splitext(f)[1] == '.py']:
        path += cluster_path + filename + " "
    # with open(f'incorrect/incorrect{feedback_metadata.ext}', 'w') as writer:
    with open(f'incorrect/incorrect.py', 'w') as writer:
        writer.write(feedback_metadata.code)
    command = f'clara feedback {path} incorrect/incorrect.py --entryfnc {feedback_metadata.entryfnc}' \
              f' --args {feedback_metadata.args} --ignoreio 1 --feedtype python '.split()
    # f' --args {feedback_metadata.args} --ignoreio 1 --feedtype {feedback_metadata.feedtype} '.split()
    out = subprocess.run(command, capture_output=True)
    if out.stdout == b'':
        if DEBUG:
            return out.stderr.decode()
        else:
            return 'feedback command failed'
    else:
        return out.stdout.decode()


# gets all the submission folders
@app.get('/get_submission_folders/', tags=["index"])
def get_index(current_user: User = Depends(get_current_active_user)):
    if os.path.isfile('index.txt'):
        with open('index.txt', 'r') as reader:
            return [s[:-1] for s in reader.readlines()]
    return 'no submissions exist'


# gets all the files under a submission folder
@app.get('/get_submitted_file_names/', tags=["index"])
def get_submitted_file_names(folder: SubmissionFolder,
                             current_user: User = Depends(get_current_active_user)):
    complete_path = os.getcwd() + '/submissions/' + folder.submission_folder
    if os.path.exists(complete_path):
        return os.listdir(complete_path)
    return 'path does not exist'


# deletes a submission_folder and all its contents
@app.post('/delete_submission_folder/', tags=["delete"])
def delete_submission_folder(folder: SubmissionFolder,
                             current_user: User = Depends(get_current_active_user)):
    if os.path.isfile('index.txt'):
        with open('index.txt', 'r') as reader:
            arr = [s[:-1] for s in reader.readlines() if folder.submission_folder != s[:-1]]
        s = ''.join(arr)
        with open('index.txt', 'w') as writer:
            writer.write(s)
        complete_path = os.getcwd() + '/submissions/' + folder.submission_folder
        if os.path.exists(complete_path):
            shutil.rmtree(complete_path)
            return f'{folder.submission_folder} is deleted'
    return f'{folder.submission_folder} is not found'


# deletes a solution_file under a submission_folder
@app.post('/delete_submission_file/', tags=["delete"])
def delete_submission_file(path: FullPath,
                           current_user: User = Depends(get_current_active_user)):
    solution_file = path.sid + '.py'
    complete_path = os.getcwd() + '/submissions/' + path.submission_folder
    if os.path.exists(complete_path):
        if solution_file in os.listdir(complete_path):
            os.remove(complete_path + '/' + solution_file)
            return f'{solution_file} is removed'
        return f'{solution_file} does not exist'
    return f'{path.submission_folder} does not exist'

# No need to implement this feature
# @app.put('/feedback_file', tags=["feedback"])
# async def feedback_file(submission_folder: str = Query(..., description="path to correct submissions",
#                                                        example="sub_code/year/category/Qn"),
#                         entryfnc: str = Query(..., description="The name of the entry function",
#                                               example="computeDeriv"),
#                         args: str = Query(..., description="The argument parameters without spaces",
#                                           example="[[[4.5]],[[1.0,3.0,5.5]]]"),
#                         feedtype: Optional[str] = Query('python', description="python, simple or repair",
#                                                         example='python'),
#                         file: UploadFile = File(..., description="The incorrect file for feedback"),
#                         ext: Optional[str] = Query('.py', description="File extenstions: .java, .py or .c",
#                                                    example='.py')):
#     cluster_path = os.getcwd() + '/clusters' + f"/{submission_folder}/"
#     path = ""
#     if not os.path.exists(cluster_path):
#         return f'{submission_folder} does not exist'
#     for filename in [f for f in os.listdir(cluster_path) if f'{ext}' in f]:
#         path += cluster_path + filename + " "
#     os.makedirs('incorrect', exist_ok=True)
#     with open(f'incorrect/{file.filename}', 'wb') as writer:
#         writer.write(await file.read())
#     command = f'clara feedback {path} incorrect/{file.filename} --entryfnc {entryfnc} --args {args}' \
#               f' --ignoreio 1 --feedtype ' f'{feedtype} '.split()
#     out = subprocess.run(command, capture_output=True)
#     if out.stdout == b'':
#         return out.stderr.decode()
#     else:
#         return out.stdout.decode()


# # make submission folder, read and decode files and submit them
# @app.post("/submit_files/", tags=["submit"], status_code=201)
# async def submit_files(submission_folder: str = Query(..., description="submission folder path",
#                                                       example="sub_code/year/category/Qn"),
#                        files: List[UploadFile] = File(..., description="The list of files submitted")):
#     path = os.getcwd() + '/' + submission_folder
#     for file in files:
#         save_file(path, file.filename, (await file.read()).decode())
#     return [f'{file.filename} submitted successfully at {submission_folder}' for file in files]
