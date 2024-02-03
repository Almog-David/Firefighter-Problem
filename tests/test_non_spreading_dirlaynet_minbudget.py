import pytest
import networkx as nx
import json

from src.Firefighter_problem import non_spreading_dirlaynet_minbudget
from src.Utils import adjust_nodes_capacity
from src.Utils import create_st_graph
from src.Utils import parse_json_to_networkx
from src.Utils import graph_flow_reduction
from src.Utils import calculate_vaccine_matrix
from src.Utils import min_cut_N_groups
from src.Utils import matrix_to_integers_values
from src.Utils import min_budget_calculation

@pytest.fixture
def sample_json_data(): return

def get_graphs(): 
    with open("src/graphs.json", "r") as file:
        json_data = json.load(file)
    graphs = parse_json_to_networkx(json_data = json_data)
    return graphs

graphs = get_graphs() 

def test_source_not_in_graph(): 
    """
    This test checks if the source node is not a real node in the graph.
    """
    with pytest.raises(ValueError, match = "Error: The source node is not on the graph"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-1"], -3 [0,5])

    with pytest.raises(ValueError, match = "Error: The source node is not on the graph"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-2"], 13 [0,1,4])
    
    with pytest.raises(ValueError, match = "Error: The source node is not on the graph"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-3"], 15 [0,6,7])

    with pytest.raises(ValueError, match = "Error: The source node is not on the graph"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-4"], -1 [1,3,5,7])

     
def test_target_not_in_graph():
    """
    This test checks if a node we're trying to save is not in the graph.
    """
    with pytest.raises(ValueError, match = "Error: Not all nodes we're trying to save are on the graph"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-1"], 0 [1,5,7]) #7#

    with pytest.raises(ValueError, match = "Error: Not all nodes we're trying to save are on the graph"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-2"], 1 [0,2,-1,9]) #-1,9#
    
    with pytest.raises(ValueError, match = "Error: Not all nodes we're trying to save are on the graph"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-3"], 4 [0,1,2,11,12,13,14]) #11,12,13,14#

    with pytest.raises(ValueError, match = "Error: Not all nodes we're trying to save are on the graph"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-4"], 0 [1,3,5,7,15,20]) #15,20#


def test_source_is_target():
    """
    This test checks if we're trying to save a source node.
    """
    with pytest.raises(ValueError, match = "Error: The source node can not be a part of the targets vector"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-1"], 0 [0,5])

    with pytest.raises(ValueError, match = "Error: The source node can not be a part of the targets vector"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-2"], 1 [0,1,4])
    
    with pytest.raises(ValueError, match = "Error: The source node can not be a part of the targets vector"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-3"], 6 [0,6,7])

    with pytest.raises(ValueError, match = "Error: The source node can not be a part of the targets vector"):
        non_spreading_dirlaynet_minbudget(graphs["Dirlay_Graph-4"], 3 [1,3,5,7])
    

#Test 1
#graph building
graph_1 = graphs["Dirlay_Graph-1"]
layers_1 = adjust_nodes_capacity(graph_1,0)
targets_1 = [1,2,3] #saving 1,2,3
G1 = create_st_graph(graph_1, targets_1)
reduction_G1 = graph_flow_reduction(G1,0)
N_1_groups = min_cut_N_groups(reduction_G1)
matrix_1 = calculate_vaccine_matrix(layers_1,N_1_groups)
integer_matrix_1 = matrix_to_integers_values(matrix_1)
min_budget_1 = min_budget_calculation(integer_matrix_1)

#Test 2
#graph building
graph_2 = graphs["Dirlay_Graph-2"]
layers_2 = adjust_nodes_capacity(graph_2,0) #src is 2
targets_2 = [2,4] #saving 2,4
G2 = create_st_graph(graph_2, targets_2)
reduction_G2 = graph_flow_reduction(G2,0) 
N_2_groups = min_cut_N_groups(reduction_G2)
matrix_2 = calculate_vaccine_matrix(layers_2,N_2_groups)
integer_matrix_2 = matrix_to_integers_values(matrix_2)
min_budget_2 = min_budget_calculation(integer_matrix_2)

#Test 3
#graph building
graph_3 = graphs["Dirlay_Graph-3"]
layers_3 = adjust_nodes_capacity(graph_3,0) #src is 0
targets_3 = [1,5,7] #saving 1,5,7
G3 = create_st_graph(graph_3, targets_3)
reduction_G3 = graph_flow_reduction(G3,0)
N_3_groups = min_cut_N_groups(reduction_G3)
matrix_3 = calculate_vaccine_matrix(layers_3,N_3_groups)
integer_matrix_3 = matrix_to_integers_values(matrix_3)
min_budget_3 = min_budget_calculation(integer_matrix_3)

#Test 4
#graph building
graph_4= graphs["Dirlay_Graph-4"]
layers_4 = adjust_nodes_capacity(graph_4,0) #src is 0
targets_4 = [4,5,6,8] #saving 4,5,6,8
G4 = create_st_graph(graph_4, targets_4)
reduction_G4 = graph_flow_reduction(G4,0)
N_4_groups = min_cut_N_groups(reduction_G4)
matrix_4 = calculate_vaccine_matrix(layers_4,N_4_groups)
integer_matrix_4 = matrix_to_integers_values(matrix_4)
min_budget_4 = min_budget_calculation(integer_matrix_4)


def test_adjust_nodes_capacity(): 
    """
    This test checks if the node capacity and layers are correct.
    """
    #Test 1
    #layers check
    layers_1_check = [[0], [1, 2], [3], [4], [5]]
    assert set(adjust_nodes_capacity(graph_1,0)) == layers_1_check
    #capacity check
    assert set(graph_1.nodes[1]['capacity']) == 1/(1*1/2)
    assert set(graph_1.nodes[2]['capacity']) == 1/(1*1/2)
    assert set(graph_1.nodes[3]['capacity']) == 1/(1*(1/2+1/3))
    assert set(graph_1.nodes[4]['capacity']) == 1/(1*(1/2+1/3+1/4))
    assert set(graph_1.nodes[5]['capacity']) == 1/(1*(1/2+1/3+1/4+1/5))

    #Test 2
    #layers check
    layers_2 = [[0], [1, 2], [4, 3]]
    assert set(adjust_nodes_capacity(graph_2,2)) == layers_2
    #capacity check
    assert set(graph_2.nodes[1]['capacity']) == 1/(1*1/2)
    assert set(graph_2.nodes[2]['capacity']) == 1/(1*1/2)
    assert set(graph_2.nodes[3]['capacity']) == 1/(1*(1/2+1/3))
    assert set(graph_2.nodes[4]['capacity']) == 1/(1*(1/2+1/3))

    #Test 3
    #layers check
    layers_3 = [[0], [1, 2, 3], [5, 4], [6, 7]]
    assert set(adjust_nodes_capacity(graph_3,0)) == layers_3
    #capacity check
    assert set(graph_3.nodes[1]['capacity']) == 1/(1*1/2)
    assert set(graph_3.nodes[2]['capacity']) == 1/(1*1/2)
    assert set(graph_3.nodes[3]['capacity']) == 1/(1*1/2)
    assert set(graph_3.nodes[4]['capacity']) == 1/(1*(1/2+1/3))
    assert set(graph_3.nodes[5]['capacity']) == 1/(1*(1/2+1/3))
    assert set(graph_3.nodes[6]['capacity']) == 1/(1*(1/2+1/3+1/4))
    assert set(graph_3.nodes[7]['capacity']) == 1/(1*(1/2+1/3+1/4))

    #Test 4
    #layers check
    layers_4 = [[0], [1, 2], [3, 4], [5], [6], [8]]
    assert set(adjust_nodes_capacity(graph_4,0)) == layers_4
    #capacity check
    assert set(graph_4.nodes[1]['capacity']) == 1/(1*1/2)
    assert set(graph_4.nodes[2]['capacity']) == 1/(1*1/2)
    assert set(graph_4.nodes[3]['capacity']) == 1/(1*(1/2+1/3))
    assert set(graph_4.nodes[4]['capacity']) == 1/(1*(1/2+1/3))
    assert set(graph_4.nodes[5]['capacity']) == 1/(1*(1/2+1/3+1/4))
    assert set(graph_4.nodes[6]['capacity']) == 1/(1*(1/2+1/3+1/4+1/5))
    assert set(graph_4.nodes[8]['capacity']) == 1/(1*(1/2+1/3+1/4+1/5+1/6))

def test_create_st_graph() : 
    """
    creates the s-t graph and connects the nodes we want to save
    """
    #Test1
    #edges check
    assert set(graph_1.__contains__("t")) == True
    assert set(graph_1.has_edge(1,"t")) == True
    assert set(graph_1.has_edge(2,"t")) == True
    assert set(graph_1.has_edge(3,"t")) == True

    #Test2
    #edges check
    assert set(graph_2.__contains__("t")) == True
    assert set(graph_2.has_edge(2,"t")) == True
    assert set(graph_2.has_edge(4,"t")) == True

    #Test3
    #edges check
    assert set(graph_3.__contains__("t")) == True
    assert set(graph_3.has_edge(1,"t")) == True
    assert set(graph_3.has_edge(5,"t")) == True
    assert set(graph_3.has_edge(7,"t")) == True

    #Test4
    #edges check
    assert set(graph_4.__contains__("t")) == True
    assert set(graph_4.has_edge(4,"t")) == True
    assert set(graph_4.has_edge(5,"t")) == True
    assert set(graph_4.has_edge(6,"t")) == True
    assert set(graph_4.has_edge(8,"t")) == True

def test_graph_flow_reduction():  #TBD
    """
    This test validates if the redcution is correct.
    """
    pass

def test_min_cut_N_groups(): 
    """
    This test validates the nodes taken from the min-cut create the right groups (N_1...N_l)
    """
    #Test 1 
    #checking equality
    N1_groups_check = [{1, 2}, set(), set(), set()]
    assert set(min_cut_N_groups(reduction_G1)) == N1_groups_check

    #Test 2
    #checking equality
    N2_groups_check = [{2},{4}]
    assert set(min_cut_N_groups(reduction_G2)) == N2_groups_check

    #Test 3
    #checking equality
    N3_groups_check = [{1},set(),{7}]
    assert set(min_cut_N_groups(reduction_G3)) == N3_groups_check
    
def test_calculate_vaccine_matrix(): 
    """
        There is an important check to do here : A matrix is valid if : For any col j, the col sum is exactly |Nj|.
        This test checks that the calculations made to create the triangular matrix from the min-cut nodes is correct.
    """
    #Test 1
    #checking equality
    matrix_1 = [[2,0,0,0]
                [0,0,0,0]
                [0,0,0,0]
                [0,0,0,0]]
    assert set(calculate_vaccine_matrix(layers_1,N_1_groups)) == matrix_1

    #Test 2
    #checking equality
    matrix_2 = [[1.5, 0.5]
                [1, 0.5]
                [0,0.5]]
    assert set(calculate_vaccine_matrix(layers_2,N_2_groups)) == matrix_2

    #Test 3
    #checking equality
    matrix_3 = [[1+1/3, 1/3, 1/3]
                [  1,   0,   1/3]
                [  0,   0,   1/3]]
    assert set(calculate_vaccine_matrix(layers_3,N_3_groups)) == matrix_3


    #Test 4
    #checking equality
    matrix_4 = [[5/6, 5/6, 1/3, 0, 0]
                [  0, 0.5, 1/3, 0 ,0]
                [  0, 0.5, 1/3, 0 ,0]
                [  0,  0,  1/3, 0 ,0]
                [  0,  0,  0,   0, 0]
                [  0,  0,  0,   0, 0]]
    assert set(calculate_vaccine_matrix(layers_4,N_4_groups)) == matrix_4
    

def test_matrix_to_integers_values(): 
    pass #in case the matrix is not ingeral from previous step, we need to make it one (so vaccianation is correct- cant vaccinate fractional node)

def test_min_budget_calculation():
    """
    This test validates that the minbudget is accurate
    """