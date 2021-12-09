import random
import webbrowser

import httpx
from rich.console import Console

from waffle import sprinkles

console = Console()

limit = 16
language = "en-GB"
country = "gb"
max_prep_time = 30
min_rating = 3.3

URL = f"https://gw.hellofresh.com/api/recipes/search"
params = {
    "limit": limit,
    "locale": language,
    "country": country,
    "max-prep-time": max_prep_time,
    "sort": "-favorites",
}

user_agent = "Shahnoza"
headers = {
    "accept": "applicaton/json",
    "Authorization": f"Bearer {sprinkles.TOKEN}",
    "user-agent": user_agent,
}


def get_receips_list():
    response = httpx.get(URL, params=params, headers=headers)
    r = response.json()


receipts = [
    {
        "name": receipt["name"],
        "link": receipt["cardLink"],
        "ingredients": receipt["ingredients"],
        "serving": receipt["yields"][0]["ingredients"],
    }
    for receipt in r["items"]
]

ingredients_ids = {
    ingredient["id"]: ingredient["name"]
    for receipt in receipts
    for ingredient in receipt["ingredients"]
}
random_receipt = random.choice(receipts)
cook = {
    "dish": random_receipt["name"],
    "link": random_receipt["link"],
    "shopping list": {
        ingredients_ids[serving["id"]]: f'{serving["amount"]} {serving["unit"]}'
        for serving in random_receipt["serving"]
    },
}

webbrowser.open_new_tab(cook["link"])
console.print(cook)
