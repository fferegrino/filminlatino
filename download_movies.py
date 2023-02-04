import requests
import time
from driver import get_driver
from settings import BASE_HEADERS, INITIAL_WAIT_TIME
from copy import deepcopy

driver = get_driver()

def get_cookies():
    driver.get("https://www.filminlatino.mx/catalogo/peliculas?rights=all")
    time.sleep(INITIAL_WAIT_TIME)
    cookies_dict = {}
    for cookie in driver.get_cookies():
        cookies_dict[cookie["name"]] = cookie["value"]
    return cookies_dict

def merge_cookies(cookies_dict):
    parts = [f"{k}={v};" for k, v in cookies_dict.items()]
    cookie = " ".join(parts)
    return cookie

def get_headers():
    headers = deepcopy(BASE_HEADERS)
    cookies_dict = get_cookies()
    headers["cookie"] = merge_cookies(cookies_dict)
    headers["referer"] = "https://www.filminlatino.mx/catalogo/peliculas?rights=all"
    headers["x-csrf-token"] = cookies_dict["XSRF-TOKEN"]
    headers["x-xsrf-token"] = cookies_dict["XSRF-TOKEN"]

    return headers


headers = get_headers()

movies = []
for page in range(1, 1000):
    data = requests.get(
        f"https://www.filminlatino.mx/wapi/catalog/browse?rights=svod&type=film&page={page}&limit=60", headers=headers
    ).json()['data']

    time.sleep(1)
    if not data:
        break
    movies.extend([m['url'] for m in data])


# Write all movies to file
with open("peliculas/urls.txt", "w") as f:
    f.write("\n".join(sorted(movies)))
