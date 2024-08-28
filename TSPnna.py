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
    full_guidance = []  
    full_guided_path = [] 



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
            
            # Get guidance and guided guided_path for the move  
            full_guidance.append(f"From {current_vertex.getName()} to {nearest_vertex.getName()}: {turn_guidance}")

            full_guided_path.append(f'From {current_vertex.getName()} to {nearest_vertex.getName()}: {guided_path}')

            full_path.append(nearest_vertex)  
            
            visited[vtx_list.index(nearest_vertex)] = True  
            
            print(f' Found the nearest vertex next to {current_vertex} is {nearest_vertex}')
            
            current_vertex = nearest_vertex  
            checked_dir = last_direction
            
        

    # Return to starting point:  
    guided_path, distance_to_start, turn_guidance, last_direction = board.find_optimized_paths(checked_dir, current_vertex, start_vertex) 
    
    total_distance += distance_to_start  
    
    full_guidance.append(f"From {current_vertex.getName()} to {start_vertex.getName()}: {turn_guidance}")
        
    full_guided_path.append(f'From {current_vertex.getName()} to {start_vertex.getName()}: {guided_path}')
    
    
    full_path.append(start_vertex)  # Close the loop by going back to the start  

    
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
    
    df_vtx = pd.read_excel('data/vertices.xlsx')  
    vtx_list = []  
    # Create the list from the excel file and store it as a list of objects  
    for i in range(len(df_vtx)):  
        vtx = Vtx(df_vtx['Ver_Name'][i], df_vtx['x'][i], df_vtx['y'][i])  
        vtx_list.append(vtx)  




    board = Board(obstacles_data)  
    initial_dir = (1, 0)  
    min_result = nearest_neighbor_path(board, vtx_list, initial_dir)  

    print('The optimal guided_path given by the nearest neighbor algorithm is')  
    print(f"Path : {min_result['Path']}")  
    print(f"  Total Distance: {min_result['Total_Distance']}")  
    print(f"  Guidance:")  
    for guidance in min_result['Guidance']:  
        print(f"    - {guidance}")  
    print(f"  Guided_Path:")  
    for guidance in min_result['Guided_Path']:  
        print(f"    - {guidance}")  
    print()