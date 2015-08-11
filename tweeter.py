''' tweets out fake facts '''
import json
import settings
import tweepy
from tweepy.error import TweepError

def get_fact():
    ''' pops a fact off the fact list '''
    fact = ''
    with open('facts.json', 'r+') as fact_file:
        facts = json.load(fact_file)
        fact = facts.pop()
        fact_file.seek(0)
        json.dump(facts, fact_file)
        fact_file.truncate()

    return fact

if __name__ == '__main__':

    auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
    api = tweepy.API(auth)

    for _ in range(0, 4):
        content = get_fact()
        try:
            api.update_status(status=content)
            break
        except TweepError as e:
            print 'Failed to tweet: "%s"' % content
            print 'error: %s' % e
