import re
import json

from datetime import datetime, timedelta

import requests


def get_schedule(date):
    r = requests.get(
        url="https://bdfed.stitch.mlbinfra.com/bdfed/transform-mlb-scoreboard?stitch_env=prod&favoriteTeams=118&"
            "sortTemplate=4&sportId=1&startDate={}&endDate={}&gameType=E&&gameType=S&&gameType=R&&"
            "gameType=F&&gameType=D&&gameType=L&&gameType=W&&gameType=A&language=en&leagueId=104&&leagueId=103&"
            "contextTeamId=".format(date, date),
    )
    raw_data = r.json()
    print(r.url)
    return [{
        'away_team': i['teams']['away']['team']['name'],
        'home_team': i['teams']['home']['team']['name'],
        'media': [i for i in re.findall(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            json.dumps(i['content'].get('media', ''))
        ) if i.endswith('16000K.mp4')]
    } for i in raw_data['dates'][0]['games']]


if __name__ == '__main__':
    date = (datetime.now() - timedelta(days=1)).strftime(format="%Y-%m-%d")
    data = get_schedule(date)
    for i in data:
        print(i['media'])
