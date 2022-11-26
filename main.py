from fastapi import FastAPI
import urllib.request, json
import random

app = FastAPI()

user_num = random.randint(5, 20)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/addresses")
async def get_address():
    list_countries = []
    with urllib.request.urlopen("https://random-data-api.com/api/v2/addresses?size="+f"{user_num}") as url:
        data = json.load(url)
    for i in range(user_num):
        list_countries.append(data[i]["country"])
    return list_countries


#delete random