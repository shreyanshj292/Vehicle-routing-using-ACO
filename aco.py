from geopy.distance import great_circle
import numpy as np
import matplotlib.pyplot as plt


def get_dist(point1, point2):
    try:
        distance = great_circle(point1, point2).kilometers
    except:
        print(point1, point2)
    if distance == 0:
        # return np.nextafter(0, 1)
        return 1e-10
    return distance

def get_unvisited(visited):
    unvisited = []
    for i in range(0, len(visited), 2):
        if visited[i] == True:
            # unvisited.append(False)
            pass
        else:
            # unvisited.append(True)
            unvisited.append(i)

        if visited[i+1] == True:
            # unvisited.append(False)
            pass
        else:
            if visited[i] == True:
                # unvisited.append(True) ## If from location not visited, then only true
                unvisited.append(i)
            else:
                # unvisited.append(False)
                pass

    return np.array(unvisited)


        
def ant_colony(points, n_ants, n_iterations, alpha,beta, evaporation_rate, Q):

    n_points = len(points)
    # print(points)
    pheromone = np.ones((n_points, n_points))

    best_path = None
    best_path_length = np.inf

    for iteration in range(n_iterations):
        paths = []
        path_lengths = []

        for ant in range(n_ants):
            visited = [False] * n_points
            current_point = np.random.randint(n_points)
            visited [current_point] = True

            path = [current_point]
            path_length = 0

            while False in visited:
                # unvisited = get_unvisited(visited)
                unvisited = np.where(np.logical_not(visited))[0]
                # print(len(visited), len(unvisited))
                # print(unvisited)

                probabilities = np.zeros(len(unvisited))
                for i, unvisited_point in enumerate(unvisited):
                    probabilities[i] = pheromone[current_point, unvisited_point] ** alpha / get_dist(points[current_point], points[unvisited_point])**beta
                
                probabilities /= np.sum(probabilities)
                # print(probabilities)

                next_point = np.random.choice(unvisited, p=probabilities)
                path.append(next_point)

                path_length += get_dist(points[current_point], points[next_point])

                visited[next_point] = True
                current_point = next_point

            paths.append(path)
            path_lengths.append(path_length)

            if path_length < best_path_length:
                best_path_length = path_length
                best_path = path

        pheromone += evaporation_rate

        for path, path_length in zip(paths, path_lengths):
            for i in range(n_points - 1):
                pheromone[path[i], path[i+1]] += Q/path_length
            pheromone[path[-1], path[0]] += Q/path_length

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    # ax = fig.add_subplot(111, projection='3d')
    points = np.array(points)
    ax.scatter(points[1:,0], points[1:,1], c='r', marker='o')
    # ax.scatter(points[1,0], points[1,1], c='g', marker='o')
    
    for i in range(1, n_points-1):
        ax.plot([points[best_path[i],0], points[best_path[i+1],0]],
                [points[best_path[i],1], points[best_path[i+1],1]],
                c='g', linestyle='-', linewidth=2, marker='o')
        
    ax.plot([points[best_path[0],0], points[best_path[-1],0]],
            [points[best_path[0],1], points[best_path[-1],1]],
            c='g', linestyle='-', linewidth=2, marker='o')
    

    ax.scatter(points[0,0], points[0,1], c='r', marker='^')
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    plt.show()
    

if __name__ == "__main__":
    # Example usage:
    points = np.random.rand(10, 2) # Generate 10 random 3D points
    print(points)


    for i in range(4):
        ant_colony(points, n_ants=10, n_iterations=100, alpha=1, beta=1, evaporation_rate=0.5, Q=1)




