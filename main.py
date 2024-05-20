from fastapi import Depends, FastAPI,HTTPException
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from security_middleware.dto.response import UserOutput,Token
# from security_middleware.dto.request import CreateUser
from security_Service import serviceSecurity
# {
#         "name": "Users",
#         "description": "Operations with users.",
#     }
app = FastAPI(
    title='Service Security',
    openapi_tags=[
    {
        "name": "Authentication",
        "description": "Authentication user.",
    }],
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian"
    }
)


@app.get("/",include_in_schema=False,response_class=RedirectResponse)
async def goToSwagger():
    return "/docs"

@app.post("/security/login",tags=["Authentication"],status_code=status.HTTP_202_ACCEPTED,response_model=Token.Token)
async def login(userCredentials :OAuth2PasswordRequestForm = Depends()):
    try:
        data = await serviceSecurity.verifyLogin(userCredentials)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{e}"
        )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"acces_token":f"{data.access_token}","type_token":"bearer"}
    )            


# @app.post('/security/user',tags=['Users'], status_code=status.HTTP_201_CREATED,response_model=UserOutput.UserOutput)
# async def create_users(user:CreateUser.CreateUser):
#     try:
#         new_user = await serviceSecurity.AddUser(user)
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=f"{e}"
#         )
#     return JSONResponse(
#         status_code= status.HTTP_201_CREATED,
#         content={
#             "created":True,
#             "data":new_user.id
#         }
#     )

