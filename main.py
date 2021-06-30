import codecs
import os
import subprocess
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, Path, Query, Body, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

tags_metadata = [
    {
        "name": "docs",
        "description": "Links to generated documentations.",
    },
    {
        "name": "submit",
        "description": 'Comes in three _flavors_. Submits code as: **string,file or files**',
    },
    {
        "name": "cluster",
        "description": 'Comes in two _flavors_. Clusters specific **files or all files in a folder**',
    },
    {
        "name": "feedback",
        "description": 'Comes in two _flavors_. Give feedback on codes passed as **strings** or as a **file**',
    },
]

# # to get a string like this run:
# # openssl rand -hex 32
# SECRET_KEY = "3a420781b6e8b5d7407588cb82aa642f02679988c3e1f4ad95102ac7aab596bb"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#
# fake_users_db = {
#     "chester": {
#         "username": "chester",
#         "full_name": "Chester Koh Boon Hong",
#         "email": "chester_koh@mymail.sutd.edu.sg",
#         # "hashed_password": "$2b$12$t5u4t2HgemA21uhsRrk24.0MoXZSq2lYZJu/5GQpqLx42IT7NRQJm",  # pass: secret
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "poskitt",
#         "full_name": "Christopher Michael POSKITT",
#         "email": " cposkitt@smu.edu.sg",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     username: Optional[str] = None
#
#
# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# app = FastAPI()
app = FastAPI(root_path='/clara',
              title="Clara API Server",
              description="An API for connecting with a  server which executes Clara",
              openapi_tags=tags_metadata)


# def fake_hash_password(password: str):
#     return "fakehashed" + password
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#

class Submission(BaseModel):
    submission_folder: str = Field(..., description="submission folder path", example="sub_code/year/category/Qn")
    code: str = Field(..., description="The code to be submitted", example="print('hello clara!')")
    sid: str = Field(..., description="The student ID", example="1000749")


class ClusterMetadataBase(BaseModel):
    submission_folder: str = Field(..., description="submission folder path to choose files from",
                                   example="sub_code/year/category/Qn")
    entryfnc: str = Field(..., description="The name of the entry function", example="computeDeriv")
    args: str = Field(..., description="The argument parameters without spaces", example="[[[4.5]],[[1.0,3.0,5.5]]]")


class ClusterMetadata(BaseModel):
    submission_folder: str = Field(..., description="submission folder path to choose files from",
                                   example="sub_code/year/category/Qn")
    entryfnc: str = Field(..., description="The name of the entry function", example="computeDeriv")
    args: str = Field(..., description="The argument parameters without spaces", example="[[[4.5]],[[1.0,3.0,5.5]]]")
    filenames: List[str] = Field(..., description="The files to be clustered", example='["c1.py","c2.py"]')


# utils
def save_file(path, name, sol):
    os.makedirs(path, exist_ok=True)
    _, ext = os.path.splitext(name)
    if ext == '':
        with open(path + '/' + name + '.py', 'w') as writer:
            writer.write(sol)
    else:
        with open(path + '/' + name, 'w') as writer:
            writer.write(sol)


def cluster(cluster_path, path, entryfnc, args):
    os.makedirs(cluster_path, exist_ok=True)
    command = f'clara cluster {path} --clusterdir {cluster_path} --entryfnc {entryfnc} --args {args} ' \
              f'--ignoreio 1'.split()
    out = subprocess.run(command, capture_output=True)
    if out.stdout == b'':
        return out.stderr.decode()
    else:
        return out.stdout.decode()


@app.get("/", tags=["docs"])
async def swagger_doc():
    print('jere')
    return RedirectResponse('./docs')
    #  return 'hello'


@app.get("/redocs", tags=["docs"])
async def reDoc():
    'Another documentation Clara API'
    return RedirectResponse('./redoc')
    #  return 'hello'


# @app.post("/token", tags=["authenticate"])
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}
#
#
# @app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


@app.post('/submit_snippet/', tags=["submit"], status_code=201)
def submit_snippet(submission: Submission):
    sol = submission.code
    path = os.getcwd() + '/' + submission.submission_folder
    save_file(path, submission.sid, sol)
    print(path)
    return f'Submission of {submission.sid}.py is successful'


@app.post("/submit_file/", tags=["submit"], status_code=201)
async def submit_file(submission_folder: str = Query(..., description="submission folder path",
                                                     example="sub_code/year/category/Qn"),
                      file: UploadFile = File(..., description="The file to be submitted")):
    path = os.getcwd() + '/' + submission_folder
    save_file(path, file.filename, (await file.read()).decode())
    return f'{file.filename} submitted successfully at {submission_folder}'


@app.post("/submit_files/", tags=["submit"], status_code=201)
async def submit_files(submission_folder: str = Query(..., description="submission folder path",
                                                      example="sub_code/year/category/Qn"),
                       files: List[UploadFile] = File(..., description="The list of files submitted")):
    path = os.getcwd() + '/' + submission_folder
    for file in files:
        save_file(path, file.filename, (await file.read()).decode())
    return [f'{file.filename} submitted successfully at {submission_folder}' for file in files]


@app.put('/cluster_files', tags=["cluster"], status_code=202)
async def cluster_files(cluster_metadata: ClusterMetadata):
    cluster_path = os.getcwd() + '/clusters/' + cluster_metadata.submission_folder
    folder_path = os.getcwd() + f"/{cluster_metadata.submission_folder}/"
    if not os.path.exists(folder_path):
        return f"{cluster_metadata.submission_folder} does not exit"
    path = ""
    for filename in cluster_metadata.filenames:
        path += os.getcwd() + f"/{cluster_metadata.submission_folder}/" + filename + " "
    return cluster(cluster_path, path, cluster_metadata.entryfnc, cluster_metadata.args)


@app.put('/cluster_folder', tags=["cluster"], status_code=202)
async def cluster_folder(cluster_metadata: ClusterMetadataBase):
    cluster_path = os.getcwd() + '/clusters/' + cluster_metadata.submission_folder
    folder_path = os.getcwd() + f"/{cluster_metadata.submission_folder}/"
    path = ""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            path += folder_path + filename + " "
    else:
        return f"{cluster_metadata.submission_folder} does not exit"
    return cluster(cluster_path, path, cluster_metadata.entryfnc, cluster_metadata.args)


@app.put('/feedback/{file_path:path}', tags=["feedback"])
async def feedback(file_path: str = Path(..., description="/sub_code/year/category/Qn", ),
                   entryfnc: str = Query(..., description="The name of the entry function"),
                   args: str = Query(..., description="The argument parameters without spaces"),
                   feedtype: Optional[str] = Query('python', description="python, simple or repair"),
                   file: UploadFile = File(..., description="The incorrect file for feedback"),
                   ext: Optional[str] = Query('.py', description="File extenstions: .java, .py or .c")):
    cluster_path = os.getcwd() + '/clusters' + f"{file_path}/"
    path = ""
    for filename in [f for f in os.listdir(cluster_path) if f'{ext}' in f]:
        path += cluster_path + filename + " "
    os.makedirs('incorrect', exist_ok=True)
    with open(f'incorrect/{file.filename}', 'wb') as writer:
        writer.write(await file.read())
    command = f'clara feedback {path} incorrect/{file.filename} --entryfnc {entryfnc} --args {args}' \
              f' --ignoreio 1 --feedtype ' f'{feedtype} '.split()
    out = subprocess.run(command, capture_output=True)
    if out.stdout == b'':
        return out.stderr.decode()
    else:
        return out.stdout.decode()


@app.put('/feedback_snippet/{file_path:path}', tags=["feedback"])
async def feedback_snippet(file_path: str = Path(..., description="/sub_code/year/category/Qn", ),
                           entryfnc: str = Query(..., description="The name of the entry function"),
                           args: str = Query(..., description="The argument parameters without spaces"),
                           feedtype: Optional[str] = Query('python', description="python, simple or repair"),
                           code: str = Query(..., description="The incorrect code for feedback"),
                           ext: Optional[str] = Query('.py', description="File extenstions: .java, .py or .c")):
    cluster_path = os.getcwd() + '/clusters' + f"{file_path}/"
    path = ""
    for filename in [f for f in os.listdir(cluster_path) if f'{ext}' in f]:
        path += cluster_path + filename + " "
    sol = codecs.decode(code, 'unicode-escape')
    with open(f'incorrect/incorrect{ext}', 'w') as writer:
        writer.write(sol)
    command = f'clara feedback {path} incorrect/incorrect{ext} --entryfnc {entryfnc} --args {args} --ignoreio 1 --feedtype ' \
              f'{feedtype} '.split()
    out = subprocess.run(command, capture_output=True)
    if out.stdout == b'':
        return out.stderr.decode()
    else:
        return out.stdout.decode()
