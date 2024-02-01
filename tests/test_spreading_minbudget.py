import pytest
import networkx as nx
import json

from src.Firefighter_Problem import spreading_minbudget
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

def get_graphs():
    with open("src/graphs.json", "r") as file:
        json_data = json.load(file)
    graphs = parse_json_to_networkx(json_data)
    return graphs

graphs =  get_graphs()
    
def test_source_not_in_graph():
    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        spreading_minbudget(graphs["RegularGraph_Graph-1"], -3, [1,0,4,5,2,6])

    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        spreading_minbudget(graphs["RegularGraph_Graph-4"], 10, [1,3,5,6,7])

    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        spreading_minbudget(graphs["RegularGraph_Graph-6"], 12, [9,2,3,4,6,7])

    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        spreading_minbudget(graphs["RegularGraph_Graph-8"], -1, [7,10,4,9,3,11,2])

    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        spreading_minbudget(graphs["RegularGraph_Graph-3"], 8, [1,4,2])
        

def test_target_not_in_graph():
    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        spreading_minbudget(graphs["RegularGraph_Graph-2"], 2, [0,4,5,11,6])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        spreading_minbudget(graphs["RegularGraph_Graph-3"], 3, [0,3,5,-1,1,2])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        spreading_minbudget(graphs["RegularGraph_Graph-6"], 7, [9,7,4,5,8,11])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        spreading_minbudget(graphs["RegularGraph_Graph-8"], 10, [0,2,4,5,8,11,12,3,15])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        spreading_minbudget(graphs["RegularGraph_Graph-7"], 1, [3,5,4,0,13])
        

def test_source_is_target():
    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,2,3,0,4,5,6])
    
    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        spreading_minbudget(graphs["RegularGraph_Graph-3"], 1, [5,1,4])
    
    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        spreading_minbudget(graphs["RegularGraph_Graph-4"], 4, [1,2,3,4,5,6,7])
    
    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        spreading_minbudget(graphs["RegularGraph_Graph-6"], 0, [0,3,5,6,7,8,9])

    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [13,10,8,6,5,4,3,0,1,2])

def test_calculate_gamma():
    pass

def test_calculate_epsilon():
    pass

def test_find_best_direct_vaccination():
    pass

def test_save_after_division():
    pass

def test_save_all_vertices():
    assert answer_1 == spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,2,3,4,5,6])
    assert answer_2 == spreading_minbudget(graphs["RegularGraph_Graph-2"], 0, [1,2,3,4,5,6,7])
    assert answer_1 != spreading_minbudget(graphs["RegularGraph_Graph-3"], 0, [1,2,3,4,5])
    assert answer_1 < spreading_minbudget(graphs["RegularGraph_Graph-4"], 0, [1,2,3,4,5,6,7])
    assert answer_1 > spreading_minbudget(graphs["RegularGraph_Graph-6"], 1, [0,2,3,4,5,6,7,8,9])
    assert answer_1 == spreading_minbudget(graphs["RegularGraph_Graph-7"], 1, [0,2,3,4,5,6])
    assert answer_1 != spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [1,2,3,4,5,6,7,8,9,10,11,12,13,14])
    
def test_save_subgroup_vertices():
    assert answer_1 != non_spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,5,6])
    assert answer_2 == non_spreading_minbudget(graphs["RegularGraph_Graph-2"], 0, [1,3,4,5,6])
    assert answer_1 > non_spreading_minbudget(graphs["RegularGraph_Graph-3"], 0, [1,2])
    assert answer_1 < non_spreading_minbudget(graphs["RegularGraph_Graph-4"], 0, [2,3,5,7])
    assert answer_1 > non_spreading_minbudget(graphs["RegularGraph_Graph-6"], 1, [0,3,5,6,8,9])
    assert answer_1 == non_spreading_minbudget(graphs["RegularGraph_Graph-7"], 1, [0,2,5,6])
    assert answer_1 == non_spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [1,3,4,5,6,9,10,12,14])
