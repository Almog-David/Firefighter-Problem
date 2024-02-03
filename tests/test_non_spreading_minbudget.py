import pytest
import networkx as nx
import json

from src.Firefighter_Problem import non_spreading_minbudget
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
        non_spreading_minbudget(graphs["RegularGraph_Graph-1"], -2, [1,2,3,4,5,6])

    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-4"], 8, [1,2,4,6,7])

    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-6"], 10, [0,2,3,5,6,7,8,9])

    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-8"], 17, [1,7,12,14,8,3,11,2])

    with pytest.raises(ValueError, match="Error: The source node isn't on the graph"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-3"], 6, [1,3,5])
        

def test_target_not_in_graph():
    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        non_spreading_minbudget(graphs["RegularGraph_Graph-2"], 0, [1,2,3,9,5,16])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        non_spreading_minbudget(graphs["RegularGraph_Graph-3"], 4, [1,2,3,6,7])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        non_spreading_minbudget(graphs["RegularGraph_Graph-6"], 3, [0,2,5,6,7,8,10])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        non_spreading_minbudget(graphs["RegularGraph_Graph-8"], 11, [1,3,12,19,8,10,4,2])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        non_spreading_minbudget(graphs["RegularGraph_Graph-7"], 2, [1,3,-1,5])
        

def test_source_is_target():
    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,2,3,0,4,5,6])
    
    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-3"], 1, [5,1,4])
    
    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-4"], 4, [1,2,3,4,5,6,7])
    
    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-6"], 0, [0,3,5,6,7,8,9])

    with pytest.raises(ValueError, match="Error: The source node can't be a part of the targets list, since the virus is spreading from the source"):
        non_spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [13,10,8,6,5,4,3,0,1,2])

def test_save_all_vertices():
    assert 2 == non_spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,2,3,4,5,6]) #answer is 2
    assert 2 == non_spreading_minbudget(graphs["RegularGraph_Graph-2"], 0, [1,2,3,4,5,6,7]) #answer is 2
    assert 3 != non_spreading_minbudget(graphs["RegularGraph_Graph-3"], 0, [1,2,3,4,5]) #answer is 2
    assert 2 > non_spreading_minbudget(graphs["RegularGraph_Graph-4"], 0, [1,2,3,4,5,6,7]) #answer is 1
    assert 1 < non_spreading_minbudget(graphs["RegularGraph_Graph-6"], 1, [0,2,3,4,5,6,7,8,9]) #answer is 3 
    assert 3 == non_spreading_minbudget(graphs["RegularGraph_Graph-7"], 1, [0,2,3,4,5,6]) #answer is 3
    assert 2 != non_spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [1,2,3,4,5,6,7,8,9,10,11,12,13,14]) #answer is 3

def test_save_subgroup_vertices():
    assert 1 != non_spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,5,6]) #answer is 2
    assert 1 == non_spreading_minbudget(graphs["RegularGraph_Graph-2"], 0, [1,3,4,5,6]) #answer is 1
    assert 3 > non_spreading_minbudget(graphs["RegularGraph_Graph-3"], 0, [1,2]) #answer is 2
    assert 1 < non_spreading_minbudget(graphs["RegularGraph_Graph-4"], 0, [2,3,5,7]) #answer is 2
    assert 4 > non_spreading_minbudget(graphs["RegularGraph_Graph-6"], 1, [0,3,5,6,8,9]) #answer is 1
    assert 2 == non_spreading_minbudget(graphs["RegularGraph_Graph-7"], 1, [0,2,5,6]) #answer is 2
    assert 3 == non_spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [1,3,4,5,6,9,10,12,14]) #answer is 3

def test_correct_st_cut(): 
    pass