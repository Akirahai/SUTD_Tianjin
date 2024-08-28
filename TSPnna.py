from libs import *


obstacles_data = [  
    (1, 0, 2, 0, "T"),  
    (3, 0, 4, 0, "T"),  
    (2, 1, 3, 1, "T"),  
    (1, 1, 1, 2, "N"),  
    (1, 2, 2, 2, "N"),  
    (4, 4, 5, 4, "B"),  
    (5, 4, 5, 5, "B")  
]  

def nearest_neighbor_path(board, vtx_list, initial_dir):  
    
    start_vertex = vtx_list[0]  # Start at V(0,0) - 0 


    visited = [False] * len(vtx_list)  # Track visited vertices  
    visited[0] = True  # Mark starting vertex as visited  
    current_vertex = start_vertex


    full_path = [current_vertex]  # Start guided_path with the starting vertex  


    total_distance = 0  
    checked_dir = initial_dir  
    full_guidance = {}
    full_guided_path = {}



    while len(full_path) < len(vtx_list):  
        nearest_vertex = None  
        min_distance = float('inf')  

        # Find the nearest unvisited vertex  
        for i in range(len(vtx_list)):  
            if not visited[i]:  
                

                _, distance, _, _ = board.find_optimized_paths(checked_dir, current_vertex, vtx_list[i])
                
                if distance < min_distance:  
                    min_distance = distance  
                    nearest_vertex = vtx_list[i]  

        # Move to the nearest vertex  
        if nearest_vertex:  
            # Update total_distance with the distance to the nearest vertex 
            
            guided_path, nearest_distance, turn_guidance, last_direction = board.find_optimized_paths(checked_dir, current_vertex, nearest_vertex)
            
            total_distance += nearest_distance
        
            full_guidance[f'From {current_vertex.getName()} to {nearest_vertex.getName()}'] = turn_guidance

            full_guided_path[f'From {current_vertex.getName()} to {nearest_vertex.getName()}'] = guided_path

            full_path.append(nearest_vertex)  
            
            visited[vtx_list.index(nearest_vertex)] = True  
            
            # print(f' Found the nearest vertex next to {current_vertex} is {nearest_vertex}')
            
            current_vertex = nearest_vertex  
            checked_dir = last_direction
            
        

    # Return to starting point:  
    guided_path, distance_to_start, turn_guidance, last_direction = board.find_optimized_paths(checked_dir, current_vertex, start_vertex) 
    
    total_distance += distance_to_start  
    
    full_guidance[f'From {current_vertex.getName()} to {nearest_vertex.getName()}'] = turn_guidance

    full_guided_path[f'From {current_vertex.getName()} to {nearest_vertex.getName()}'] = guided_path
    
    
    full_path.append(start_vertex) 

    
    path_names = [v.getName() for v in full_path]
    
    # Collect results  
    result_entry = {  
        'Path': path_names,  
        'Total_Distance': total_distance,  
        'Guidance': full_guidance,  
        'Guided_Path': full_guided_path  
    }  

    return result_entry  

# Example usage  
if __name__== "__main__":  

    vtx_list = load_vertices('data/vertices.xlsx')
    board = Board(obstacles_data)  
    initial_dir = (1,0) # Initial Direction of the car on the board
    min_result = nearest_neighbor_path(board, vtx_list, initial_dir)  



# Save all the results into folder
    output_dir = 'output/Nearest Neighbourhood'
    
    os.makedirs(output_dir, exist_ok=True)
    
    
    # Save as Json file
    output_file = f"output/Nearest Neighbourhood/optimal_path_{initial_dir}_nna.json"  

    output_data = {  
        'Optimal Path': {  
            'Path': min_result['Path'],  
            'Total Distance': min_result['Total_Distance'],  
            'Guidance': min_result['Guidance'],  
            'Guided Path': min_result['Guided_Path']  
        }  
    }  
    
    with open(output_file, 'w') as json_file:  
        json.dump(output_data, json_file, indent=4)  

    print(f"Results saved to {output_file}")  
    

    # Save the combined guidance
    output_file = f"output/Nearest Neighbourhood/optimal_guidance_{initial_dir}_nna.json"  
    
    combined_actions = []  
    guidance = min_result['Guidance']  


    for key in guidance:  
        combined_actions.extend(guidance[key]) 


    output_data = {  
        'Optimal Path': {  
            'Path': min_result['Path'],  
            'Total Distance': min_result['Total_Distance'],  
            'Combined Actions': combined_actions  # Final combined actions  
        }  
    }  
    
    # Write to a JSON file  
    with open(output_file, 'w') as json_file:  
        json.dump(output_data, json_file, indent=4)  # indent for pretty printing  

    print(f"Results saved to {output_file}")