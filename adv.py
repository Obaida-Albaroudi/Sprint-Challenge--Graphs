from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval
import sys
sys.setrecursionlimit(15000)
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
# traversal_path = ['n', 'n',"s","e"]
traversal_path = []


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# Maybe create graph
class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = {}
    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        If both exist, and a connection from v1 to v2
        """

        self.vertices[v1]=(v2)
    
        # if v1 in  self.vertices and v2 in self.vertices:
        #     self.vertices[v1].add(v2)
        # else:
        #     raise IndexError("That vertex does not exist!")
    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """
        Directions=["n","s","e","w"]

        if len(self.vertices)<=1:
            self.add_vertex(starting_vertex)
            objects={}
            for i in player.current_room.get_exits():
                objects[i]="?"    
            self.add_edge(player.current_room.id,objects)
        if visited is None:
            visited=set()

        if "?" not in self.vertices[starting_vertex].values():
            visited.add(starting_vertex)
            arr=self.get_all_social_paths(starting_vertex,"?")
            print("arr",arr)
            if arr== None:
                print("Break")
                return
            else:
                print("Continue", self.vertices)

                # print("arr",arr,"arr[starting_vertex]",starting_vertex)   
                for movement in arr:
                            # print("TEEEEST",movement,starting_vertex,self.vertices[starting_vertex].keys())
                            for move in self.vertices[starting_vertex].keys():
                                # print("TEEEEST",movement,move,starting_vertex)
                                if self.vertices[starting_vertex][move]==movement:                                        
                                        player.travel(move)
                                        traversal_path.append(move)

                self.dft_recursive(player.current_room.id, visited)       

        else:
            RandomDirection=random.randrange(0,4)
            for child_vert in self.vertices[starting_vertex]:  
                # print("Directions[RandomDirection]",Directions[RandomDirection],"player.current_room.id",player.current_room.id,"starting_vertex",starting_vertex,"child_vert",child_vert,"self.vertices",self.vertices )
                if child_vert ==Directions[RandomDirection]:
                    # print("SUCCESS")
                    if self.vertices[starting_vertex][child_vert] == "?":
                        player.travel(child_vert)
                        # print("Directions[RandomDirection] 2222",Directions[RandomDirection],"player.current_room.id",player.current_room.id,"starting_vertex",starting_vertex,"child_vert",child_vert)
                        if player.current_room.id not in self.vertices.keys():
                            self.add_vertex(player.current_room.id)
                            obj={}
                            for i in player.current_room.get_exits():
                                obj[i]="?"    
                            self.add_edge(player.current_room.id,obj)
                            obj={}
                        if player.current_room.id not in visited:
                            traversal_path.append(child_vert)
                            # print("child vert", child_vert)
                            if child_vert=="n":
                                # print("Wow",player.current_room.id)
                                self.vertices[starting_vertex][child_vert]=player.current_room.id
                                # self.vertices[player.current_room.id]["s"]=starting_vertex
                            elif child_vert=="s":
                                self.vertices[starting_vertex][child_vert]=player.current_room.id
                                # self.vertices[player.current_room.id]["n"]=starting_vertex
                            elif child_vert=="e":
                                self.vertices[starting_vertex][child_vert]=player.current_room.id
                                # self.vertices[player.current_room.id]["w"]=starting_vertex
                            elif child_vert=="w":
                                self.vertices[starting_vertex][child_vert]=player.current_room.id
                                # self.vertices[player.current_room.id]["e"]=starting_vertex
                            print("inside",player.current_room.id)
                            self.dft_recursive(player.current_room.id, visited)
                # else:
            self.dft_recursive(player.current_room.id, visited)

    def get_all_social_paths(self, starting_vertex,destination_vertex):
            """
            Takes a user's starting_vertex as an argument

            Returns a dictionary containing every user in that user's
            extended network with the shortest friendship path between them.

            The key is the friend's ID and the value is the path.
            """
            visited = {} # Note that this is a dictionary, not a set
            # variable=0
            queue=Queue()
            queue.enqueue([starting_vertex])
            while queue.size()>0:
                path=queue.dequeue()
                # print("path",path)
                current_user = path[-1]
                # print("current_user", current_user)
                if current_user not in visited:
                    if "?" in self.vertices[current_user].values():
                        # print("path",path, self.vertices[current_user].values())
                        return path

                    # print("current_user", current_user)
                    visited[current_user]=path

                    for ID in self.vertices[current_user].values():
                        # print("inside")
                        new_path=list(path)
                        new_path.append(ID)
                        queue.enqueue(new_path)


            

graphs=Graph()

graphs.dft_recursive(player.current_room.id)

print("HI",player.current_room.id)
print(graphs.vertices)

# print(bfs(player.current_room, "?"))
player.current_room = world.starting_room
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
    # print("move",move,"player.current_room",player.current_room,"visited_rooms",visited_rooms)

# print("visited_rooms",len(visited_rooms), traversal_path)
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
