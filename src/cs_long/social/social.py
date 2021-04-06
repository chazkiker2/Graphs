from collections import deque
import random


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendships(self, user_id, *friends):
        for friend in friends:
            self.add_friendship(user_id, friend)

    def add_friendship(self, user_id, friend_id):
        """Creates a bi-directional friendship"""

        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments
        Creates that number of users and a randomly distributed friendships
        between those users.
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        for i in range(num_users):
            self.add_user(f"test_user_{i}")

        potential_friendships = [
            (user_id, friend_id)
            for user_id in self.users
            for friend_id in range(user_id + 1, self.last_id + 1)
        ]
        random.shuffle(potential_friendships)
        for i in range((num_users * avg_friendships) // 2):
            f1, f2 = potential_friendships[i]
            self.add_friendship(f1, f2)

    def get_shortest_social_path(self, start, end):
        q = deque()
        q.append([start])
        visited = set()
        while q:
            path = q.popleft()
            friend = path[-1]
            if friend not in visited:
                if friend == end:
                    return path
                visited.add(friend)
                for next_friend in self.friendships[friend]:
                    q.append(path.copy() + [next_friend])

    def get_all_social_paths(self, user_id):
        """
        :param user_id: the relevant user for which to find an extended network

        Returns a dictionary containing every user in that user's extended network
        with the shortest friendship path between them.
        The key is the relevant friend's ID; the value is the shortest path between them
        """
        stack = deque()
        stack.append(user_id)
        friend_paths = {}

        while stack:
            friend = stack.pop()
            if friend not in friend_paths:
                friend_paths[friend] = None
                for next_friend in self.friendships[friend]:
                    stack.append(next_friend)

        return {
            friend_id: self.get_shortest_social_path(user_id, friend_id)
            for friend_id in friend_paths
        }


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(f"sg.friendships={sg.friendships}")
    connections = sg.get_all_social_paths(1)
    print(f"connections={connections}")
