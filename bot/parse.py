import requests
from bs4 import BeautifulSoup

import database
import structure


def get_programs(url):
    response_text = requests.get(url).text
    soup = BeautifulSoup(response_text, "html.parser")
    print(f'[+] Выполняю {url} : ', end='')
    all_html = [i for i in soup.findAll('article', {'class': 'post-news'}) if 'закрыта' not in str(i)]
    print('Выполнено')
    return [(i.find('a')['href'],
             i.find('div', {'class': 'offset-top-20'}).text.split('b>')[-1].replace('\n', '').replace('Предмет: ', ''),
             i.find('img')['src'].replace(' ', '').replace('\n', ''),
             i.find('div', {'class': 'offset-top-10'}).text.replace('\nКлассы: ', '')[:-1]) for i
            in all_html]


def get_info(data):
    url, subject, image, klass = data
    if subject in structure.iss_keys:
        subject = structure.iss_keys[subject]
    response_text = requests.get(url).text
    soup = BeautifulSoup(response_text, "html.parser")
    if not 'программа' in str(soup):
        return []
    print(f'[+] Выполняю {url} : ', end='')
    register = soup.find('div', {'id': 'tabs-n-1'}).findAll('p')[-1].find('b').text[3:].split()
    temp_reg = register[1]
    if len(temp_reg) == 1:
        temp_reg = '0' + temp_reg
    register = register[0] + ' ' + temp_reg + structure.mouth[f' {register[2]} '] + register[3]
    temp = {'url': url,
            'subject': subject,
            'title': soup.find('div', {'class': 'container'}).find('h3').text.replace('\n', ''),
            'class': klass,
            'dates': soup.find('div', {'id': 'tabs-n-1'}).find('p').find('strong').text,
            'register': register,
            'image': image}
    try:
        temp['place'] = soup.find('div', {'id': 'tabs-n-1'}).find('p').findAll('b')[-1].text
    except:
        try:
            temp['place'] = soup.find('div', {'id': 'tabs-n-1'}).find('p').findAll('strong')[1].text
        except:
            temp['place'] = soup.find('div', {'id': 'tabs-n-1'}).find('p').findAll('strong')[0].text.split('на базе ')[
                -1]
    # print(temp['register'])
    print('Готово')
    return temp


def main():
    programs = []
    info = []
    sent = database.get_urls()
    new = []
    main_urls = ['https://reg.olympmo.ru/direction/science?page=1',
                 'https://reg.olympmo.ru/direction/science?page=2',
                 'https://reg.olympmo.ru/direction/science?page=3',
                 'https://reg.olympmo.ru/direction/art?page=1',
                 'https://reg.olympmo.ru/direction/art?page=2',
                 'https://reg.olympmo.ru/direction/art?page=3',
                 'https://reg.olympmo.ru/direction/sport?page=1',
                 'https://reg.olympmo.ru/direction/sport?page=2',
                 'https://reg.olympmo.ru/direction/sport?page=3']
    print('--Начало выполнения--')
    print('Получение всех программ')

    for url in main_urls:
        temp = get_programs(url)
        programs += [i for i in temp if not i[0] in sent]
        new += [i[0] for i in temp if not i[0] in sent]
    if programs:
        print('Получение информации о программах')
    for data in programs:

        temp = get_info(data)
        if temp:
            info.append(temp)
    database.new_urls(new)
    return info


if __name__ == "__main__":
    for i in main():
        print(f"'{i['register']}',")
