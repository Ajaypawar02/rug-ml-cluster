'''
A script to generate a random dataset of interactions between users in a social network.

The script takes in a number of users and a number of interactions and generates a random dataset of interactions between users as a .CSV file.
'''

import random
import numpy as np
import json

assets = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

def generate_random_integer(minimum: int, maximum: int) -> int:
    return int(random.randint(minimum, maximum))


def generate_graph(users: int) -> dict:
    total_users = 10 * users

    # Generate a random mapping of users to IDs
    user_mapping = dict(zip(list(range(total_users)), [int(item) for item in np.random.permutation(list(range(total_users)))]))

    # Add initial interaction with root node
    output = [{'user0': user_mapping[0], 'user1': user_mapping[i], 'asset': 'A', 'amount': generate_random_integer(1e4, 1e6), 'timestamp': generate_random_integer(16e6, 19e6)} for i in range(1, users)]
    output += [{'user0': user_mapping[i], 'user1': user_mapping[0], 'asset': np.random.choice(assets), 'amount': generate_random_integer(1e4, 1e6), 'timestamp': generate_random_integer(16e6, 19e6)} for i in range(1, users)]

    # Generate random clusters of users
    clusters = np.random.choice(users, generate_random_integer(1, users), replace=False)

    # Add random interactions within clusters
    for cluster in clusters:
        for user in range(cluster):
            iterations = np.random.randint(1, int(np.sqrt(users)))
            for _ in range(iterations):
                user0 = user if np.random.rand() < 0.5 else int(np.random.choice(cluster))
                user1 = user if user0 != user else int(np.random.choice(cluster))
                output.append({'user0': user_mapping[user0], 'user1': user_mapping[user1], 'asset': np.random.choice(assets), 'amount': generate_random_integer(1e4, 1e6), 'timestamp': generate_random_integer(12e6, 19e6)})

    # Add random interactions between additional users
    for external_user in range(users, total_users):
        iterations = np.random.randint(1, users)
        for _ in range(iterations):
            user0 = external_user if np.random.rand() < 0.5 else int(np.random.choice(users))
            user1 = int(np.random.choice(range(10 * users)))
            output.append({'user0': user_mapping[user0], 'user1': user_mapping[user1], 'asset': np.random.choice(assets), 'amount': generate_random_integer(1e4, 1e6), 'timestamp': generate_random_integer(12e6, 19e6)})

    return {'interactions': list(np.random.permutation(output))}


def main(N: int) -> None:
    # Generate and write the output to JSON file
    with open("data/interactions.json", "w") as outfile:
        print(i := generate_graph(N))
        json.dump(i, outfile)
    return


if __name__ == '__main__':
    main(100)
