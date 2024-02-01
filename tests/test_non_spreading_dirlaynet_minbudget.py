import pytest
import networkx as nx
import json

from src.Firefighter_problem import non_spreading_dirlaynet_minbudget
from src.Utils import parse_json_to_networkx

@pytest.fixture
def sample_json_data(): return

def get_graphs(): return

def test_source_not_in_graph(): return #checks if the source node is not a real node in the graph.

def test_target_not_in_graph(): return #checks if a node we're trying to save is not in the graph.

def test_source_is_target(): return #checks if we're trying to save a source node.

def test_nodes_capacity(): return # checks if the node capacity is correct.

def test_reduction(): return # validates if the redcution is correct.

def test_min_cut(): return #is that neccesarry to check as it is a part of networkX library.

def test_min_cut_N_groups(): return #this tests validates the nodes taken from the min-cut create the right groups (N_1...N_l)

# there is an important check to do here : A matrix is valid if : For any col j, the col sum is exactly |Nj|.
def test_upper_triangular_matrix(): return #checks that the calculations made to create the triangular matrix from the min-cut nodes is correct.

def test_integrability_of_matrix(): return #in case the matrix is not ingeral from previous step, we need to make it one (so vaccianation is correct- cant vaccinate 1/2 node)

def test_vaccination_process(): return #not 100% sure about this one, putting it here just in case we need.


