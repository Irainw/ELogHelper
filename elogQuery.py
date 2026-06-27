import requests
import pandas as pd
import re

class ELogQuery:
    """
    A class to query and process ELog data.
    """

    def __init__(self, params: dict, url: str = 'https://mccelog.slac.stanford.edu/elog/wbin/elog_display_json.php'):
        """
        Initialize the ELogQuery with parameters and URL.

        Args:
            params (dict): The parameters for the GET request.
            url (str): The URL to send the GET request to.
        """
        self.params = params
        self.url = url

    def isTableText(self, text: str) -> bool:
        """
        Check if the given text contains table-like data.

        Args:
            text (str): The text to check.
        returns:
            bool: True if the text appears to be a table, otherwise False.
        """
        if not isinstance(text, str):
            return False
        patterns = [ 
            r'<table\b',                # HTML table
            r'\n\s*\|',                 # markdown table rows
            r'^\s*\|.*\|\s*$',          # single markdown table line
            r'\n\s*-{2,}\s*\n',         # separator lines
            r'\t',                      # tab-separated table-like text
        ]

        return any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in patterns)
    
    def removePictureText(self, text: str) -> str:
        """
        Remove image-related content from a string.

        Args:
            text (str): The text to clean.
        Returns:
            str: The cleaned text with picture references removed.
        """
        if not isinstance(text, str):
            return ""
        
        cleanedText = re.sub(r'<\s*img\b[^>]*>', '', text, flags=re.IGNORECASE)
        cleanedText = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', cleanedText)
        cleanedText = re.sub(r'<\s*figure\b[^>]*>.*?<\s*/\s*figure\s*>', '', cleanedText, flags=re.IGNORECASE | re.DOTALL)
        cleanedText = re.sub(r'<\s*p\b[^>]*>', '', cleanedText, flags=re.IGNORECASE)
        cleanedText = re.sub(r'<\s*/\s*p\s*>', '', cleanedText, flags=re.IGNORECASE)
        cleanedText = re.sub(r'https?://\S+\.(?:png|jpe?g|gif|svg|webp)\S*', '', cleanedText, flags=re.IGNORECASE)
        cleanedText = re.sub(r'\b(?:https?:\/\/)?(?:www\.)?[^\/\s]+\.(?:png|jpe?g|gif|svg|webp)\b', '', cleanedText, flags=re.IGNORECASE)

        return cleanedText.strip()
    
    def removeNewLines(self, text: str) -> str:
        """
        Remove newline characters from a string.

        Args:
            text (str): The text to clean.
        Returns:
            str: The cleaned text with newline characters removed.
        """
        if not isinstance(text, str):
            return ""
        
        cleanedText = text.replace('\n', ' ').replace('\r', ' ')
        cleanedText = re.sub(r'\s+', ' ', cleanedText)  # Replace multiple spaces with a single space

        return cleanedText.strip()
    
    def extractTitleText(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a DataFrame containing only the title and text columns,
        excluding rows where text appears to be a table.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
        Returns:
            pd.DataFrame: A new DataFrame with only title and text columns.
        """
        result = df.loc[:, ['title', 'text']].copy()
        result['title'] = result['title'].fillna('').astype(str).apply(self.removePictureText)
        result['text'] = result['text'].fillna('').astype(str).apply(self.removeNewLines)
        result['text'] = result['text'].fillna('').astype(str).apply(self.removePictureText)
        mask = result['text'].apply(lambda x: not self.isTableText(x))
        return result.loc[mask, ['title', 'text']].reset_index(drop=True)

    def requestElog(self) -> pd.DataFrame:
        """
        Request ELog data from the specified URL with given parameters.

        Returns:
            pd.DataFrame: A DataFrame containing the cleaned title and text data.
        """
        r = requests.get(self.url, params=self.params)
        data = r.json()
        return data

    def cleanElogData(self, data: list) -> pd.DataFrame:
        """
        Clean the ELog data by extracting title and text, removing picture references and newlines.

        Args:
            data (list): The raw ELog data.
        """
        df = pd.DataFrame(data)
        cleanedDF = self.extractTitleText(df)
        return cleanedDF
