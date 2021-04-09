from collections import deque
import random
import time


class Queue:
    def __init__(self):
        self.storage = deque()

    def __len__(self):
        return len(self.storage)

    def enqueue(self, value):
        # add to right (tail)
        self.storage.append(value)

    def dequeue(self):
        # take from left (head)
        return self.storage.popleft()


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendships(self, user_id, *friends):
        """creates friendships between the user with the given ID and an iterable of all the other friends"""

        for friend in friends:
            self.add_friendship(user_id, friend)

    def add_friendship(self, user_id, friend_id):
        """Creates a bi-directional friendship"""

        if user_id == friend_id:
            # print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def reset_network(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def populate_graph(self, num_users, avg_friendships):
        self.reset_network()

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

    def populate_graph_linear(self, num_users, avg_friendships):
        self.reset_network()

        for i in range(num_users):
            self.add_user(f"test_user_{i}")

        # set a target to friendships to (num_users * avg_friendships)
        target_friendships = num_users * avg_friendships
        # create a counter for the total number of friendships created and set it to zero
        current_friendship_count = 0
        # create a collisions counter and set it to zero
        collisions = 0

        # iterate while the target friendships are less than total friendships
        while current_friendship_count < target_friendships:

            # randomly pick a user as the user_id
            user_id = random.randint(1, self.last_id)
            # randomly pick a user as the friend_id
            friend_id = random.randint(1, self.last_id)

            # if an add_friendship call returns true –– then we added 2 friendships
            res = self.add_friendship(user_id, friend_id)
            if res:
                # add 2 to the total friendships (due to bi-directional nature of connections)
                current_friendship_count += 2
            else:
                # increment collisions
                collisions += 1

        print(f"collisions={collisions}")

    # BFS breadth-first search implementation
    # @see get_shortest_social_path for bi-directional (faster) implementation
    def get_shortest_bfs(self, start, destination):
        """
        returns the shortest path between the starting friend and destination friend

        !BFS implementation!
        @see get_shortest_social_path for bi-directional (faster) implementation
        """

        q = deque()
        q.append([start])
        visited = set()
        while q:
            path = q.popleft()
            friend = path[-1]
            if friend not in visited:
                if friend == destination:
                    return path
                visited.add(friend)
                for next_friend in self.friendships[friend]:
                    q.append(path.copy() + [next_friend])

    # bi-directional search implementation
    def get_shortest_social_path(self, start, destination):
        """
        returns the shortest path between the starting friend and destination friend

        !BI-DIRECTIONAL SEARCH IMPLEMENTATION!
        @see get_shortest_bfs for BFS (slower) implementation

        Bi-Directional Search operates by running two BFS simultaneously:
        - one from the starting node
        - one from the destination node
        Each iteration, we'll take extend the two paths by one more level
        Once the paths overlap, we know we've hit a potential solution
        """

        # if they are the same user
        if start == destination:
            # then there is only one shortest path to self
            return [start]

        # dictionary of currently active vertices with their corresponding paths.
        active_paths = {
            start: [start],  # path from start to _some_node_
            destination: [destination]  # path from destination node to _some_node_
        }

        # will contain vertices that we've ruled out along the way
        inactive_verts = set()

        # while there are still potential solution paths
        while active_paths:
            # every key in active_paths is an active vertex
            active_verts = list(active_paths.keys())

            # for every active vertex
            for vert in active_verts:
                # the current path from node to somewhere
                current_path = active_paths[vert]
                # starting node in this path
                origin = current_path[0]
                # all unique friends that are still active
                current_neighbors = set(self.friendships[vert]) - inactive_verts

                # check if our current neighbors hit an active vertex
                # this would happen once each BFS overlaps
                # if this happens, we have a potential solution path
                for meeting_vert in current_neighbors.intersection(active_verts):
                    # check to make sure that the two paths didn't start at the same place
                    # if they didn't, then we've got a path from start to destination
                    if origin != active_paths[meeting_vert][0]:
                        # reverse one of the paths
                        active_paths[meeting_vert].reverse()
                        # combine the results
                        joined_paths = active_paths[vert] + active_paths[meeting_vert]
                        # check if joined_paths starts with the proper starting friend
                        if joined_paths[0] != start:
                            # if joined paths is in reverse order (i.e, from destination friend to starting friend)
                            # then we'll reverse it to start at the starting friend
                            joined_paths.reverse()
                        # return our joined paths from start to destination
                        return joined_paths

                # if we're here, we did not find a solution at this level

                # so check for new neighbours to extend our paths another level
                new_neighbors = set(current_neighbors) - inactive_verts - set(active_verts)
                # for every new neighbor
                # extend the paths, remove the previous one, and update the active vertices
                for neighbor_vert in new_neighbors:
                    # extend path and update record
                    active_paths[neighbor_vert] = current_path + [neighbor_vert]
                    # add the neighbor vert to our list of active vertices
                    active_verts.append(neighbor_vert)

                # finally, remove the current path (b/c we did not get a solution)
                # and record the current vert as an inactive endpoint.
                active_paths.pop(vert, None)
                inactive_verts.add(vert)

    def get_all_social_paths(self, user_id):
        """
        find a detailed extended network for the user with the given id

        Returns a dictionary containing every user in that user's extended network with the
        shortest friendship path between them. The key is the relevant friend's ID; the
        value is the shortest path between them
        :param user_id: the relevant user for which to find an extended network
        """

        # start with a DFS to get the extended social network
        # using deque in LIFO fashion: add to tail, take from tail
        stack = deque()
        # add user_id to the top of the stack
        stack.append(user_id)
        # will keep track of each friend in extended network
        friend_paths = {}

        # while stack is not empty
        while stack:
            # take our current friend off the top of the stack
            friend = stack.pop()
            # if we haven't yet visited this friend
            if friend not in friend_paths:
                # make an empty entry in our friend_paths
                friend_paths[friend] = None
                # for every connection that this friend has
                for connection in self.friendships[friend]:
                    # add connection to the top of our stack
                    stack.append(connection)

        # currently, my get_shortest_social_path employs a Bi-Directional Search
        # to find the shortest path between a Source and Destination.
        # This could also be a BFS, but the Bi-Directional is wildly more scalable
        return {
            # get the shortest path between the input user_id and
            # each friend_id in the network of extended friends
            friend_id: self.get_shortest_social_path(user_id, friend_id)
            for friend_id in friend_paths
        }

    def get_all_social_paths_lecture(self, user_id):
        q = deque()
        q.append([user_id])
        visited = {}

        while q:
            current_path = q.popleft()
            current_user_id = current_path[-1]
            if current_user_id not in visited:
                visited[current_user_id] = current_path
                for friend in self.friendships[current_user_id]:
                    q.append(current_path + [friend])

        return visited

    def get_all_social_paths_linear(self, user_id):
        pass


if __name__ == '__main__':
    num_users = 10000
    avg_friendships = 15000

    sg = SocialGraph()
    start_time = time.time()
    sg.populate_graph(num_users, avg_friendships)
    end_time = time.time()
    print(f"QUADRATIC --- {end_time - start_time} seconds")

    start_time2 = time.time()
    sg.populate_graph_linear(num_users, avg_friendships)
    end_time2 = time.time()
    print(f"LINEAR --- {end_time2 - start_time2} seconds")
