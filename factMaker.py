from bs4 import BeautifulSoup
import requests
import re


def get_page():
    r = requests.get('http://en.wikipedia.org/wiki/Special:Random')

    soup = BeautifulSoup(r.text)

    topic = soup.find('h1').text
    content = soup.find('div', {'id': 'mw-content-text'})
    paragraphs = content.findChildren('p')

    sentences = []

    for paragraph in paragraphs:
        paragraph = paragraph.text
        paragraph = re.sub(r'\[[0-9].?\]', ' ', paragraph)
        paragraph = re.sub(r'\n', '', paragraph)
        sentences += paragraph.split('. ')

    return {'topic': topic, 'text': sentences}


content = []
for i in range(2):
    content.append(get_page())

print content[0]['topic'] + ' + ' + content[1]['topic']

fact = [content[0]['text'][0]]

i = 0
for i in range(1, 10):
    if len(content[0]['text']) > i and len(content[1]['text']) > i:
        fact.append(content[1]['text'][i])
        fact.append(content[0]['text'][i])
    else:
        break

result = '. \n'.join(fact) + '.'

print result
