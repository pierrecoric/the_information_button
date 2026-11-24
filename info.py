from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import random
from gtts import gTTS
import subprocess



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

#Get all the links
all_links = soup.find_all("a", href=True)
   
#Get the content of all the paragraphs.
paragraphs = soup.find_all("p")
clean_paragraphs = []
for paragraph in paragraphs:
    clean_paragraphs.append(paragraph.get_text())

#Get the title of the page
title = soup.find_all("h1")
print(title[0].get_text())

#Get a random paragraph.
random_paragraph = clean_paragraphs[random.randint(1, len(clean_paragraphs) - 1)]
print(random_paragraph)

tts = gTTS(text=random_paragraph, lang="en", slow=False)
tts.save("speech.mp3")
subprocess.run(["afplay", "speech.mp3"], check=True)