import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import datetime
import pyperclip
import itertools

# Constants for time costs  
t_0 = 2  # Time for a normal path  
t_B = 10  # Time for a broken path  
t_T = 6 # Time for a thin path  
t_N = float('inf')  # Time for no path (infinity)  
t_lr = 2  # Additional time when turning left or right 

class Vtx_normal(object):  
    def __init__(self, name, x, y):  
        self.name = name  
        self.x = x  
        self.y = y  

    def __str__(self):  
        return str(self.name) + '(' + str(self.x) + ',' + str(self.y) + ')'  

    def __repr__(self):  
        return self.__str__() 
    
    def optimized_paths(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) 
    
    
    

class Vtx(object):
    def __init__(self, name, x, y):
        self.name=name
        self.x=x
        self.y=y
    # def getName(self):
    #     return self.name
    def __str__(self):
        return str(self.name) + '('+str(self.x) +','+ str(self.y) + ')'
    
    def __repr__(self):
        return self.__str__()
    
    def getName(self):
        return f'V({self.x},{self.y})'
    
    def optimized_paths(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    

class Edge:  
    def __init__(self, x1, y1, x2, y2):  
        self.x1 = x1  
        self.y1 = y1  
        self.x2 = x2  
        self.y2 = y2  

    # Consistent name to search for similar edge
    def __str__(self):
        if (self.x2 + self.y2) > (self.x1 + self.y1):
            
            return f"Edge(({self.x1}, {self.y1}), ({self.x2}, {self.y2}))"
        
        elif (self.x1 + self.y1) > (self.x2 + self.y2):
            return f"Edge(({self.x2}, {self.y2}), ({self.x1}, {self.y1}))"
    
    
    def __repr__(self):  
        return self.__str__()  

class Obs:  
    def __init__(self, edge, obs_type):  
        if not isinstance(edge, Edge) or not isinstance(obs_type, str):  
            raise ValueError("edge must be an Edge object and type must be a string.")  

        self.edge = edge  
        self.type = obs_type  # type of obstacle: B (broken), T (thin), N (no path)  

        # Assign value based on the type  
        if obs_type == "B":  
            self.value = t_B  
        elif obs_type == "T":  
            self.value = t_T  
        elif obs_type == "N":  
            self.value = t_N  

    def __str__(self):  
        return f"Obs({self.edge}, type={self.type}, v={self.value})"  

    def __repr__(self):  
        return self.__str__()  

    def get_edge(self):  
        return self.edge

    def get_type(self):  
        return self.type  

    def get_value(self):  
        return self.value  
    
    
    
class Board:  
    def __init__(self, obstacles_data):  
        self.vertices = self.create_vertices()
        self.obstacles = [Obs(Edge(x1, y1, x2, y2), obs_type) for x1, y1, x2, y2, obs_type in obstacles_data]
        self.t_0 = t_0
        self.t_B = t_B
        self.t_T = t_T
        self.t_N = t_N
        self.t_lr = t_lr


    # Create all vertices on the boards (36 points)
    def create_vertices(self):  
        vertices = {}  
        for i in range(6):  # from (0,0) to (5,5), so we need 6 points  
            for j in range(6):  
                name = f'V({i},{j})'  
                vertices[name] = Vtx_normal(name, i, j)  
        return vertices  

    # Find all the possible paths for the car to run with number_of_paths
    
    def find_paths(self, start_point, end_point, number_of_paths):  
        start_vertex = self.vertices[start_point]  
        end_vertex = self.vertices[end_point]  

        all_paths = []  
        self.dfs(start_vertex, end_vertex, [], all_paths, number_of_paths, 0, set())  
        
        return all_paths  

    # Checking all the paths, delete unnecessary paths
    def dfs(self, current, end, path, all_paths, total_steps, current_steps, visited):  
        # Add the current vertex to the path  
        path.append((current.x, current.y))  
        visited.add((current.x, current.y))  

        # If we reached the end but the steps used do not match, return  
        if current == end:  
            if current_steps < total_steps:  
                # We've reached the end too soon, so we don't record this path!  
                path.pop()  
                visited.remove((current.x, current.y))  
                return  
        
        # If we used the total steps, store the path only if we're at the end  
        if current_steps == total_steps:  
            if current == end:  
                all_paths.append(path.copy())  

        # If we exceeded the steps, backtrack  
        if current_steps >= total_steps:  
            path.pop()  
            visited.remove((current.x, current.y))  
            return  

        # Explore adjacent vertices  
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # left, right, up, down  
            nx, ny = current.x + dx, current.y + dy  
            if 0 <= nx < 6 and 0 <= ny < 6:  # Ensure it is within bounds  
                next_vertex_name = f'V({nx},{ny})'  
                next_vertex = self.vertices[next_vertex_name]  
                
                # Only visit if it hasn't been visited  
                if (nx, ny) not in visited:  
                    self.dfs(next_vertex, end, path, all_paths, total_steps, current_steps + 1, visited)  

        # Backtrack  
        path.pop()  
        visited.remove((current.x, current.y))  

    
    # Calculate the number of turns required for the given path with an initial direction.  
    def calculate_turns(self, initial_direction, path):  
        if len(path) < 2:  
            return 0  # No turns if the path has less than two points  

        turns = 0  
        turns_guidance = []
        last_direction = initial_direction  

        for i in range(1, len(path)):  
            x1, y1 = path[i - 1]  
            x2, y2 = path[i]  

            # Determine the direction of movement  
            dx = x2 - x1  
            dy = y2 - y1  
            current_direction = (dx, dy)  

            # Count turns  
            if last_direction == current_direction:
                turns_guidance.append('Move Straight')
                
            elif (current_direction[0] + last_direction[0] == 0) and (current_direction[1] + last_direction[1] == 0):  
                turns += 2  
                turns_guidance.append('U - Turn')  
            else:  
                # To determine the type of turn  
                if last_direction == (0, 1) and current_direction == (1, 0):  
                    turns += 1  # Right Turn  
                    turns_guidance.append('Right Turn')  
                elif last_direction == (1, 0) and current_direction == (0, -1):  
                    turns += 1  # Right Turn  
                    turns_guidance.append('Right Turn')  
                elif last_direction == (0, -1) and current_direction == (-1, 0):  
                    turns += 1  # Right Turn  
                    turns_guidance.append('Right Turn')  
                elif last_direction == (-1, 0) and current_direction == (0, 1):  
                    turns += 1  # Right Turn  
                    turns_guidance.append('Right Turn')  
                else:  
                    # Otherwise, it's a left turn  
                    turns += 1  # Left Turn  
                    turns_guidance.append('Left Turn')
                
                last_direction = current_direction
                

        return turns, turns_guidance, last_direction
    
    
    def calculate_total_time(self,initial_direction,path):  
        total_time = 0   

        for i in range(len(path) - 1):  
            x1, y1 = path[i]  
            x2, y2 = path[i + 1]  
            edge = Edge(x1, y1, x2, y2)

            # Check which obstacle type is associated with this edge  
            obs_check = 0
            for obstacle in self.obstacles:
                if str(obstacle.get_edge()) == str(edge):
                    total_time += obstacle.get_value()
                    # print(f'The car stuck at {edge} with the {obstacle.get_type()} path')
                    obs_check = 1
                    break
            if obs_check == 0:
                total_time += t_0     

            # Calculate turns with initial direction  

        turns,turns_guidance, last_direction= self.calculate_turns(initial_direction, path) 
        # print(f'The number of turns is {turns}')
        total_time += int(turns) * self.t_lr 

        return total_time, turns_guidance, last_direction
    
    
    def find_optimized_paths(self, initial_direction,start_point, end_point, number_of_paths):
        
        
        all_paths = self.find_paths(start_point, end_point, number_of_paths)
        
        min_dis = float('inf')
        min_turn_guidance = []
        min_last_direction = ''
        min_path = []
        for path in all_paths:
            
            total_time,turn_guidance, last_direction = self.calculate_total_time(initial_direction , path)
            
            if total_time < min_dis:
                min_dis = total_time
                min_turn_guidance = turn_guidance
                min_last_direction = last_direction
                min_path = path

        return min_path, min_dis, min_turn_guidance, min_last_direction
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
class Edge:
    def __init__(self, x1, y1, x2, y2):
        # Initialize the coordinates of the edge - the edge connects (x1, y1) and (x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        # Return a string representation of the edge
        return f"Edge(({self.x1}, {self.y1}), ({self.x2}, {self.y2}))"

    def __repr__(self):
        # Return a string representation suitable for debugging
        return self.__str__()
    
    
t_0= 2 # extra time taken to turn 90 degree
t_B= 6 # extra time taken to travel on broken line B - need to do our own research
t_T=  10#  extra time taken to travel on thin line T = need to find out by experiences
t_N=float('inf')# extra time taken to travel on no line N

class Obs:
    def __init__(self, edge, type):
        if not isinstance(edge, Edge) or not isinstance(type, str):
            raise ValueError("edge must be an Edge object and type must be a string.")

        self.edge = edge
        self.type = type # type of obstacle B: broken line, T: thin line, N: no line

        # Assign v based on the type
        if type == "B":
            self.value = t_B
        elif type == "T":
            self.value = t_T
        elif type == "N":
            self.value = t_N

    def __str__(self):
        return f"Obs({self.edge}, type={self.type}, v={self.value})"

    def __repr__(self):
        return self.__str__()

    def get_edge(self):
        return self.edge

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value





