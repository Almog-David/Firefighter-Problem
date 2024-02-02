import pytest
import networkx as nx
import json

from src.Firefighter_problem import non_spreading_dirlaynet_minbudget
from src.Utils import adjust_nodes_capacity
from src.Utils import create_st_graph
from src.Utils import parse_json_to_networkx

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


def test_adjust_nodes_capacity(): 
    """
    This test checks if the node capacity and layers are correct.
    """
    #Test 1
    graph_1 = graphs["Dirlay_Graph-1"]
    #layers check
    layers_1 = [[0], [1, 2], [3], [4], [5]]
    assert set(adjust_nodes_capacity(graph_1,0)) == layers_1
    #capacity check
    assert set(graph_1.nodes[1]['capacity']) == 1/(1*1/2)
    assert set(graph_1.nodes[2]['capacity']) == 1/(1*1/2)
    assert set(graph_1.nodes[3]['capacity']) == 1/(1*(1/2+1/3))
    assert set(graph_1.nodes[4]['capacity']) == 1/(1*(1/2+1/3+1/4))
    assert set(graph_1.nodes[5]['capacity']) == 1/(1*(1/2+1/3+1/4+1/5))

    #Test 2
    graph_2 = graphs["Dirlay_Graph-2"]
    #layers check
    layers_2 = [[0], [1, 2], [4, 3]]
    assert set(adjust_nodes_capacity(graph_2,2)) == layers_2
    #capacity check
    assert set(graph_2.nodes[1]['capacity']) == 1/(1*1/2)
    assert set(graph_2.nodes[2]['capacity']) == 1/(1*1/2)
    assert set(graph_2.nodes[3]['capacity']) == 1/(1*(1/2+1/3))
    assert set(graph_2.nodes[4]['capacity']) == 1/(1*(1/2+1/3))

    #Test 3
    graph_3 = graphs["Dirlay_Graph-3"]
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
    graph_4 = graphs["Dirlay_Graph-4"]
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
    graph_1 = graphs["Dirlay_Graph-1"]
    graph_1 = create_st_graph(graph_1,[1,2,3]) #want to save 1,2,3
    #edges check
    assert set(graph_1.__contains__("t")) == True
    assert set(graph_1.has_edge(1,"t")) == True
    assert set(graph_1.has_edge(2,"t")) == True
    assert set(graph_1.has_edge(3,"t")) == True

    #Test2
    graph_2 = graphs["Dirlay_Graph-2"]
    graph_2 = create_st_graph(graph_2,[2,4]) #want to save 2,4
    #edges check
    assert set(graph_2.__contains__("t")) == True
    assert set(graph_2.has_edge(2,"t")) == True
    assert set(graph_2.has_edge(4,"t")) == True

    #Test3
    graph_3 = create_st_graph(graph_3,[1,5,7]) #want to save 1,5,7
    #edges check
    assert set(graph_3.__contains__("t")) == True
    assert set(graph_3.has_edge(1,"t")) == True
    assert set(graph_3.has_edge(5,"t")) == True
    assert set(graph_3.has_edge(7,"t")) == True

    #Test4
    graph_4 = graphs["Dirlay_Graph-4"]
    graph_4 = create_st_graph(graph_4,[2,4,5,8]) #want to save 2,4,5,8
    #edges check
    assert set(graph_4.__contains__("t")) == True
    assert set(graph_4.has_edge(2,"t")) == True
    assert set(graph_4.has_edge(4,"t")) == True
    assert set(graph_4.has_edge(5,"t")) == True
    assert set(graph_4.has_edge(8,"t")) == True



def test_graph_flow_reduction(): return # validates if the redcution is correct.

def test_min_cut(): return #is that neccesarry to check as it is a part of networkX library.

def test_min_cut_N_groups(): return #this tests validates the nodes taken from the min-cut create the right groups (N_1...N_l)

# there is an important check to do here : A matrix is valid if : For any col j, the col sum is exactly |Nj|.
def test_upper_triangular_matrix(): return #checks that the calculations made to create the triangular matrix from the min-cut nodes is correct.

def test_integrability_of_matrix(): return #in case the matrix is not ingeral from previous step, we need to make it one (so vaccianation is correct- cant vaccinate 1/2 node)

def test_vaccination_process(): return #not 100% sure about this one, putting it here just in case we need.


