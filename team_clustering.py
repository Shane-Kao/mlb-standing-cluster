import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import euclidean_distances


def get_cluster(cluster_data):
    best_model = None
    best_sil_score = -np.inf
    for n_clusters in range(1, len(cluster_data) + 1):
        try:
            agglomerative_clustering = AgglomerativeClustering(
                linkage="average",
                n_clusters=n_clusters,
            )
            agglomerative_clustering.fit(cluster_data)
            sil_score = silhouette_score(
                X=euclidean_distances(cluster_data, cluster_data),
                labels=agglomerative_clustering.labels_,
            )
            if sil_score > best_sil_score:
                best_sil_score = sil_score
                best_model = agglomerative_clustering
        except:
            pass
    return best_model


if __name__ == "__main__":
    from get_standing import get_standing
    from itertools import groupby
    from operator import itemgetter

    data = get_standing()
    cluster_data = [[float(i['sport_games_back'])] if i['sport_games_back'] != '-' else [0] for i in data]

    best_model = get_cluster(cluster_data)
    # print(data)

    clustered_data = [dict(**j, **{"label": best_model.labels_[i]}) for i, j in enumerate(data)]
    clustered_data.sort(key=lambda d: d['label'])

    for key, value in groupby(clustered_data, key=itemgetter('label')):
        print(key, '&'.join([i['team_name'] for i in value]))
