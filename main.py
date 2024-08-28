import time  

from libs import *
from TSPex import *
from TSPnna import *
from TSPbb import *


def load_vertices(file_path):  
    df_vtx = pd.read_excel(file_path)  
    vtx_list = []  
    for i in range(len(df_vtx)):  
        vtx = Vtx(df_vtx['Ver_Name'][i], df_vtx['x'][i], df_vtx['y'][i])  
        vtx_list.append(vtx)  
    return vtx_list  

def run_algorithms(vertices, board, initial_direction):  
    results = []  

    # Run TSP Branch and Bound  
    start_time = time.time()  
    tsp_bb_solver = TSPBranchAndBound(board, vertices, initial_direction)  
    min_result_bb = tsp_bb_solver.solve()  
    elapsed_time_bb = time.time() - start_time  

    results.append({  
        'Algorithm': 'TSP Branch and Bound',  
        'Total Distance': min_result_bb['Total_Distance'],  
        'Time (seconds)': elapsed_time_bb  
    })  

    # Run TSP Nearest Neighbor Approximation  
    start_time = time.time()  
    min_result_nna = nearest_neighbor_path(board, vertices, initial_direction)  
    elapsed_time_nna = time.time() - start_time  

    results.append({  
        'Algorithm': 'TSP Nearest Neighborhood',  
        'Total Distance': min_result_nna['Total_Distance'],  
        'Time (seconds)': elapsed_time_nna  
    })  
    
    
    # Run TSP Exhaustive Search
    start_time = time.time()
    min_result_ex = ex_min_possible_path(board, vertices, initial_direction)
    elapsed_time_ex = time.time() - start_time
    
    results.append({
        'Algorithm': 'TSP Exhaustive Search',
        'Total Distance': min_result_ex['Total_Distance'],
        'Time (seconds)': elapsed_time_ex
    })

    return results  

def main():
    vtx_list = load_vertices('data/vertices.xlsx') 
    board = Board(obstacles_data)  
    initial_dir = (1,0) # Initial Direction of the car on the board

    # Run all 3 algorithms  
    results = run_algorithms(vtx_list, board, initial_dir)  

    results_df = pd.DataFrame(results)  
    
    # Print the comparison of TSP Algorithms 
    print(f"Comparison of TSP Algorithms at the initial direction {initial_dir}:")  
    print(results_df)  

if __name__ == "__main__":  
    main()