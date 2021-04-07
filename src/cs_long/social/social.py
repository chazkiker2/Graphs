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
        """creates friendships between the user with the given ID and an iterable of all the other friends"""

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
        Populates
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

        Bi-Directional Search operates by running two BFS simultaneously,
        one from the starting node and one from the destination node
        Each iteration, we'll take one extend the two paths by one more level
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
