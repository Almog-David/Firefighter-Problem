import pytest
import networkx as nx

@pytest.fixture
def sample_json_data():
    return {
        "Dirlay": {
            "Graph-1": {
                "vertices": [0, 1, 2, 3, 4, 5],
                "edges": [{"source": 0, "target": 1}, {"source": 0, "target": 2}]
            },
        },
        "RegularGraph": {
            "Graph-1": {
                "vertices": [0, 1, 2],
                "edges": [{"source": 0, "target": 1}, {"source": 1, "target": 2}]
            },
        }
    }
    
def test_source_not_in_graph():
    pass

def test_target_not_in_graph():
    pass

def test_source_is_target():
    pass

def test_calculate_gamma():
    pass

def test_calculate_epsilon():
    pass

def test_find_best_direct_vaccination():
    pass

def test_save_after_division():
    pass

def test_save_all_vertices():
    pass

def test_save_subgroup_vertices():
    pass