''' Combines sentences from wikipedia articles '''
from bs4 import BeautifulSoup
from nltk import word_tokenize
import requests
import re
import nltk


def get_page(page=None):
    ''' load and parse a wikipedia page '''
    if page:
        r = requests.get(page)
    else:
        r = requests.get('http://en.wikipedia.org/wiki/Special:Random')

    soup = BeautifulSoup(r.text)

    topic = soup.find('h1').text
    page_content = soup.find('div', {'id': 'mw-content-text'})
    paragraphs = page_content.findChildren('p')

    match = re.search(r'[can|may] refer to', paragraphs[0].text)
    if match and not page:
        return get_page()

    sentences = []
    for paragraph in paragraphs:
        paragraph = paragraph.text
        paragraph = re.sub(r'\[[0-9].?\]', '', paragraph)
        paragraph = re.sub(r'[\s]+', ' ', paragraph)
        paragraph = re.sub(r' \(.*\)', '', paragraph)
        sentences += paragraph.split('. ')

        for sentence in sentences:
            if sentence == '' or re.match(r'^\s$', sentence):
                sentences.remove(sentence)

            sentence = sentence.strip()

    return {'topic': topic, 'text': sentences}


primary_page = raw_input("name a wikipedia page: ")
secondary_page = raw_input("and another: ")

content = [get_page(primary_page), get_page(secondary_page)]

print content[0]['topic'] + ' + ' + content[1]['topic']

# add the first sentence of the primary article untouched.
fact = []

for i in range(10):
    if len(content[0]['text']) > i and len(content[1]['text']) > i:
        primary = content[0]['text'][i]
        secondary = content[1]['text'][i]
        primary_pos = nltk.pos_tag(word_tokenize(primary))
        secondary_pos = nltk.pos_tag(word_tokenize(secondary))

        joined_sentence = []
        if len(primary_pos) and len(secondary_pos):
            for word in primary_pos:
                if word[1][:2] == 'VB':
                    break
                else:
                    joined_sentence.append(word[0])

            isAddable = False
            for word in secondary_pos:
                if word[1][:2] == 'VB':
                    isAddable = True
                if isAddable:
                    joined_sentence.append(word[0])
            fact.append(' '.join(joined_sentence))

    else:
        break

result = '. \n'.join(fact) + '.'
result = re.sub(r' ,', ',', result)
result = re.sub(r' \'', '\'', result)

print result
print '\n\n'
