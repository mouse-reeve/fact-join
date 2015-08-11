''' tweets out fake facts '''
import json
import settings
import tweepy

if __name__ == '__main__':
    fact = ''
    with open('facts.json', 'r+') as fact_file:
        facts = json.load(fact_file)
        fact = facts.pop()
        fact_file.seek(0)
        json.dump(facts, fact_file)
        fact_file.truncate()
    print fact
