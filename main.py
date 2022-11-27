from fastapi import FastAPI, HTTPException
import urllib.request, json
import requests

app = FastAPI()

class Country:
    def __init__(self, name, capital, population, languages):
        self.name = name
        self.capital = capital
        self.population = population
        self.languages = languages

def add_country_and_replace_nonunique(country_index, addresses, list_countries):
    current_country = addresses[country_index]["country"]
    while current_country in list_countries:
        with urllib.request.urlopen("https://random-data-api.com/api/v2/addresses") as url:
            temp_data = json.load(url)
            current_country = temp_data["country"]
            addresses[country_index] = temp_data
    list_countries.append(current_country)
    return list_countries


def make_list_countries(countries_amount):
    list_countries = []
    with urllib.request.urlopen("https://random-data-api.com/api/v2/addresses?size=" + f"{countries_amount}") as url:
        addresses = json.load(url)
    for country_index in range(countries_amount):
        list_countries = add_country_and_replace_nonunique(country_index, addresses, list_countries)
    addresses_and_countries = {
        "countries": list_countries,
        "addresses": addresses
    }
    return addresses_and_countries

def request_countries(list_countries):
    requested_countries = []
    for i in range(len(list_countries)):
        country_without_spaces = list_countries[i].replace(" ", "")
        url_country = "https://restcountries.com/v3.1/name/" + f"{country_without_spaces}"
        if requests.get(url_country).status_code == 404:
            requested_countries.append({list_countries[i]: "No information found!", "population": 0})
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
            if len(requested_countries) == 0 or country1.population >= requested_countries[0]["population"]:
                requested_countries.insert(0, country1.__dict__)
            else:
                for a in range(len(requested_countries)):
                    if country1.population >= requested_countries[a]["population"]:
                        requested_countries.insert(a, country1.__dict__)
                        break
    return requested_countries


@app.get("/")
async def root():
    return {
        "APP NAME": "Country randomizer",
        "Usage": "Open /countries/ordered_by_population?countries_amount={int}&show_addresses={bool}"
    }

@app.get("/countries/ordered_by_population")
async def countries_ordered_by_population(countries_amount:int, show_addresses: bool):
    if countries_amount < 5 or countries_amount > 20:
        raise HTTPException(status_code=400, detail="Requested number is out of possible range, "
                                                    "countries_amount should be from 5 to 20")
    countries_and_addresses = make_list_countries(countries_amount)
    countries_with_data = request_countries(countries_and_addresses["countries"])
    if show_addresses:
        return {"addresses":countries_and_addresses["addresses"],
                "countries": countries_with_data}
    else:
        return countries_with_data