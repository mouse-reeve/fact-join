''' tweets out fake facts '''
import json
import settings
import tweepy
from tweepy.error import TweepError
from mastodon import Mastodon

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

    twitter_auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_SECRET)
    twitter_auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
    twitter_api = tweepy.API(twitter_auth)

    mastodon_api = Mastodon(client_id=settings.MASTODON_CLIENT_ID,
                            client_secret=settings.MASTODON_CLIENT_SECRET,
                            access_token=settings.MASTODON_TOKEN,
                            api_base_url='https://botsin.space')

    try:
        twitter_api.verify_credentials()
    except TweepError:
        pass
    else:
        content = get_fact()
        try:
            twitter_api.update_status(status=content)
            mastodon_api.status_post(status=content)
        except TweepError as e:
            print 'Failed to tweet: "%s"' % content
            print 'error: %s' % e
