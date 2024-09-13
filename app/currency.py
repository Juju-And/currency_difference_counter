import json
from urllib.request import urlopen

invoice_date = "2024-05-16"
transfer_date = "2024-05-16"

def get_currency_rate(date):
    invoice_rate_url = urlopen(f'https://api.nbp.pl/api/exchangerates/tables/A/{date}/?format=json')
    in_json = invoice_rate_url.read()
    in_jdata = json.loads(in_json)
    # get USD currency rate for the declared date
    rate = in_jdata[0]['rates'][1]["mid"]
    return rate

def collect_currency_rates(invoice_date, transfer_date):
    # while True:
    #     try:
    #         invoice_date = input("When the invoice was issued? (a date in the YYYY-MM-DD format) ")
    #         break
    #     except ValueError:
    #         print("Invalid Input, please use YYYY-MM-DD format")
    #
    # while True:
    #     try:
    #         transfer_date = input("When the transfer was registered to your account? (a date in the YYYY-MM-DD format) ")
    #         break
    #     except ValueError:
    #         print("Invalid Input, please use YYYY-MM-DD format")

    date_and_rate = {
        "invoice_date": invoice_date,
        "invoice_rate": get_currency_rate(invoice_date),
        "transfer_date": transfer_date,
        "transfer_rate": get_currency_rate(transfer_date)
    }

    return date_and_rate


def calculate_currency_dif():
    # while True:
    #     try:
    #         invoice_value = float(input("Input the value of your latest invoice in USD... "))
    #         break
    #     except ValueError:
    #         print("Invalid Input, please use format XXXX.XX")
    invoice_value = 1000
    date_and_rate = collect_currency_rates(invoice_date, transfer_date)

    # calculate invoice value in PLN for the date of the invoice issue (previous working day)
    invoice_value_pln = invoice_value * date_and_rate["invoice_rate"]

    # calculate invoice value in PLN for the date of the day of transfer (previous working day)
    invoice_value_pln_transfer = invoice_value * date_and_rate["transfer_rate"]

    # negative or positive exchange differences
    difference = invoice_value_pln - invoice_value_pln_transfer

    if difference > 0:
        print("Positive exchange differences")
    else:
        print("Negative exchange differences")


    currency_data = {
        "invoice_value": invoice_value,
        "date_of_invoice_issue": date_and_rate["invoice_date"],
        "currency_rate_day_of_issue": date_and_rate["invoice_rate"],
        "date_of_invoice_transfer": date_and_rate["transfer_date"],
        "currency_rate_day_of_transfer": date_and_rate["transfer_rate"]

    }

    print(currency_data)

calculate_currency_dif()
