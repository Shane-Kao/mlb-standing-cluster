from itertools import groupby
from operator import itemgetter
from datetime import datetime, timedelta

from get_standing import get_standing
from team_clustering import get_cluster
from get_rank import get_rank
from get_schedule import get_schedule


data = get_standing()
cluster_data = [[float(i['sport_games_back'])] if i['sport_games_back'] != '-' else [0] for i in data]
best_model = get_cluster(cluster_data)

clustered_data = get_rank(standing_data=data, label=best_model.labels_)
clustered_data.sort(key=lambda d: d['rank'])


rank_dict = {}
for key, value in groupby(clustered_data, key=itemgetter('rank')):
    rank_dict = dict(**rank_dict, **{i['team_name']: key for i in value})

date = (datetime.now() - timedelta(days=1)).strftime(format="%Y-%m-%d")
schedule = get_schedule(date)

schedule = [dict(score=rank_dict[i['away_team']] + rank_dict[i['home_team']], **i) for i in schedule]

for i in sorted(schedule, key=lambda x: x['score']):
    print(i)