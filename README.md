# EX and NNA TSP Project  

This project implements the Exhaustive Search (EX) Nearest Neighbor Algorithm (NNA) for solving the Traveling Salesman Problem (TSP). The project consists of two main scripts: `TSPnna.py` for running the NNA algorithm and `TSPex.py` for running EX algorithm.  

## Prerequisites  

You install the required libraries using pip with requirements:  

```bash  
pip install requirements.txt
```  

## Running the Scripts  

### To change the count of seconds for the car to run in each kinds of line and the turning time, refer to the libs.py

### To run the Branch and Bound Algorithm (BB):

```bash  
python TSPbb.py  
```

### To run the Nearest Neighbor Algorithm (NNA):  

```bash  
python TSPnna.py  
```  

### To run the Exhaustive Search Algorithm (EX):  

```bash  
python TSPex.py  
```  

## Output  

The outputs of both scripts will all be saved into the folder `output` You can find all the necessary file in the same directory where the scripts are located.  

## Result Comparison

After implementing all three algorithm, I created the main.py to run through all the three algorithms to make comparison of their performance based on the total distance and execution time. 

The result can be seen as below with the 6 vertices according to our challenge:

**Comparison of TSP Algorithms at the initial direction (0,1):**

| Algorithm                            | Total Distance | Time (seconds) |  
|--------------------------------------|----------------|-----------------|  
| TSP Branch and Bound                 | 50.17          | 2.338           |  
| TSP Nearest Neighborhood    | 55.10          | 0.036           |  
| TSP Exhaustive Search                | 50.17          | 7.861           | 

To run the programme to compare between each algorithm, you can follow the script below:

```bash  
python main.py  
```

