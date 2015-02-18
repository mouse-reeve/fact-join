from bs4 import BeautifulSoup
from nltk import word_tokenize
import requests
import re
import nltk


def get_page(page=None):
    if page:
        r = requests.get(page)
    else:
        r = requests.get('http://en.wikipedia.org/wiki/Special:Random')

    soup = BeautifulSoup(r.text)

    topic = soup.find('h1').text
    content = soup.find('div', {'id': 'mw-content-text'})
    paragraphs = content.findChildren('p')

    match = re.search(r'[can|may] refer to', paragraphs[0].text)
    if match and not page:
        return get_page()

    sentences = []
    for paragraph in paragraphs:
        paragraph = paragraph.text
        paragraph = re.sub(r'\[[0-9].?\]', '', paragraph)
        paragraph = re.sub(r'[\s]+', ' ', paragraph)
        sentences += paragraph.split('. ')

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence == '':
                sentences.remove(sentence)

    return {'topic': topic, 'text': sentences}


primary_page = raw_input("name a wikipedia page: ")
secondary_page = raw_input("and another: ")

content = [get_page(primary_page), get_page(secondary_page)]

print content[0]['topic'] + ' + ' + content[1]['topic']

# add the first sentence of the primary article untouched.
fact = []#[content[0]['text'][0]]

for i in range(10):
    if len(content[0]['text']) > i and len(content[1]['text']) > i:
        primary = content[0]['text'][i]
        secondary = content[1]['text'][i]
        primary_pos = nltk.pos_tag(word_tokenize(primary))
        secondary_pos = nltk.pos_tag(word_tokenize(secondary))

        sentence = []
        if len(primary_pos) and len(secondary_pos):
            for word in primary_pos:
                if word[1][:2] == 'VB':
                    break
                else:
                    sentence.append(word[0])

            isAddable = False
            for word in secondary_pos:
                if word[1][:2] == 'VB':
                    isAddable = True
                if isAddable:
                    sentence.append(word[0])
            fact.append(' '.join(sentence))

    else:
        break

result = '. \n'.join(fact) + '.'
result = re.sub(r' ,', ',', result)
result = re.sub(r' \'', '\'', result)

print result
print '\n\n'
