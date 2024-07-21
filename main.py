from card import CardPage
from urllib.parse import urlsplit
import os

urls = [
    {
        "url": "https://steamcommunity.com/market/listings/753/17390-Fwoops",
        "id": "1"
    },
    {
        "url": "https://steamcommunity.com/market/listings/753/17390-Geoff%20%28Foil%29",
        "id": "2"
    },
    {
        "url": "https://steamcommunity.com/market/listings/753/304650-Bandaged%20Poissonnier",
        "id": "3"
    },
]

# print(os.path.split(urlsplit(urls[0]["url"]).path)[-1].split("-")[0])

with CardPage() as card:
    for url in urls:
        if content := card.get(url["url"]):
            with open(f"{url['id']}selenium-context.html", "w", encoding="utf-8") as f:
                f.write(content)
