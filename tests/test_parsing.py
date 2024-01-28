import pytest
import networkx as nx

from src.Utils import parse_json_to_networkx

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
    
@pytest.fixture
def missing_vertices_json():
    return {
        "InvalidGraph": {
            "Graph-1": {
                "edges": [{"source": 0, "target": 1}, {"source": 1, "target": 2}]
            }
        }
    }

@pytest.fixture
def missing_edges_json():
    return {
        "InvalidGraph": {
            "Graph-2": {
                "vertices": [0, 1, 2]
            }
        }
    }
    
@pytest.fixture
def empty_json():
    return {
        "InvalidGraph": {
            "Graph-3": {
                "vertices": [],
                "edges": []
            }
        }
    }
    
def test_parsing(sample_json_data):
    graphs = parse_json_to_networkx(sample_json_data)

    assert isinstance(graphs["Dirlay_Graph-1"], nx.DiGraph)
    assert set(graphs["Dirlay_Graph-1"].nodes()) == {0, 1, 2, 3, 4, 5}
    assert set(graphs["Dirlay_Graph-1"].edges()) == {(0, 1), (0, 2)}

    assert isinstance(graphs["RegularGraph_Graph-1"], nx.Graph)
    assert set(graphs["RegularGraph_Graph-1"].nodes()) == {0, 1, 2}
    assert set(graphs["RegularGraph_Graph-1"].edges()) == {(0, 1), (1, 2)}
    
        
def test_parse_exceptions(missing_vertices_json, missing_edges_json, empty_json):
    
    with pytest.raises(KeyError):
        parse_json_to_networkx(missing_vertices_json)

    with pytest.raises(KeyError):
        parse_json_to_networkx(missing_edges_json)

    with pytest.raises(KeyError):
        parse_json_to_networkx(empty_json)