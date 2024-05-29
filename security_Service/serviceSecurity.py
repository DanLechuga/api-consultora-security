import datetime
from fastapi import HTTPException

from bson import ObjectId
from jose import jwt
from security_middleware.dto.response import UserOutput,Token,DataToken
from security_middleware.helpers import utils
from security_middleware.dto.request import CreateUser
from security_Repositories import userRepository
import os
from starlette import status

def getVariable(name):
    return os.environ.get(name,"NOT FOUND")




SECRET_KEY = getVariable("key_jwt")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


async def AddUser(user : CreateUser.CreateUser) -> UserOutput.UserOutput:
    hashed_pass = utils.hash_pass(user.password)
    user.password = hashed_pass
    coll = {
        "_id":f"{ObjectId()}",
        "email":f"{user.email}",
        "password":f"{user.password}",
        "created_at":f"{datetime.datetime.now()}"
    }
    await userRepository.InsertUser(coll)  
    response = UserOutput.UserOutput(
        id= str(coll["_id"]),
        email= coll["email"],
        created_at=coll["created_at"]
    )
    return response


async def verifyLogin(user) -> Token.Token:
    userinDb =  await userRepository.GetUserByEmail(user.username)
    if(userinDb is not None):
        if(utils.verify_pass(user.password,userinDb['password'])):    
            to_encode = userinDb
            expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
            response = Token.Token(
                access_token= encoded_jwt,
                token_type="Bearer"
            )
            return response
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not Validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not Validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"}) 
        
        
