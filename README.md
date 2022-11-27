# Country randomiser

## About
This web application accepts an amount of countries (from 5 to 20), sends a request to API `https://random-data-api.com/` to get that amount of unique countries, and then collects information about the capital, population and languages of those countries by requesting API of `restcountries.com`. After that, the app returns the collected information in JSON.

## Requirements
Python 3.9 with pip
There is requirements.txt file with all the necessary libraries.
run `pip install -r requirements.txt`

## How to use the application
After installing all the required packages, application can be started by command `uvicorn main:app`. The help message will be on the address `http://127.0.0.1:8000/`  
There two ways to get information about countries:
1. You can type a number between 5 and 20 after the part "ordered_by_population?countries_amount=" and select if you want to see the full list of requested countries with addreses (from thr first API). For example, a full link can look like this: 
127.0.0.1:8000/countries/ordered_by_population?countries_amount=15&show_addresses=True
2. You can open FastAPI documentation, using the link: 
http://127.0.0.1:8000/docs
And use Swagger interface.
This method will show information in a more readable view. 

