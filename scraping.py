from urllib.request import urlopen
from bs4 import BeautifulSoup
import io
import gzip
import requests
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

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


###########################################################################


def get_last_10_links():
    url_list = []
    base_url = "https://finance.yahoo.com"
    url = "https://finance.yahoo.com/topic/stock-market-news/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if not a 200 status
        html = response.text

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Find all <h3> elements with class 'Mb(5px)' (news titles)
        h3_elements = soup.find_all('h3', class_='Mb(5px)')

        # Extract and construct full URLs
        for h3 in h3_elements:
            a_element = h3.find('a')
            if a_element:
                href = a_element.get('href')
                full_url = href if href.startswith('http') else base_url + href
                url_list.append(full_url)

        return url_list[:10]

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return []
    

###########################################################################

def get_last_10_new_content(url_lst):
    url_dict = {}
    for url in url_lst:
        # Initialize Safari WebDriver
        driver = webdriver.Safari()
        driver.get(url)

        # Optional: Wait for elements to load, adjust the time based on page loading speed
        driver.implicitly_wait(5)  # Wait for 5 seconds for elements to load

        # Find all <div> elements with the class "body yf-5ef8bf"
        div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.body.yf-5ef8bf')

        # Iterate over each <div> element found
        for div in div_elements:
            # Inside each <div>, find all <p> elements with the class "yf-1pe5jgt"
            p_elements = div.find_elements(By.CSS_SELECTOR, 'p.yf-1pe5jgt')
            
            # Extract text from each <p> element and concatenate into a single string
            ps_text = " ".join([p.text for p in p_elements])

        # Close the browser once done
        driver.quit()

        url_dict[url] = ps_text

    return url_dict
