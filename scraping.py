from urllib.request import urlopen
from bs4 import BeautifulSoup
import gzip
import io

def get_last_10_news():
    string = ""
    # This code is going to scrape some necessary information from Yahoo Finance.
    url = "https://finance.yahoo.com/topic/stock-market-news/"
    response = urlopen(url)

    # Check if the content is compressed with gzip
    if response.info().get('Content-Encoding') == 'gzip':
        # If gzip encoded, decompress the data
        buf = io.BytesIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        html = f.read().decode('utf-8')
    else:
        # Otherwise, read normally and decode
        html = response.read().decode('utf-8')

    soup = BeautifulSoup(html, "html.parser")

    # Now you can print or process the soup object
    #print(soup.prettify())

    # Find all <h3> elements
    h3_elements = soup.find_all('h3', class_ = "Mb(5px)")
    p = soup.find_all('p', class_ = "Fz(14px) Lh(19px) Fz(13px)--sm1024 Lh(17px)--sm1024 LineClamp(2,38px) LineClamp(2,34px)--sm1024 M(0)")

    # Loop through each <h3> element
    for index, h3 in enumerate(h3_elements):
        # Within each <h3>, find all <a> elements
        a_elements = h3.find_all('a')
        string = string + a_elements[0].contents[1] + "\n"
        string = string + p[index].contents[0] + "\n"
        string = string + "===========================================================" + "\n"

    return string


