import requests
import pandas as pd
import re

def isTableText(text: str) -> bool:
    """
    Check if the given text contains table-like data.

    Args:
        text (str): The text to check.

    Returns:
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


def removePictureText(text: str) -> str:
    """
    Remove image-related content from a string.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text with picture references removed.
    """
    if not isinstance(text, str):
        return ""

    cleaned_text = re.sub(r'<\s*img\b[^>]*>', '', text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', cleaned_text)
    cleaned_text = re.sub(r'<\s*figure\b[^>]*>.*?<\s*/\s*figure\s*>', '', cleaned_text, flags=re.IGNORECASE | re.DOTALL)
    cleaned_text = re.sub(r'<\s*p\b[^>]*>', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'<\s*/\s*p\s*>', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'https?://\S+\.(?:png|jpe?g|gif|svg|webp)\S*', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'\b(?:https?:\/\/)?(?:www\.)?[^\/\s]+\.(?:png|jpe?g|gif|svg|webp)\b', '', cleaned_text, flags=re.IGNORECASE)

    return cleaned_text.strip()

def removeNewLines(text: str) -> str:
    """
    Remove newline characters from a string.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text with newline characters removed.
    """
    if not isinstance(text, str):
        return ""

    cleaned_text = text.replace('\n', ' ').replace('\r', ' ')
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Replace multiple spaces with a single space

    return cleaned_text.strip()

def extractTitleText(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a DataFrame containing only the title and text columns,
    excluding rows where text appears to be a table.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.

    Returns:
        pd.DataFrame: A new DataFrame with only title and text columns.
    """
    result = df.loc[:, ['title', 'text']].copy()
    result['title'] = result['title'].fillna('').astype(str).apply(removePictureText)
    result['text'] = result['text'].fillna('').astype(str).apply(removeNewLines)
    result['text'] = result['text'].fillna('').astype(str).apply(removePictureText)
    mask = result['text'].apply(lambda x: not isTableText(x))
    return result.loc[mask, ['title', 'text']].reset_index(drop=True)

params = {
        'limit': '100',
        'after': '1',
        'logbook': 'SPEAR3'
}

r = requests.get('https://mccelog.slac.stanford.edu/elog/wbin/elog_display_json.php', params=params)

data = r.json()
df = pd.DataFrame(data)
cleanedDF = extractTitleText(df)

print(cleanedDF)