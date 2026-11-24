from bs4 import BeautifulSoup
from urllib.request import Request, urlopen



url = "https://en.wikipedia.org/wiki/Arlon"

req = Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
)

with urlopen(req) as fp:
    soup = BeautifulSoup(fp, "html.parser")

print(soup.prettify())
