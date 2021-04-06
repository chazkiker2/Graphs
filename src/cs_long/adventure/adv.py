import random
from collections import deque
from ast import literal_eval

from player import Player
from world import World

# ----------------------------
# Seed the World
world = World()

map_files = {
    "line": "maps/test_line.txt",
    "cross": "maps/test_cross.txt",
    "loop": "maps/test_loop.txt",
    "loop_fork": "maps/test_loop_fork.txt",
    "main": "maps/main_maze.txt"
}

map_file = map_files["main"]

# loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

# Initialize the Player in the starting_room
player = Player(world.starting_room)

# ----------------------------
# Solution code

# declaring constants for readability and to reduce risk of errors
NORTH = "n"
EAST = "e"
SOUTH = "s"
WEST = "w"
UNEXPLORED = "?"

# declared for ease of use in constructing undirected graph
# accessing one direction will return opposite direction
opposite = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

# 'traversal_path' will contain directions for the user to walk
# that will visit every node in the graph (or 'room' in the 'maze')
traversal_path = []

# 'traversal_graph' will have keys representing each room id that we've visited
# the associated value will be a sub-dictionary with a cardinal direction
# representing a known path out of the room
# The associated value will be either the id of the room on the other side or a '?'
traversal_graph = {}


def bfs(starting_room_id):
    """finds the shortest path from the starting room to a room with an unexplored route

    This function is a breadth first search that will start at the room with the given id.
    We will traverse through every known connection until we find one that has an unexplored route

    The value returned will be a list of tuple pairs. Each tuple pair will have (direction, room_in_direction).
    The first room will be the room we started at, the last room being the closest room with unexplored paths.
    The player will be able to walk the 'direction' in each tuple to end up at the room with paths to explore
    """
    q = deque()
    q.append([('*', starting_room_id)])
    visited = set()
    while q:
        # take the path at the head of the queue
        path = q.popleft()
        # get the last connection pair in our current path
        # '_' would have been the direction associated with this connection
        # but that is only relevant for the returned path
        _, room = path[-1]
        if room not in visited:
            visited.add(room)
            # if there is an unexplored path in this room's connections, then we've found our target
            if UNEXPLORED in traversal_graph[room].values():
                return path  # return the path; this is the shortest path to not fully explored room

            # for ever connection—(direction, room) in this room's connections
            for connection in traversal_graph[room].items():
                # add the next possible path (from START to SOME_NODE) to the end of the queue
                q.append(path.copy() + [connection])


def dft(last_id=None, travelled_direction=None):
    """populates a path that, when walked in order, will visit every room in the map at least once

    This function is a depth-first traversal that picks a random unexplored direction from the player's
    current room; travels in that direction; then loops. If we reach a dead-end (i.e., a room with
    no unexplored paths), we will walk back to the nearest room with new paths to explore
    """
    id_ = player.current_room.id
    possible_paths = player.current_room.get_exits()
    if id_ not in traversal_graph:
        traversal_graph[id_] = {direction: UNEXPLORED for direction in possible_paths}
    if last_id and travelled_direction:
        traversal_graph[id_][opposite[travelled_direction]] = last_id
    unexplored_paths = [
        direction for direction in possible_paths if
        direction in traversal_graph[id_] and traversal_graph[id_][direction] == UNEXPLORED
    ]
    # if unexplored_paths is empty, we'll have to traverse back to a room with an unexplored route
    if not unexplored_paths:
        # bfs back to closest node with an unvisited path
        most_recent_unexplored = bfs(id_)
        # if there is a path to a not-fully-explored node,
        # we'll travel that path to get back to the unexplored node
        if most_recent_unexplored:
            for d, r_id in most_recent_unexplored[1:]:
                traversal_path.append(d)
                player.travel(d)
            dft()
        # otherwise, there must not be any other rooms to traverse!
        else:
            return
    # else, there are paths to explore at this room; let's pick one
    else:
        # choose an unexplored path at random
        to_explore = random.choice(unexplored_paths)
        # explore. this finds what room is on the other side of our connection and updates our traversal_graph
        traversal_graph[id_][to_explore] = player.current_room.get_room_in_direction(to_explore).id
        # have the player travel in this direction
        player.travel(to_explore)
        # represent this travel in our path
        traversal_path.append(to_explore)
        # recurse to continue dft
        dft(id_, to_explore)


dft()  # invoke the traversal to explore all the rooms

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
