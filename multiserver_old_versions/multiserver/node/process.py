from bs4 import BeautifulSoup
import requests

def process(task):
    def get_no_err(url, session):
        while True:
            try:
                page = session.get(url)
                if page.ok:
                    break
                else:
                    time.sleep(3)
            except:
                time.sleep(3)
        return page

    page = get_no_err(url, session)
    soup = BeautifulSoup(page.text)
    return [a.text for a in soup.find_all('a', {'class': 'title'})]

