#Parser.py
from bs4 import BeautifulSoup
import requests
def parse():
    url = 'https://www.omgtu.ru/general_information/faculties/?ysclid=m7egu9b0g4810530086'
    page = requests.get(url)
    print(page.status_code)

    soup = BeautifulSoup(page.text, "html.parser")
    block = soup.find_all('div', class_='main__content')

    description = ''
    for data in block:
        uls = data.find_all('ul')
        for ul in uls:
            description += ul.text.strip() + '\n'

    with open("otvet.txt", "w", encoding="utf-8") as file:
        file.write(description)


if __name__ == '__main__':
    parse()