from datetime import datetime

import requests


def get_video():
    pass


def get_schedule(date):
    r = requests.get(
        url="https://bdfed.stitch.mlbinfra.com/bdfed/transform-mlb-scoreboard?stitch_env=prod&favoriteTeams=118&"
            "sortTemplate=4&sportId=1&startDate={}&endDate={}&gameType=E&&gameType=S&&gameType=R&&"
            "gameType=F&&gameType=D&&gameType=L&&gameType=W&&gameType=A&language=en&leagueId=104&&leagueId=103&"
            "contextTeamId=".format(date, date),
    )
    raw_data = r.json()

    return [{
        'away_team': i['teams']['away']['team']['name'],
        'home_team': i['teams']['home']['team']['name'],
        'recap': [k for k in [j for j in i['content']['media']['epgAlternate'] if
                  j['title'] == 'Daily Recap'][0]['items'][0]['playbacks'] if
                  k['name'] == 'highBit'][0]['url'],  # mp4Avc
        'condensed': [k for k in [j for j in i['content']['media']['epgAlternate'] if
                  j['title'] == 'Extended Highlights'][0]['items'][0]['playbacks'] if k['name'] == 'highBit'][0]['url'] if
        [j for j in i['content']['media']['epgAlternate'] if
                  j['title'] == 'Extended Highlights'][0]['items'] else None,
    } for i in raw_data['dates'][0]['games']]


if __name__ == '__main__':
    date = datetime.now().strftime(format="%Y-%m-%d")
    data = get_schedule(date)
    for i in data:
        print(i)