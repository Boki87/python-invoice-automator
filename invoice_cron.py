#!/usr/bin/env python3

import json
from datetime import datetime

import pdfkit

current_date = datetime.now()

# calculate the previous month and year
current_month = current_date.month
current_year = current_date.year
current_month_name = current_date.strftime("%B")


if current_month == 1:
    previous_month = 12
    previous_year = current_year - 1
else:
    previous_month = current_month - 1
    previous_year = current_year

# Create a date for the first day of the previous month
previous_month_date = datetime(previous_year, previous_month, 1)

# Get the previous month's name
previous_month_name = previous_month_date.strftime("%B")


HTML_TEMPLATE = "template.html"


def render_tamplate(template_path, data):
    with open(template_path, "r") as file:
        template = file.read()
    for key, val in data.items():
        if key != "items":
            template = template.replace(f"{{{{ {key} }}}}", val)
    return template


# load data from json
with open("data.json", "r") as f:
    data = json.load(f)

# sum up the amount of all items
amount = 0
items_html = "<tr>"
for item in data["items"]:
    amount += int(item["rate"])
    formated_item_rate = "{:,.2f}".format(int(item["rate"]))
    formated_item_rate = data["currency"] + formated_item_rate
    items_html += f"""
          <td class="items bold">{item['item']}</td>
          <td class="rest">{item['quantity']}</td>
          <td class="rest">{formated_item_rate}</td>
          <td class="rest">{formated_item_rate}</td>
    """
items_html += "</tr>"

formated_amount = "{:,.2f}".format(amount)
formated_amount = data["currency"] + formated_amount

tax = int(data["tax"])
tax_total = tax / 100 * amount
formated_tax = "{:,.2f}".format(tax_total)

total_amount = amount + tax_total
formated_total = "{:,.2f}".format(total_amount)
formated_total = data["currency"] + formated_total

data["items_html"] = items_html.replace("{{month}}", previous_month_name)
data["formated_amount"] = formated_amount
data["formated_tax"] = formated_tax
data["formated_total"] = formated_total


data["date"] = current_month_name + " 1, " + str(current_year)
data["due_date"] = current_month_name + " 15, " + str(current_year)

data["prev_invoice_number"] = str(int(data["prev_invoice_number"]) + 1)
data["invoice_number"] = data["prev_invoice_number"]


# print(data)

# generate pdf
html_content = render_tamplate(HTML_TEMPLATE, data)

output_path = (
    f"./invoices/Invoice_{data['invoice_number']}_{current_year}_{data['name']}.pdf"
)

pdfkit.from_string(html_content, output_path)


# clean json and write new invoice number to it
del data["items_html"]
del data["formated_amount"]
del data["formated_tax"]
del data["formated_total"]
del data["date"]
del data["due_date"]
del data["invoice_number"]
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)


print("PDF generated")

# TODO: send email from gmail
