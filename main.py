from fastapi import FastAPI
import urllib.request, json
import random
import requests

app = FastAPI()

user_num = 50

class Country:
    def __init__(self, name, capital, population, languages):
        self.name = name
        self.capital = capital
        self.population = population
        self.languages = languages

def add_country(country_num, data, list_countries):
    if data[country_num]["country"] in list_countries:
        with urllib.request.urlopen("https://random-data-api.com/api/v2/addresses") as url:
            temp_data = json.load(url)
            print(temp_data)
            list_countries.append(temp_data["country"])
        print(f"deleted {data[country_num]}")
    else:
        list_countries.append(data[country_num]["country"])
    return list_countries

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/countries")
async def get_address():
    list_countries = []
    with urllib.request.urlopen("https://random-data-api.com/api/v2/addresses?size="+f"{user_num}") as url:
        data = json.load(url)
    for country_num in range(user_num):
        list_countries = add_country(country_num, data, list_countries)
    print(len(list_countries) == user_num)
    requested_countries = []
    for i in range(len(list_countries)):
        country = list_countries[i].replace(" ", "")
        url_country = "https://restcountries.com/v3.1/name/"+f"{country}"
        if requests.get(url_country).status_code == 404:
            requested_countries.append({country:"No information found!", "population":0})
        else:
            with urllib.request.urlopen(url_country) as url:
                data = json.load(url)

            capital = "There is no official capital"
            if "capital" in data[0]:
                capital = data[0]["capital"]

            country1 = Country(data[0]["name"]["official"],
                               capital,
                               data[0]["population"],
                               data[0]["languages"])
            if  len(requested_countries) == 0 or country1.population >= requested_countries[0]["population"]:
                requested_countries.insert(0, country1.__dict__)
            else:
                for a in range(len(requested_countries)):
                    if country1.population >= requested_countries[a]["population"]:
                        requested_countries.insert(a, country1.__dict__)
                        break
    return requested_countries

