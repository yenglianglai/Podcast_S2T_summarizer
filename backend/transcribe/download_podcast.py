from bs4 import BeautifulSoup
import requests
import logging


def download_mp3(url):
    def get_podcast_url(url):
        logging.info("getting url...")
        print()
        page = requests.get(url)
        soup = BeautifulSoup(page.content)
        divs = soup.find_all("div", jsname="fvi9Ef")

        mp3_url = str(divs[0].attrs.get("jsdata", None))
        mp3_url = mp3_url[mp3_url.find("https") :]
        return mp3_url

    def download_mp3_from_url(mp3_url):
        logging.info("downloading mp3...")
        audio = requests.get(mp3_url)
        with open("audio.mp3", "wb") as file:
            file.write(audio.content)

    mp3_url = get_podcast_url(url)
    download_mp3_from_url(mp3_url)
