import pandas as pd
from geopy.distance import great_circle
import random as rand
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def get_dist(point1, point2):
    try:
        distance = great_circle(point1, point2).kilometers
    except:
        print(point1, point2)
    return distance


locations = pd.read_excel('locations.xlsx', sheet_name='Sheet6')

points = []
for idx, row in locations.iterrows():
    lat = row['lat']
    lng = row['lng']
    loc = [lat, lng]
    points.append(loc)

def random_centroids(all_points, K):
    centroids = []
    for i in range(K):
        centroid = all_points[rand.randint(0, len(all_points) - 1)]
        centroids.append(centroid)
    return centroids


def assign_cluster(all_points, centroids):
    assignments = []

    for point in all_points:
        dist_point_clust = []

        for centroid in centroids:
            d_clust = get_dist(centroid, point)
            dist_point_clust.append(d_clust)

        assignment = np.argmin(dist_point_clust)
        assignments.append(assignment)

    return assignments

def new_centroids(all_points, centroids, assignments, K):
    new_centroids = []
    for i in range(K):
        pt_cluster = []
        for x in range(len(all_points)):
            if(assignments[x] == i):
                pt_cluster.append(all_points[x])

        mean_c = np.mean(pt_cluster, axis=0)
        new_centroids.append(mean_c)

    return new_centroids

def sse(all_vals, assignments, centroids):
    errors = []
    
    for i in range(len(all_vals)):
        #get assigned centroid for each point
        centroid = centroids[assignments[i]]
    
        #compute the distance (error) between one point and its closest centroid
        # error = np.linalg.norm(np.array(all_vals[i]) - np.array(centroid))
        error = get_dist(all_vals[i], centroid)
        
        #append squared error to the list of error
        errors.append(error**2)
        
    #and sum up all the errors
    sse = sum(errors)
    
    return sse


def kmeans_clustering(all_vals,K,max_iter = 100, tol = pow(10,-5) ):
    it = -1
    all_sse = []
    assignments = []
    
    #Place K centroids at random locations
    centroids = random_centroids(all_vals, K)
   
    #Until algorithm converges (needs two iterations before comparing the errors)
    while (len(all_sse)<=1 or (it < max_iter and all_sse[it] > 100)):
    # while (len(all_sse)<=1 or (it < max_iter and np.absolute(all_sse[it] - all_sse[it-1])/all_sse[it-1] >= tol)):
        it += 1
        #Assign all data points to the closest center
        assignments = assign_cluster(all_vals, centroids)
        
        #Compute the new centroids
        centroids = new_centroids(all_vals, centroids, assignments, K)
        
        #Compute SSE
        sse_kmeans = sse(all_vals, assignments, centroids)
        all_sse.append(sse_kmeans)        
        print(it)
        
     
    return (assignments, centroids, all_sse, it+1)



if __name__ == "__main__":
    assignments, centroids, all_sse, it =  kmeans_clustering(points, 3, max_iter=1000)

    print(all_sse)

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