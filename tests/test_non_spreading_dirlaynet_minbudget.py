import pytest
import networkx as nx
import json

from src.Firefighter_problem import non_spreading_dirlaynet_minbudget
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


def test_nodes_capacity(): return # checks if the node capacity is correct.

def test_reduction(): return # validates if the redcution is correct.

def test_min_cut(): return #is that neccesarry to check as it is a part of networkX library.

def test_min_cut_N_groups(): return #this tests validates the nodes taken from the min-cut create the right groups (N_1...N_l)

# there is an important check to do here : A matrix is valid if : For any col j, the col sum is exactly |Nj|.
def test_upper_triangular_matrix(): return #checks that the calculations made to create the triangular matrix from the min-cut nodes is correct.

def test_integrability_of_matrix(): return #in case the matrix is not ingeral from previous step, we need to make it one (so vaccianation is correct- cant vaccinate 1/2 node)

def test_vaccination_process(): return #not 100% sure about this one, putting it here just in case we need.


