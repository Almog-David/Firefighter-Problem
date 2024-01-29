import networkx as nx
import pytest
import sys
import os

from src.Utils import *

@pytest.fixture
def test_graph():
    """
    Create a pre-determined graph for testing, minimizes code duplication in tests - this is called at the beginning of each test
    """
    pass

@pytest.fixture
def test_dirlay():
    """
    Create a pre-determined directed layered network for testing.
    """
    pass

def test_validate_parameters(test_graph):
    pass

def test_spread_virus(test_graph):
    pass

def test_spread_vaccination(test_graph):
    pass

def test_vaccinate_node(test_graph):
    pass

def test_clean_graph(test_graph):
    pass

def test_adjust_nodes_capacity(test_graph):
    pass

def test_create_st_graph(test_graph):
    pass

def test_flow_reduction(test_graph):
    pass

def test_calculate_vaccine_matrix(test_dirlay):
    pass

def test_display_graph(test_graph):
    pass