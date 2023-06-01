import json
import networkx as nx
from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def get_clusters(path='data/interactions.json'):

    with open(path) as f:
        interactions = json.load(f)
    graph = nx.Graph()
    token_a_users = set()

    for interaction in interactions['interactions']:
        user0 = interaction['user0']
        user1 = interaction['user1']
        asset_type = interaction['asset']
        time = interaction['timestamp']

        graph.add_edge(user0, user1, asset_type=asset_type, time=time)

        if asset_type == 'A' and time > 16000000:
            # C: user0 sending token A is always the same user in this example, we don't want to connect this user
            # token_a_users.add(user0)
            token_a_users.add(user1)

    # Step 3: Extract features
    node_features = {}
    edge_features = {}

    # C: Runtime O(n)
    for node in graph.nodes:
        node_features[node] = {
            'num_interactions': len(graph.edges(node)),
            'has_token_A': int(node in token_a_users)
        }

    # C: Runtime O((N / 10) * N)
    # C: Better to do this during the initial for loop
    for edge in graph.edges:
        edge_features[edge] = {
            'asset_type': graph.edges[edge]['asset_type'],
            'time': graph.edges[edge]['time']
        }

    # Step 4: Prepare training data
    X_node = []
    X_edge = []
    y = []

    # C: Another loop through nodes and edges
    for node in graph.nodes:
        X_node.append(list(node_features[node].values()))
        y.append(node in token_a_users)

    for edge in graph.edges:
        X_edge.append([edge_features[edge]['asset_type']])

    # One-hot encoding for categorical feature 'asset_type'
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    X_edge_encoded = encoder.fit_transform(X_edge)

    X = []
    for i in range(len(X_node)):
        # C: Why would we want to add the number of interactions to the X matrix?
        X.append(X_node[i] + X_edge_encoded[i].tolist())

    X = StandardScaler().fit_transform(X)

    # Step 5: Train clustering model
    model = SpectralClustering(n_clusters=2, affinity='nearest_neighbors')
    model.fit(X)

    # Step 6: Output user ID clusters
    clusters = {}
    for i, node in enumerate(graph.nodes):
        cluster_label = model.labels_[i]
        if cluster_label not in clusters:
            clusters[cluster_label] = []
        clusters[cluster_label].append(node)

    for cluster_label, users in clusters.items():
        print(f"Cluster {cluster_label}: {users}")

    return True


if __name__ == '__main__':
    get_clusters()
