from sklearn.cluster import DBSCAN
import math


class Cluster:
    def __init__(self, vector_4d, distance, time, minimum_cluster):
        self.vector_4d = vector_4d
        self.distance = distance
        self.time = time
        self.minimum_cluster = minimum_cluster

    def custom_metric(self, q, p, space_eps, time_eps):
        dist = 0
        for i in range(2):
            dist += (q[i] - p[i]) ** 2
        spatial_dist = math.sqrt(dist)
        time_dist = math.sqrt((q[2] - p[2]) ** 2)
        return 1 if (time_dist / time_eps <= 1 and spatial_dist / space_eps <= 1 and p[3] != q[3]) else 2

    def cluster(self) -> str:
        ans = ''
        params = {"space_eps": self.distance, "time_eps": self.time}
        db = DBSCAN(eps=1, min_samples=self.minimum_cluster - 1, metric=self.custom_metric,
                    metric_params=params).fit_predict(self.vector_4d)
        unique_labels = set(db)
        total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) - 1
        ans += "Total clusters: {}\n".format(total_clusters)
        total_noise = list(db).count(-1)
        ans += "Total un-clustered: {}\n\n".format(total_noise)
        for k in unique_labels:
            if k != -1:
                labels_k = db == k
                cluster_k = self.vector_4d[labels_k]
                ans += "Cluster {} size: {}\n".format(k, len(cluster_k))
                for pt in cluster_k:
                    ans += "{}, {}, {}, {}\n".format(pt[0], pt[1], pt[2], pt[3])
                ans += '\n'
        return ans
