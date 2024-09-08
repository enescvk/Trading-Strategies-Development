from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import io
import gzip

def get_last_10_news_headlines():
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


def get_last_10_links():
    url_list = []
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

    # Loop through each <h3> element
    for h3 in h3_elements:
        # Find the first <a> element within the <h3>
        a_element = h3.find('a')  # Use find() to get the first <a> tag, not find_all()
        
        # Check if an <a> element was found
        if a_element:
            # Extract the href attribute
            href = a_element.get('href')
            
            # Append the href to the url_list
            url_list.append(href)

    # Now url_list contains all the extracted URLs

    return url_list

def get_last_10_new_content(url_lst):
    url_dict = {}
    for url in url_lst:
        response = urlopen(url)

        # Check if the content is compressed with gzip
        if response.info().get('Content-Encoding') == 'gzip':
            buf = io.BytesIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            html = f.read().decode('utf-8')
        else:
            html = response.read().decode('utf-8')

        soup = BeautifulSoup(html, "html.parser")

        # Find the <div> element with the class "caas-body"
        div_elements = soup.find('div', class_="caas-body")
        
        if div_elements:
            # Find all <p> elements within the <div>
            p_elements = div_elements.find_all('p')
            
            # Extract text from each <p> element and concatenate into a single string
            ps_text = " ".join([p.get_text() for p in p_elements])
            
            # Store the extracted text in the url_dict
            url_dict[url] = ps_text

        else:
            print(f"No content found for {url}")

    return url_dict