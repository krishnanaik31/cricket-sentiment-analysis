import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plot


class TwitterConnection(object):
    def __init__(self):
        consumer_key = 'l199RQVXCaYPZki5aErm5pPIc'
        consumer_secret_key = 'cU24ZP4tioeeLT5WiHYg5iv8f5boFFCc2lfUq5vZu4Xh8u1AtI'
        access_token = '3316225315-V1ZmShhO2KRa0xjSQoCXz3NbNU8VRYo4brQiMAz'
        access_secret_key = 'q5DEY31DxDVQRIT3GOCDc19e9Ba3Ae904r6RAHL19fxAZ'
        self.twitter = OAuthHandler(consumer_key, consumer_secret_key)
        self.twitter.set_access_token(access_token, access_secret_key)
        self.client = tweepy.API(self.twitter)

    def get_sentiment(self, tweet):
        blob = TextBlob(tweet.text)
        if blob.sentiment.polarity > 0.00:
            return 'positive'
        else:
            return 'negative'

    def get_tweets(self, query_word, count=1000):
        tweets_list = []
        fetched_tweets = self.client.search(q=query_word, count=count)
        for tweet in fetched_tweets:
            if tweet.retweeted == False:
                parsed_tweets = {'text': tweet.text, 'sentiment': self.get_sentiment(tweet), 'location':tweet.user.location}
                if tweet.retweet_count > 0:
                    if parsed_tweets not in tweets_list:
                        tweets_list.append(parsed_tweets)
        return tweets_list

class SentimentAnalysis(object):
    def get_query_results(self, query, twitter,count=2000000):
        # file=open("tweet.txt","w")
        tweets = twitter.get_tweets(query, count)
        # file.write(tweets)
        # file.close()
        # print(tweets)
        positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        positive_percentage = 100 * len(positive_tweets) / len(tweets)
        negative_percentage = 100 * len(negative_tweets) / len(tweets)
        print("Positive tweets percentage: {} %".format(positive_percentage))
        print("Negative tweets percentage: {} %".format(negative_percentage))
        result = {'positive': positive_tweets, 'negative': negative_tweets,
                  'percentage': {'positive': positive_percentage,
                                 'negative': negative_percentage}}
        return result


    def main(self):
        twitter = TwitterConnection()
        query = input("Enter the Query you want to search for??? ")
        query_results = self.get_query_results(query=query, twitter=twitter)
        labels = ['Positive Tweets', 'Negative Tweets']
        sizes = [query_results['percentage']['positive'], query_results['percentage']['negative']]
        color = ['green', 'red']
        patches, texts = plot.pie(sizes, colors=color, shadow=True, startangle=90)
        plot.legend(patches, labels, loc="best")
        plot.axis('equal')
        plot.tight_layout()
        plot.show()


if __name__ == '__main__':
    sentinment = SentimentAnalysis()
    sentinment.main()
