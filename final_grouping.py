from clustering import kmeans_clustering
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

locations = pd.read_excel('locations.xlsx', sheet_name='Sheet6')
locations['cluster'] = -1
points = []
for idx, row in locations.iterrows():
    lat = row['lat']
    lng = row['lng']
    loc = [lat, lng]
    points.append(loc)

assignments, centroids, all_sse, it =  kmeans_clustering(points, 3, max_iter=1000)

for i in range(len(points)):
    assignment = int(assignments[i])
    locations.at[i, 'cluster'] = assignment

# print(locations)

store_df = pd.read_excel('locations.xlsx', sheet_name='Sheet5')
loc_df = locations[['location', 'cluster']]

store_df = pd.merge(store_df, loc_df, left_on='store', right_on='location', how='left')
store_df = store_df.rename(columns={'cluster': 'store-cluster'})
store_df = store_df.drop(columns=['location'])
store_df = pd.merge(store_df, loc_df, left_on='accomodation', right_on='location', how='left')
store_df = store_df.rename(columns={'cluster': 'accomodation-cluster'})
store_df = store_df.drop(columns=['location'])


print(store_df)
store_df.to_csv('store_assignment.csv', index=False)


for i in range(len(points)):
    x = points[i][0]
    y = points[i][1]

    if assignments[i] == np.int64(2):
        plt.scatter(x, y, color='green', marker='o')
    elif assignments[i] == np.int64(1):
        plt.scatter(x, y, color='red', marker='o')
    else:
        plt.scatter(x, y, color='blue', marker='s')

plt.scatter(centroids[0][0], centroids[0][1], color='blue', marker='^')
plt.scatter(centroids[1][0], centroids[1][1], color='red', marker='^')
plt.scatter(centroids[2][0], centroids[2][1], color='green', marker='^')

plt.show()