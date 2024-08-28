from libs import *






# Function to analyze a full_paths going through 5 points
def analysis_full_optimized_paths(board,full_path, dir):
    checked_dir = dir
    full_guidance = {}
    full_guided_path = {}
    path_names = [v.getName() for v in full_path] 
    total_distance = 0
    
    
    for i in range(len(full_path)- 1):
        start_vtx = full_path[i]  
        end_vtx = full_path[i + 1]
        
        guided_path, distance, turn_guidance, last_direction = board.find_optimized_paths(checked_dir, start_vtx, end_vtx)
        
        total_distance += distance
        
        full_guidance[f'From {start_vtx.getName()} to {end_vtx.getName()}'] = turn_guidance

        full_guided_path[f'From {start_vtx.getName()} to {end_vtx.getName()}'] = guided_path
        
        checked_dir = last_direction
        
        
    result_entry = {  
        'Path': path_names,  
        'Total_Distance': total_distance,  
        'Guidance': full_guidance,
        'Guided_Path': full_guided_path
    }
    
    return result_entry
    
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
def min_possible_path(board, vtx_list, initial_dir):
    
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
    
    df_vtx = pd.read_excel('data/vertices.xlsx')
    vtx_list = []
    # Create the list from the excel filde and stor it as list of objects
    for i in range(len(df_vtx)):
        vtx = Vtx(df_vtx['Ver_Name'][i], df_vtx['x'][i], df_vtx['y'][i])
        vtx_list.append(vtx)
    
    
    board = Board(obstacles_data)  
    initial_dir = (1,0)  
    min_result = min_possible_path(board, vtx_list, initial_dir)
    
    # print('The optimal path given by the exhaustive search algorithm is')
    # print(f"Path : {min_result['Path']}")  
    # print(f"  Total Distance: {min_result['Total_Distance']}")  
    # print(f"  Guidance:")  
    # for guidance in min_result['Guidance']:  
    #     print(f"    - {guidance}")  
    # print(f"  Guided_Path:")
    # for guidance in min_result['Guided_Path']:
    #     print(f"    - {guidance}")
    # print()
    
    output_dir = 'output/Exhaustive Search'
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"output/Exhaustive Search/optimal_path_{initial_dir}_ex.txt"  
    
    with open(output_file, 'w') as file:  
        file.write('The optimal path given by the exhaustive search algorithm is\n')  
        file.write(f"Path : {min_result['Path']}\n")  
        file.write(f"  Total Distance: {min_result['Total_Distance']}\n")  
        file.write(f"  Guidance:\n")  
        for guidance in min_result['Guidance']:  
            file.write(f"    - {guidance}\n")  
        file.write(f"  Guided_Path:\n")  
        for guidance in min_result['Guided_Path']:  
            file.write(f"    - {guidance}\n")  
    
    print(f"Results saved to {output_file}")  
    
    
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

    # Iterate through the Guidance structure and collect actions  
    for key in guidance:  
        combined_actions.extend(guidance[key])  # Add all actions for each segment  

    # Prepare data for JSON  
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