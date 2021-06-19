from datetime import datetime

import requests


def get_standing():
    r = requests.get(
        url="https://statsapi.mlb.com/api/v1/standings",
        params={
            "leagueId": "103,104",
            "season": datetime.now().year,
            "standingsTypes": "regularSeason",
        }
    )
    raw_data = r.json()
    records = raw_data["records"]
    team_records = sum([i["teamRecords"] for i in records], [])
    standing = [{
        "team_id": i["team"]["id"],
        "team_name": i["team"]["name"],
        "sport_games_back": i["sportGamesBack"],
    } for i in team_records]
    return standing


if __name__ == "__main__":
    data = get_standing()
    for i in data:
        print(i)