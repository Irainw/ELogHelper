import requests
from bs4 import BeautifulSoup
import random


class WikiScraper:
    def __init__(self, base_url: str = "https://aosd.slac.stanford.edu/wiki/index.php/"):
        self.base_url = base_url
        
    def request(self, url: str):
        '''
        Make a GET request to the specified URL and return the response content.
        Arguments:
            url (str): The URL to send the GET request to.
            Returns:
                The content of the response if the request is successful, otherwise None.'''
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return None
        
    def soup(self, url:str):
            '''
            Creates a BeautifulSoup object from content of specified URL.
            Arguments:
                url (str): The URL to send a GET request to.
            Returns:
                A BeautifulSoup object if the request is successful, otherwise None.'''
            content = self.request(url)
            if content:
                return (BeautifulSoup(content, 'html.parser'))
            else:
                print(f"Failed to make soup for {url}.")
                return None

    def findLinks(self, url:str):
        '''
        Finds all links in the body content of the specified URL.
        Arguments:
            url (str): The URL to send a GET request to.
        Returns:
            A list of links found in the body content of the page.'''
        
        soup = self.soup(url)
        if not soup:
            print(f"Failed to find links for {url}.")
            return []
        links = soup.find(id = 'bodyContent').find_all('a')
        scrapedLinks = [a for a in links if a['href'].startswith('/wiki/index.php')]
        return scrapedLinks

    def articleData(self, url: str):
        '''
        Fetches an article page and returns its title, body text, and soup object.
        Arguments:
            url (str): The URL to send a GET request to.
        Returns:
            A tuple of (title, text, soup) if the page is parsed successfully, otherwise (None, None, None).'''
        soup = self.soup(url)
        if not soup:
            print(f"Failed to parse article data for {url}.")
            return None, None, None

        titleNode = soup.find(id='firstHeading')
        bodyNode = soup.find(id='bodyContent')
        if not titleNode or not bodyNode:
            print(f"Could not find article content for {url}.")
            return None, None, None

        title = titleNode.get_text(strip=True)
        text = bodyNode.get_text(" ", strip=True)
        return title, text, soup

    def cleanText(self, text: str) -> str:
        '''
        Cleans the text by removing image references and other unwanted content.
        Arguments:
            text (str): The text to clean.
        Returns:
            The cleaned text.'''
        # Remove images, tables but preserve text, and links from the text  
    
    def recursiveScrapeArticle(self, url: str):
        '''
        Scrapes an article from the specified URL, extracts its title and text, and recursively scrapes a random linked article.
        Arguments:
            url (str): The URL of the article to scrape.
        Returns:
            None. This function prints the title and text of the article and continues scraping linked articles recursively.'''
        title, text, soup = self.articleData(url)
        if not soup:
            print(f"Failed to scrape article for {url}.")
            return
        
        scrapedLinks = self.findLinks(url)
        
        if len(scrapedLinks) == 0:
            print('No links scraped')
        else:
            random_link = random.choice(scrapedLinks)
            self.recursiveScrapeArticle(self.base_url + random_link['href'])