import requests
from bs4 import BeautifulSoup
import re
import time

def google_Search(search_words):
    search_words = search_words[8:]
    response = requests.get(
    f"https://www.bing.com/search?q={search_words}",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    })
    time.sleep(1)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.select("h2 a")
    arrayTitle = []
    arrayURL = []
    arrayOutput = []
    for d in data:
        arrayTitle.append(d.text)
        arrayURL.append(d["href"])
    for i in range(len(arrayTitle)):
        arrayOutput.append(f"{str(arrayTitle[i])} ---> {str(arrayURL[i])}")
    arrayOutput = str(arrayOutput)
    arrayOutput = re.sub("\[|\'|\]","",arrayOutput)
    return arrayOutput.replace(', ',"\n")