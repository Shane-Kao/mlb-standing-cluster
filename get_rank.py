from itertools import groupby
from operator import itemgetter

from scipy.stats import rankdata


def get_rank(standing_data, label):
    clustered_data = [dict(**j, **{"label": label[i]}) for i, j in enumerate(standing_data)]
    clustered_data.sort(key=lambda d: d['label'])
    avg_games_back = []
    for key, value in groupby(clustered_data, key=itemgetter('label')):
        sport_games_back = [float(i['sport_games_back']) if i['sport_games_back'] != '-' else 0 for i in value]
        avg_games_back.append(sum(sport_games_back)/len(sport_games_back))
    rank_ = rankdata(avg_games_back)
    clustered_data = [dict(**i, **{"rank": rank_[i['label']]}) for i in clustered_data]
    return clustered_data


if __name__ == "__main__":
    from get_standing import get_standing
    from team_clustering import get_cluster

    data = get_standing()
    cluster_data = [[float(i['sport_games_back'])] if i['sport_games_back'] != '-' else [0] for i in data]
    best_model = get_cluster(cluster_data)


    clustered_data = get_rank(standing_data=data, label=best_model.labels_)
    clustered_data.sort(key=lambda d: d['rank'])

    for key, value in groupby(clustered_data, key=itemgetter('rank')):
        print(key, [i['team_name'] for i in value])

