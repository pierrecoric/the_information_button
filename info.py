from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import random
from gtts import gTTS
import subprocess
import re

#The seed URL
with open("seed.txt", "r") as file:
    seed_url = file.read().strip()

#Building the request
req = Request(
    seed_url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
)

#Getting the html and parsing it.
with urlopen(req) as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Get all the links
all_links = soup.find_all("a", href=True)

# Extract URLs
links = [link["href"] for link in all_links]

#Get the clean ones.
wiki_url = "https://en.wikipedia.org/wiki/"
clean_links = []
for link in links:
    if wiki_url in link and "#" not in link and "File" not in link and "Help" not in link and "Template" not in link and "Talk" not in link and "Wikipedia" not in link:
        clean_links.append(link)

   
#Get the content of all the paragraphs.
paragraphs = soup.find_all("p")
clean_paragraphs = []
for paragraph in paragraphs:
    text = paragraph.get_text(strip=True)
    #Remove square brackets and their content
    text = re.sub(r'\[.*?\]', '', text)
    if len(text) > 65:
        clean_paragraphs.append(text)

#Getting the title of the page.
title_current = soup.find_all("h1")
title_current = title_current[0].get_text()

#Get a random paragraph.
if len(clean_paragraphs) > 0:
    random_paragraph = clean_paragraphs[random.randint(0, len(clean_paragraphs) - 1)]
else:
    random_paragraph = "no information."

#Build the text.
text_content = f'Some information about {title_current}. {random_paragraph}'

#Navigation.
#Get a random link from the page.
random_link = clean_links[random.randint(0, len(clean_links) - 1)]

#Building the next request
req = Request(
    random_link,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
)

#Get the title fo that page.
with urlopen(req) as fp:
    soup = BeautifulSoup(fp, "html.parser")

#Getting the title of the next page.
title_next = soup.find_all("h1")
title_next = title_next[0].get_text()



#Write history
#Went from "title" to "title"
with open("output/history.md", "a") as file:
    file.write(f'We went from [{seed_url}]({title_current}) to [{random_link}]({title_next})\n')

with open("output/some_info.md", "a") as file:
    file.write(f'Some information about [{seed_url}]({title_current}). {random_paragraph}\n')

#change seed to a random link.
with open("seed.txt", "w") as file:
    file.write(f'{random_link} ')

#Speak the info.
tts = gTTS(text=text_content, lang="en", slow=False)
tts.save("info.mp3")
subprocess.run(["afplay", "info.mp3"], check=True)
