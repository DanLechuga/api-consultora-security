from security_Repositories import unitOfWork

async def InsertUser(user):
    if(await unitOfWork.connectionDb()):
        unitOfWork.InserUser(user)
        
        
async def GetUserByEmail(email):
    if(await unitOfWork.connectionDb()):
        return unitOfWork.getUserByEmail(email)
    return None           