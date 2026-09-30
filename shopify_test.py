import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

shop = os.getenv("SHOPIFY_SHOP")
client_id = os.getenv("SHOPIFY_CLIENT_ID")
client_secret = os.getenv("SHOPIFY_CLIENT_SECRET")

url = f"https://{shop}.myshopify.com/admin/oauth/access_token"

#############################
##     GET ACCESS TOKEN
#############################

auth_url = f"https://{shop}.myshopify.com/admin/oauth/access_token"
auth_response = requests.post(
    auth_url,
    data ={
        "grant_type":"client_credentials",
        "client_id":client_id,
        "client_secret": client_secret
    },
)

auth_response.raise_for_status()
access_token = auth_response.json()["access_token"]
print("Auth successful")

###########################
####### GRAPH QL ##########
###########################

graphql_url = (
    f"https://{shop}.myshopify.com"
    "/admin/api/2026-07/graphql.json"
)

query = """
query {
    products(first: 10) {
        nodes {
            id
            title
        }
    }
}
"""

response = requests.post(
    graphql_url,
    headers={
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token,
    },
    json={
        "query": query
    },
)

response.raise_for_status()
response.raise_for_status()
data = response.json()
print(json.dumps(data, indent=2))