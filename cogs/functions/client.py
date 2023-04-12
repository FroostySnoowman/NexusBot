import yaml
import paypalrestsdk
from paypalrestsdk import Invoice

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

name = data["General"]["NAME"]
website = data["General"]["WEBSITE"]
tos = data["General"]["TOS"]
ns_logo_url = data["General"]["NS_LOGO_URL"]
paypal_client_id = data["PayPal"]["PAYPAL_CLIENT_ID"]
paypal_client_secret = data["PayPal"]["PAYPAL_CLIENT_SECRET"]

my_api = paypalrestsdk.Api({
  'mode': 'live',
  'client_id': paypal_client_id,
  'client_secret': paypal_client_secret})

async def createinvoice(total):
    fee = total * 0.05 + 0.4
    invoice = Invoice({
        "merchant_info": {
            "business_name": name,
            "website": website
        },
        "items": [
            {
                "name": "Commission Service",
                "description": f"Service at {name}",
                "quantity": 1,
                "unit_price": {
                    "currency": "USD",
                    "value": total
                }
            },
            {
                "name": "Fee",
                "description": "The fee for this invoice as per our TOS.",
                "quantity": 1,
                "unit_price": {
                    "currency": "USD",
                    "value": fee
                }
            }
        ],
        "note": f"This invoice is for your ticket at {name}. \nYou should pay at least 50% + fees to let the freelancer start.",
        "terms": tos,
        "payment_term": {
            "term_type": "NET_45"
        },
        "allow_partial_payment": True,
        "minimum_amount_due": {
            "currency": "USD",
            "value": (total + fee) * 0.5
        }
    }, api=my_api)

    if invoice.create():
        invoice = Invoice.find(invoice['id'], api=my_api)
        if invoice.send():
            id = invoice.id
            return(id)