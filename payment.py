import requests

url = "https://mercury-uat.phonepe.com/v3/debit"

headers = {
    'content-type': "application/json",
    'x-verify': "X-VERIFY"
    }

response = requests.request("POST", url, headers=headers)

print(response.text)