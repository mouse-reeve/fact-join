''' Combines sentences from wikipedia articles '''
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize
import re
import requests
import sys


def get_page(page=None):
    ''' load and parse a wikipedia page '''
    if page:
        r = requests.get(page)
    else:
        r = requests.get('http://en.wikipedia.org/wiki/Special:Random')

    soup = BeautifulSoup(r.text)

    page_topic = soup.find('h1').text
    page_content = soup.find('div', {'id': 'mw-content-text'})
    paragraphs = page_content.findChildren('p')

    # skip lists
    if (page_topic.startswith('List ') or page_topic.startswith('Lists ')) and not page:
        return get_page()

    # skip disambiguation pages
    match = re.search(r'[can|may] refer to', paragraphs[0].text)
    if match and not page:
        return get_page()

    sentences = []
    for paragraph in paragraphs:
        paragraph = paragraph.text
        # remove citation footnotes: [1]
        paragraph = re.sub(r'\[[0-9].?\]', '', paragraph)

        paragraph = re.sub(r'[\s]+', ' ', paragraph)

        # remove parentheticals: (whateva)
        paragraph = re.sub(r' \(.*\)', '', paragraph)
        sentences += paragraph.split('. ')

        for sentence in sentences:
            if sentence == '' or re.match(r'^\s$', sentence):
                sentences.remove(sentence)

            sentence = sentence.strip()

    return {'topic': page_topic, 'text': sentences}


def pos_tag(sentences):
    ''' uses nltk to tag part of speech for each sentence '''
    tagged = []
    for sentence in sentences:
        tags = nltk.pos_tag(word_tokenize(sentence))

        # throw out sentenes with no verb
        verbs = [word for word in tags if word[1].startswith('VB')]
        if len(verbs):
            tagged.append(tags)
    return tagged

def merge_sentences(primary, secondary):
    ''' combines two pos tagged sentences '''
    joined_sentence = []
    for word in primary:
        if word[1][:2] == 'VB':
            break
        else:
            joined_sentence.append(word[0])

    isAddable = False
    for word in secondary:
        if word[1][:2] == 'VB':
            isAddable = True
        if isAddable:
            joined_sentence.append(word[0])
    return ' '.join(joined_sentence)


if __name__ == '__main__':
    primary_page = 'http://en.wikipedia.org/wiki/%s' % sys.argv[1] if len(sys.argv) >= 2 else \
                   'http://en.wikipedia.org/wiki/Special:Random'
    secondary_page = 'http://en.wikipedia.org/wiki/%s' % sys.argv[2] if len(sys.argv) >= 3 else \
                     'http://en.wikipedia.org/wiki/Special:Random'

    content = [get_page(primary_page), get_page(secondary_page)]
    for item in content:
        item['tagged'] = pos_tag(item['text'][:20])

    facts = []
    while len(content[0]['tagged']) and len(content[1]['tagged']):
        facts.append(merge_sentences(content[0]['tagged'].pop(0), content[1]['tagged'].pop(0)))

    # display the results
    print '%s + %s' % (content[0]['topic'], content[1]['topic'])

    for fact in facts:
        fact = re.sub(r' \.', '.', fact)
        fact = re.sub(r' ,', ',', fact)
        fact = re.sub(r' \'', '\'', fact)
        fact = re.sub(r'`` ', '\"', fact)
        fact = re.sub(r'\'\'', '\"', fact)

        topic = content[0]['topic']
        hashtag = topic.split(' ')
        hashtag = '#%s' % ''.join(hashtag)

        if topic in fact:
            fact = re.sub(topic, hashtag, fact)

        print fact

