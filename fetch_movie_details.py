import json
import os
import time
from copy import deepcopy

import requests

from driver import get_driver
from settings import BASE_HEADERS, INITIAL_WAIT_TIME

driver = get_driver()


def get_cookies(movie_slug):
    driver.get(f"https://www.filminlatino.mx/pelicula/{movie_slug}")
    time.sleep(INITIAL_WAIT_TIME)
    cookies_dict = {}
    for cookie in driver.get_cookies():
        cookies_dict[cookie["name"]] = cookie["value"]

    return cookies_dict


def merge_cookies(cookies_dict):
    parts = [f"{k}={v};" for k, v in cookies_dict.items()]
    cookie = " ".join(parts)
    return cookie


def get_movie_info(movie_slug):
    headers = deepcopy(BASE_HEADERS)
    cookies_dict = get_cookies(movie_slug)
    headers["cookie"] = merge_cookies(cookies_dict)
    headers["referer"] = f"https://www.filminlatino.mx/pelicula/{movie_slug}"
    headers["x-csrf-token"] = cookies_dict["XSRF-TOKEN"]
    headers["x-xsrf-token"] = cookies_dict["XSRF-TOKEN"]

    req = requests.get(
        f"https://www.filminlatino.mx/wapi/medias/film/{movie_slug}", headers=headers
    )

    return req.json()


with open("peliculas/urls.txt", "r") as f:
    anchors = f.read().splitlines()
    for anchor in anchors:
        [*_, slug] = anchor.rsplit("/")
        info_json = f"peliculas/{slug}.json"

        if os.path.exists(info_json):
            continue
        info = get_movie_info(slug)
        print(f"Saving {slug} to {info_json}")
        with open(info_json, "w") as f:
            json.dump(info, f, indent=4, sort_keys=True)
