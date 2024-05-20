from pymongo import MongoClient
import os

def getVariable(name):
    return os.environ.get(name,"NOT FOUND")
conection = getVariable("bd_security")

client = MongoClient(conection)


async def connectionDb() ->bool:
    isConnect = False
    try:
        client.admin.command("ping")
        isConnect=True
        
    except Exception as e:
        print(f"{e}")
    
    return isConnect    



def InserUser(user):
    client.get_database("securityService").get_collection("User").insert_one(user)
    
    
def getUserByEmail(email):
    return client.get_database("securityService").get_collection("User").find_one({"email":f"{email}"})