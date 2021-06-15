import codecs
import os
import subprocess
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, Path, Query, Body, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

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


app = FastAPI()


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

@app.get("/", tags=["docs"])
async def read_root():
    return RedirectResponse('./docs')


@app.get("/phantom")
async def read_phan():
    return "Hello world"


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


@app.post('/submit/{file_path:path}', tags=["submit"], status_code=201)
def submit(code: str = Query(..., description="The code to be submitted"),
           sid: str = Query(..., description="The student ID"),
           file_path: str = Path(..., description="/sub_code/year/category/Qn", )):
    sol = codecs.decode(code, 'unicode-escape')
    path = os.getcwd() + file_path
    os.makedirs(path, exist_ok=True)

    with open(path + '/' + sid + '.py', 'w') as writer:
        writer.write(sol)
    return 'Submission of {sid}.py is successful'


@app.put('/cluster/{file_path:path}', tags=["cluster"], status_code=202)
async def cluster(file_path: str = Path(..., description="/sub_code/year/category/Qn", ),
                  entryfnc: str = Query(..., description="The name of the entry function"),
                  args: str = Query(..., description="The argument parameters without spaces"),
                  filenames: List[str] = Body(..., description="The file to be submitted")):
    cluster_path = os.getcwd() + '/clusters' + file_path
    path = ""
    for filename in filenames:
        path += os.getcwd() + f"{file_path}/" + filename + " "
    os.makedirs(cluster_path, exist_ok=True)
    command = f'clara cluster {path} --clusterdir {cluster_path} --entryfnc {entryfnc} --args {args} ' \
              f'--ignoreio 1'.split()
    out = subprocess.run(command, capture_output=True)
    if out.stdout == b'':
        return out.stderr.decode()
    else:
        return out.stdout.decode()


@app.put('/cluster_folder/{file_path:path}', tags=["cluster"], status_code=202)
async def cluster_folder(file_path: str = Path(..., description="/sub_code/year/category/Qn", ),
                         entryfnc: str = Query(..., description="The name of the entry function"),
                         args: str = Query(..., description="The argument parameters without spaces")):
    cluster_path = os.getcwd() + '/clusters' + file_path
    folder_path = os.getcwd() + f"{file_path}/"
    path = ""
    for filename in os.listdir(folder_path):
        path += folder_path + filename + " "
    os.makedirs(cluster_path, exist_ok=True)
    command = f'clara cluster {path} --clusterdir {cluster_path} --entryfnc {entryfnc} --args {args} ' \
              f'--ignoreio 1'.split()
    out = subprocess.run(command, capture_output=True)
    if out.stdout == b'':
        return out.stderr.decode()
    else:
        return out.stdout.decode()


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


@app.post("/uploadfile/{file_path:path}", tags=["submit"], status_code=201)
async def submit_file(file_path: str = Path(..., description="/sub_code/year/category/Qn"),
                      file: UploadFile = File(..., description="The file to be submitted")):
    path = os.getcwd() + file_path
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{file.filename}', 'wb') as writer:
        writer.write(await file.read())
    return f'{file.filename} submitted successfully at {file_path}'


@app.post("/uploadfiles/{file_path:path}", tags=["submit"], status_code=201)
async def submit_files(file_path: str = Path(..., description="/sub_code/year/category/Qn"),
                       files: List[UploadFile] = File(..., description="The list of files submitted")):
    path = os.getcwd() + file_path
    os.makedirs(path, exist_ok=True)
    for file in files:
        with open(f'{path}/{file.filename}', 'wb') as writer:
            writer.write(await file.read())
    return [f'{file.filename} submitted successfully at {file_path}' for file in files]
