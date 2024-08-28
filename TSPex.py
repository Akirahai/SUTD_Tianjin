from libs import *


    
# Exhaustive Search all possible paths, store in results 
def all_possible_paths(board, vtx_list, initial_dir):  
    
    results = []  
    start_vertex = vtx_list[0]  # Start at V(0,0) - 0


    vertices_to_permute = vtx_list[1:]  # Starting from the second vertex
    all_permutations = permutations(vertices_to_permute)  
        
        
    for perm in all_permutations:  
        # Create the full path starting and ending at V(0,0)  
        full_path = [start_vertex] + list(perm) + [start_vertex]  # Round trip to start  
        path_names = [v.getName() for v in full_path]  
        
        total_distance = 0  
        full_guidance = []  
        
        result_entry = analysis_full_optimized_paths(board,full_path, initial_dir)
        
        results.append(result_entry)
        
    return results  

# Compare them with total_distance value, return the minimum one
def ex_min_possible_path(board, vtx_list, initial_dir):
    
    all_paths_results = all_possible_paths(board, vtx_list, initial_dir)
    
    min_journey = float('inf')
    
    found_idx = 0
    found_result = []
    for idx, result in enumerate(all_paths_results):  
        if result['Total_Distance'] < min_journey:
            min_journey = result['Total_Distance']
            found_idx = idx + 1
            found_result = result
    
    return found_result
    


if __name__== "__main__":
    
    vtx_list = load_vertices('data/vertices.xlsx')
    board = Board(obstacles_data)  
    initial_dir = (0,1) # Initial Direction of the car on the board 
    min_result = ex_min_possible_path(board, vtx_list, initial_dir)
    
    
    
# Save all the results into folder
    output_dir = 'output/Exhaustive Search'
    
    os.makedirs(output_dir, exist_ok=True)
    
    
    # Save as Json file
    output_file = f"output/Exhaustive Search/optimal_path_{initial_dir}_ex.json"  
    
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
    output_file = f"output/Exhaustive Search/optimal_guidance_{initial_dir}_ex.json"  
    
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