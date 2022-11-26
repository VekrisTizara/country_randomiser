from fastapi import FastAPI
from pydantic import BaseModel
import urllib.request, json
import random
import requests


app = FastAPI()

user_num = random.randint(5, 20)

class Country(BaseModel):


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/countries")
async def get_address():
    list_countries = []
    with urllib.request.urlopen("https://random-data-api.com/api/v2/addresses?size="+f"{user_num}") as url:
        data = json.load(url)
    for country_num in range(user_num):
        list_countries.append(data[country_num]["country"])

    print(list_countries[0])

    for i in range(len(list_countries)):
        country = list_countries[i].replace(" ", "")
        url_country = "https://restcountries.com/v3.1/name/"+f"{country}"
        if requests.get(url_country).status_code == 404:
            print(404)
        else:
            with urllib.request.urlopen(url_country) as url:
                data = json.load(url)
        return data

