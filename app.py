from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0]["rates"]

exchange_list = ["currency", "code", "bid", "ask"]

#print(rates)

with open("currency.csv", "w", encoding="UTF8", newline="") as csvfile:
    output = csv.DictWriter(csvfile, delimiter=";", fieldnames=exchange_list)
    output.writeheader()
    for rate in rates:
        output.writerow(rate)

currency_list = []
csv_list = {}
bid_list = []

with open("currency.csv", "r", encoding="UTF8", newline="") as csvfile:
    input_list = csv.DictReader(csvfile, delimiter=";", fieldnames=exchange_list)
    index = 0
    for x in input_list:
        currency_list.append([index,x["currency"].title()])
        bid_list.append(x['bid'])
        index += 1
    csvfile.close()


@app.route("/nbp", methods=["GET", "POST"])
def calc():

    if request.method == 'GET':
        return render_template("nbp_calc.html", options=options)

    if request.method == "POST":
        option = int(request.form["option"][1:2])
        amount = int(request.form.get("amount"))
        bid_value = float(bid_list[option])
        result = bid_value * amount
        return render_template("nbp.html", items=currency_list, b=bid_value, p=result)
    return render_template("nbp.html", items=currency_list)

if __name__ == "__main__":
    app.run(debug=True)
