import requests
from bs4 import BeautifulSoup
import random

response = requests.get("https://aosd.slac.stanford.edu/wiki/index.php/Training")
print(response.status_code)

soup = BeautifulSoup(response.content, 'html.parser')
#print(soup.prettify())

list(soup.children)
links = soup.find(id = 'bodyContent').find_all('a')
hrefLink = [a for a in links if a['href'].startswith('/wiki/')]
#print(f'Links are {links} and hrefLinks are {hrefLink}')

def scrapeArticle(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	
	title = soup.find(id='firstHeading').text
	#print(title)
	text = soup.find(id='bodyContent').text
	
	links = soup.find(id='bodyContent').find_all('a')
	#print(links)
	scrapedLinks = [a for a in links if a['href'].startswith('/wiki/index.php')]
	if len(scrapedLinks)==0:
		print('no links scraped')
	else:
		randomLink = random.choice(scrapedLinks)
		scrapeArticle('https://aosd.slac.stanford.edu/' + randomLink['href'])
	
	
scrapeArticle('https://aosd.slac.stanford.edu/wiki/index.php/Category:ASO1')
#scrapeArticle('https://aosd.slac.stanford.edu/wiki/index.php/Gotchas')


