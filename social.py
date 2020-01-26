
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
        
        if self.get_all_social_paths(starting_vertex,"?") == None:
            return

        if "?" not in self.vertices[starting_vertex].values():
            arr=self.get_all_social_paths(starting_vertex,"?")   
            for movement in arr[starting_vertex]:
                        for move in self.vertices[starting_vertex].keys():
                            if self.vertices[starting_vertex][move]==movement:
                                    # print("TEEEEST",movement,move,starting_vertex)
                                    player.travel(move)
                                    traversal_path.append(move)

            self.dft_recursive(player.current_room.id, visited)       

        else:
            RandomDirection=random.range(0,4)
            for child_vert in self.vertices[starting_vertex]:  
                if child_vert ==Directions[RandomDirection]:
                    if self.vertices[starting_vertex][child_vert] == "?":
                        player.travel(child_vert)
                        if player.current_room.id not in self.vertices.keys():
                            self.add_vertex(player.current_room.id)
                            obj={}
                            for i in player.current_room.get_exits():
                                obj[i]="?"    
                            self.add_edge(player.current_room.id,obj)
                            obj={}
                        if player.current_room.id not in visited:
                            traversal_path.append(child_vert)

                            if child_vert=="n":
                                self.vertices[starting_vertex][child_vert]=player.current_room.id
                                self.vertices[player.current_room.id]["s"]=starting_vertex
                            elif child_vert=="s":
                                self.vertices[starting_vertex][child_vert]=player.current_room.id
                                self.vertices[player.current_room.id]["n"]=starting_vertex
                            elif child_vert=="e":
                                self.vertices[starting_vertex][child_vert]=player.current_room.id
                                self.vertices[player.current_room.id]["w"]=starting_vertex
                            elif child_vert=="w":
                                self.vertices[starting_vertex][child_vert]=player.current_room.id
                                self.vertices[player.current_room.id]["e"]=starting_vertex

                            self.dft_recursive(player.current_room.id, visited)
                            # print("visited",visited)

def get_all_social_paths(self, starting_vertex,destination_vertex):
        """
        Takes a user's starting_vertex as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {} # Note that this is a dictionary, not a set
        shortest=[None]*len(self.vertices)
        # variable=0
        queue=Queue()
        queue.enqueue([starting_vertex])
        while queue.size()>0:
            path=queue.dequeue()
            # print("path",path)
            current_user = path[-1]
            # print("current_user", current_user)
            if current_user not in visited:
                print("visited", visited,"starting_vertex",starting_vertex,"destination_vertex",destination_vertex)
                visited[current_user]=path

                for ID in self.vertices[current_user].values():
                    print("ID", ID)
                    if ID =="?":
                        new_path=list(path)
                        new_path.append(ID)
                        queue.enqueue(new_path)
                        if len(visited[current_user])<len(shortest) and len(visited[current_user])>1:
                            shortest=visited[current_user]
                    
        # del visited[user_id]
        print("shortest",shortest, visited)
        return visited



                if "?" not in self.vertices[starting_vertex].values():
                    # if starting_vertex==0:
                    #     return self.dft_recursive("?", visited)
                    # print("INSIDE",child_vert,starting_vertex, self.vertices,visited)
                    visited.add(starting_vertex)  
                    arr=self.get_all_social_paths(starting_vertex,"?")  
                    print("arr[starting_vertex]",arr[starting_vertex])
                    for movement in arr[starting_vertex]:
                        for move in self.vertices[starting_vertex].keys():
                            if self.vertices[starting_vertex][move]==movement:
                                    # print("TEEEEST",movement,move,starting_vertex)
                                    player.travel(move)
                                    if player.current_room.id==0 and "?" not in self.vertices[player.current_room.id].values():
                                        return
                                    # print("player.current_room.id",player.current_room.id)
                                    traversal_path.append(move)

                    self.dft_recursive(player.current_room.id, visited)