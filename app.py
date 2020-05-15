from flask import Flask
from flask import request
import requests
import SentinmentAnalysis
import json
app = Flask(__name__)


@app.route('/', methods=['POST'])
def run_twitter_analysis():
    query = json.loads(request.data)['query']
    twitter = SentinmentAnalysis.TwitterConnection()
    sentinment = SentinmentAnalysis.SentimentAnalysis()
    return sentinment.get_query_results(query=query,twitter=twitter)

@app.route('/matches/list', methods=['GET'])
def list_matches():
    URL = 'https://cricapi.com/api/matches?apikey=ybFGAvuP99aLszqmEhcc9wIu1Bg2'
    r = requests.get(url=URL)
    matches = r.json()['matches']
    obj={}
    arrays=[]
    for match in matches:
        obj = {'date':match['date'],'matchStarted':match['matchStarted'],'team-1':match['team-1'],'team-2':match['team-2'],'slugs':{'team-1':findSlug(match['team-1']),'team-2':findSlug(match['team-2'])}}
        arrays.append(obj)
    return {'matches':arrays}

def findSlug(wordString):
    words_array = wordString.split()
    if len(words_array)>1:
        slug=""
        for word in words_array:
            slug=slug+word[0]
    else:
        slug=wordString[0:3]
    return slug

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
