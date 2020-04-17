from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def move_me(direction):

    player.travel(direction)
    traversal_path.append(direction)


def dft(visited=None, prev=None, moves=None, p=player):


    print(visited)
    # Initialize our current position
    current = p.current_room.id
    # Get neighbors
    neighbors = p.current_room.get_exits()
    # Directional map
    reverse_dir = {'s': 'n', 'n': 's', 'w': 'e', 'e': 'w'}

    # # If visited is None, initialize to an empty dict
    # # so we can recurse with visited
    if not visited:
        visited = {}

    # If it's a new room, initialize an empty dictionary at that room
    if current not in visited:
        visited[current] = {}

    # If we can move, update the current room
    if moves:
        visited[prev][moves] = current

    if prev:
        visited[current][reverse_dir[moves]] = prev

    if len(visited[current]) < len(neighbors):
        for direction in neighbors:
            if direction not in visited[current]:
                move_me(direction)
                dft(visited, prev=current, moves=direction)

    if len(visited) < len(room_graph):
        direction = reverse_dir[moves]
        move_me(direction)

    # print(visited.keys())


dft()


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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
