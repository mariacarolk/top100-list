import requests
from requests.exceptions import HTTPError
import re
from bs4 import BeautifulSoup

URL = 'https://www.usatoday.com/picture-gallery/life/music/2019/05/29/the-100-absolute-best-songs-in-history/39513475/'

html_text = ''

# Pattern code for get info from web
def crawl_website(URL):
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except HTTPError as exc:
        print(exc)
    else:
        html_text = response.text

    return html_text

file_name = ''

def write_html(str: file_name, text) -> str:
    with open (file=file_name, mode='w', errors="ignore") as html_file:
        html_file.write(text)

text = ''

#Return the HTML
text = crawl_website(URL)

file_name = 'file_music.html'
write_html(file_name, text)

# Creates a BeautifulSoup object containing the page data
page = BeautifulSoup(open(file_name, mode='r'), 'html.parser')

# Search all HTML elements that matches the specified criteria and returns a ResultSet object
table = page.find_all('div', {'class': 'gnt_pg_img_cap'})

music_list = []

# Iters lines and columns of the ResultSet to extract the information needed
for div in table:
    # Extracting position, music, and artist information
    div_text = div.get_text(strip=True)
    # Looks for one or more digits (\d+) at the beginning (^) of the div_text string
    position = re.search(r'^\d+', div_text).group()

    music_artist_match = re.search(r'(\d+\.\s*)(.*)\s*•\s*Artist:\s*(.*)\s*•\s*Year:\s*(\d+)', div_text)

    if music_artist_match:
        music = music_artist_match.group(2).strip()
        artist = music_artist_match.group(3).strip()

        # Creating a dictionary for each entry
        entry = {
            'Position': position,
            'Music': music,
            'Artist': artist
        }

        music_list.append(entry)

# Order the list by position
music_list = sorted(music_list, key=lambda x: int(x['Position']))

# Write a csv file
with open (file='music.csv', mode='w', encoding='utf8') as csv_file:
    csv_file.write('position;music;artist\n')

    for music in music_list:
        csv_line = music['Position'] + ';' + music['Music'] + ';' + music['Artist'] + '\n'
        csv_file.write(csv_line)
