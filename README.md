# Apartment-scrapper

This is a web application intended to calculate currency difference between the day of issuing an invoice and the day of actual transfer to the bank account. It should always take into consideration the currency rate from the last working day before the date of issue/transfer. 
The application accepts invoice value and two dates in order to give user the difference which should be booked for tax purposes.


## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Install all required modules running pip with the provided file:

```
$ pip install -r requirements.txt
```

### Installing

As a first step, you need to create locally PostgreSQL database named 'currencyrates'. 

Secondly,copy the .env.sample as .env and fill with your PostgreSQL credentials.

```
user = "your_user"
pw = "your_password"
db = "currencyrates"
host = "localhost"
port = "5432"
SECRET_KEY = "your_key"
```

## Running locally#
