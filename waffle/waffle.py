import random
import typing as t
import webbrowser

import httpx

from waffle import sprinkles
from waffle.baker import waffle_baker

URL = f"https://gw.hellofresh.com/api/recipes/search"


user_agent = "Shahnoza"
headers = {
    "accept": "applicaton/json",
    "Authorization": f"Bearer {sprinkles.TOKEN}",
    "user-agent": user_agent,
}


def get_receipts_list(params: t.Dict):
    response = httpx.get(URL, params=params, headers=headers)
    return response.json()


def get_random_receipt(json_response: t.Dict):

    receipts = [
        {
            "name": receipt["name"],
            "link": receipt["cardLink"],
            "ingredients": receipt["ingredients"],
            "serving": receipt["yields"][0]["ingredients"],
        }
        for receipt in json_response["items"]
    ]

    ingredients_ids = {
        ingredient["id"]: ingredient["name"]
        for receipt in receipts
        for ingredient in receipt["ingredients"]
    }
    random_receipt = random.choice(receipts)
    return {
        "dish": random_receipt["name"],
        "link": random_receipt["link"],
        "shopping list": {
            ingredients_ids[serving["id"]]: f'{serving["amount"]} {serving["unit"]}'
            for serving in random_receipt["serving"]
        },
    }


params = {
    "limit": sprinkles.limit,
    "locale": sprinkles.language,
    "country": sprinkles.country,
    "max-prep-time": sprinkles.max_prep_time,
    "sort": "-favorites",
}

response_json = get_receipts_list(params=params)
cook = get_random_receipt(response_json)
webbrowser.open_new_tab(cook["link"])
waffle_baker(cook)
