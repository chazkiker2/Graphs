from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from collections import deque

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

NORTH = "n"
EAST = "e"
SOUTH = "s"
WEST = "w"
UNEXPLORED = "?"
directions = [NORTH, EAST, SOUTH, WEST]
opposite = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

tg = {}

unexplored_rooms = {}


def bfs(starting_room):
    q = deque()
    q.append([('*', starting_room)])
    visited = set()
    while q:
        path = q.popleft()
        direction, room = path[-1]
        if room not in visited:
            visited.add(room)
            if room not in tg or UNEXPLORED in tg[room].values():
                return path
            for known in tg[room].items():
                new_path = path.copy()
                q.append(new_path + [known])


def dft(last_id=None, travved_dir=None):
    id_ = player.current_room.id
    possible_paths = player.current_room.get_exits()
    if id_ not in tg:
        tg[id_] = {direction: UNEXPLORED for direction in possible_paths}
    if last_id and travved_dir:
        tg[id_][opposite[travved_dir]] = last_id
    unexplored_paths = [
        direction for direction in possible_paths if
        direction in tg[id_] and tg[id_][direction] == UNEXPLORED
    ]
    if not unexplored_paths:
        # bfs back to closest node with unvisited
        most_recent_unexplored = bfs(id_)
        if most_recent_unexplored:
            for d, r_id in most_recent_unexplored[1:]:
                traversal_path.append(d)
                player.travel(d)
            dft()
        else:
            return
    else:
        to_explore = random.choice(unexplored_paths)
        tg[id_][to_explore] = player.current_room.get_room_in_direction(to_explore).id
        player.travel(to_explore)
        traversal_path.append(to_explore)
        dft(id_, to_explore)


dft()
print(tg)
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
