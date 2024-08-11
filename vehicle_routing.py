import pandas as pd
from aco import ant_colony

store_assignment = pd.read_csv('store_assignment.csv')

store_assignment['key'] = store_assignment['store'] + "-" + store_assignment['accomodation']

num_vehicles = 3

transportation = pd.read_excel('locations.xlsx', sheet_name='Sheet4')
transportation['key'] = transportation['From'] + "-" + transportation['To']

for i in range(num_vehicles):
    store_ass_vehicle = store_assignment[store_assignment['store-cluster'] == i]
    store_ass_vehicle['temp'] = 1
    store_ass_vehicle = store_ass_vehicle.drop(columns=['store', 'accomodation', 'store-cluster', 'accomodation-cluster'])

    transportation_vehicle = pd.merge(transportation, store_ass_vehicle, on='key', how='left')
    transportation_vehicle = transportation_vehicle[transportation_vehicle['temp'] == 1]
    transportation_vehicle = transportation_vehicle.reset_index()
    # print(transportation_vehicle)
    temp_nodes = []

    lat = 0
    lng = 0
    rows = transportation_vehicle.shape[0]
    for index, row in transportation_vehicle.iterrows():
        from_lat = row['from-lat']
        from_lng = row['from-lng']
        to_lat = row['to-lat']
        to_lng = row['to-lng']

        lat += from_lat
        lat += to_lat

        lng += from_lng
        lng += to_lng

        p1 = [from_lat, from_lng]
        p2 = [to_lat, to_lng]
        temp_nodes.append(p1)
        temp_nodes.append(p2)

    lat /= 2*rows
    lng /= 2*rows
    print(lat, lng)

    nodes = [[lat, lng]]
    nodes.extend(temp_nodes)

    ant_colony(nodes, n_ants=10, n_iterations=100, alpha=1, beta=1, evaporation_rate=0.5, Q=1)