import pytest
import networkx as nx
import json

from src.Firefighter_Problem import spreading_minbudget
from src.Utils import parse_json_to_networkx, calculate_gamma, calculate_epsilon, find_best_direct_vaccination

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
        spreading_minbudget(graphs["RegularGraph_Graph-3"], 3, [0,4,5,-1,1,2])

    with pytest.raises(ValueError, match="Error: Not all nodes in the targets list are on the graph."):
        spreading_minbudget(graphs["RegularGraph_Graph-6"], 7, [9,2,4,5,8,11])

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

@pytest.mark.parametrize("graph_key, source, targets, expected_gamma, expected_direct_vaccination", [
    ("RegularGraph_Graph-4", 0, [1, 2, 3, 4, 5 ,6 ,7], {
        1: [(1, 1)],
        2: [(1, 1), (2, 1), (2, 2), (5, 1)],
        3: [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (5, 1), (5, 2), (6, 1)],
        4: [(1, 1), (2, 1), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (6, 1)],
        5: [(1, 1), (5, 1), (5, 2), (6, 1)],
        6: [(6, 1)],
        7: [],
    }, {
        (1, 1): [1, 2, 3, 4, 5, 7],
        (2, 1): [2, 3, 4, 7],
        (2, 2): [2, 3, 7],
        (3, 1): [3, 4, 7],
        (3, 2): [3, 4, 7],
        (3, 3): [3, 7],
        (4, 1): [4, 7],
        (4, 2): [4, 7],
        (4, 3): [4, 7],
        (5, 1): [2, 3, 4, 5, 7],
        (5, 2): [3, 4, 5, 7],
        (6, 1): [3, 4, 5, 6, 7]
    }),
    ("RegularGraph_Graph-1", 0, [1, 3, 4, 5], {
        1: [(1, 1)],
        2: [(2, 1)],
        3: [(1, 1), (2, 1), (3, 1), (3, 2)],
        4: [(1, 1), (4, 1), (4, 2)],
        5: [(1, 1), (2, 1), (3, 1), (3, 2), (5, 1), (5, 2), (5, 3)],
        6: [(2, 1), (6, 1), (6, 2)],
    }, {
        (1, 1): [1, 3, 4, 5],
        (2, 1): [2, 3, 5, 6],
        (3, 1): [3, 5],
        (3, 2): [3, 5],
        (4, 1): [4],
        (4, 2): [4],
        (5, 1): [5],
        (5, 2): [5],
        (5, 3): [5],
        (6, 1): [6],
        (6, 2): [6],
    })
])
def test_calculate_gamma(graph_key, source, targets, expected_gamma, expected_direct_vaccination):
    calculated_gamma, calculated_direct_vaccination = calculate_gamma(graphs[graph_key], source, targets)
    
    assert calculated_gamma == expected_gamma
    assert calculated_direct_vaccination == expected_direct_vaccination


@pytest.mark.parametrize("direct_vaccinations, expected_epsilon", [
    ({
        (1, 1): [1, 2, 3, 4, 5, 7],
        (2, 1): [2, 3, 4, 7],
        (2, 2): [2, 3, 7],
        (3, 1): [3, 4, 7],
        (3, 2): [3, 4, 7],
        (3, 3): [3, 7],
        (4, 1): [4, 7],
        (4, 2): [4, 7],
        (4, 3): [4, 7],
        (5, 1): [2, 3, 4, 5, 7],
        (5, 2): [3, 4, 5, 7],
        (6, 1): [3, 4, 5, 6, 7],
    }, [
        {(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)},
        {(2, 2), (3, 2), (4, 2), (5, 2)},
        {(3, 3), (4, 3)}
    ]),
    ({
        (1, 1): [1],
        (1, 2): [1],
        (2, 1): [1, 2, 3],
        (3, 1): [3],
        (3, 2): [3],
        (4, 1): [1, 4, 6, 8],
        (5, 1): [3, 5, 6, 7, 8],
        (6, 1): [4, 6, 8],
        (6, 2): [6, 8],
        (7, 1): [7, 8],
        (7, 2): [7, 8],
        (8, 1): [8],
        (8, 2): [8],
        (8, 3): [8],
    }, [
        {(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)},
        {(1, 2), (3, 2), (6, 2), (7, 2), (8, 2)},
        {(8, 3)}
    ]),
])
def test_calculate_epsilon(direct_vaccinations, expected_epsilon):
    calculated_epsilon = calculate_epsilon(direct_vaccinations)
    
    assert calculated_epsilon == expected_epsilon

@pytest.mark.parametrize("graph_key, direct_vaccinations, current_epsilon, targets, expected_best_direct_vaccination", [
    ("RegularGraph_Graph-1",
     {
     (1, 1): [1, 2, 3, 4, 5, 7],
        (2, 1): [2, 3, 4, 7],
        (2, 2): [2, 3, 7],
        (3, 1): [3, 4, 7],
        (3, 2): [3, 4, 7],
        (3, 3): [3, 7],
        (4, 1): [4, 7],
        (4, 2): [4, 7],
        (4, 3): [4, 7],
        (5, 1): [2, 3, 4, 5, 7],
        (5, 2): [3, 4, 5, 7],
        (6, 1): [3, 4, 5, 6, 7],
    }, 
    [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
    [1, 3, 4, 5, 6], 
    (1, 1)),
    ("Dirlay_Graph-5", 
     {
        (1, 1): [1],
        (1, 2): [1],
        (2, 1): [1, 2, 3],
        (3, 1): [3],
        (3, 2): [3],
        (4, 1): [1, 4, 6, 8],
        (5, 1): [3, 5, 6, 7, 8],
        (6, 1): [4, 6, 8],
        (6, 2): [6, 8],
        (7, 1): [7, 8],
        (7, 2): [7, 8],
        (8, 1): [8],
        (8, 2): [8],
        (8, 3): [8],
    }, 
    [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)],
    [1, 2, 3, 4, 5, 6, 7, 8],
    (5, 1))
])
    
def test_find_best_direct_vaccination(graph_key, direct_vaccinations, current_epsilon, targets, expected_best_direct_vaccination):
    calculated_best_direct_vaccination = find_best_direct_vaccination(graphs[graph_key],direct_vaccinations,current_epsilon,targets)
    
    assert calculated_best_direct_vaccination == expected_best_direct_vaccination

def test_save_all_vertices():
    assert 2 == spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,2,3,4,5,6]) # answer is 2
    assert 2 == spreading_minbudget(graphs["RegularGraph_Graph-2"], 0, [1,2,3,4,5,6,7]) # answer is 2
    assert 3 != spreading_minbudget(graphs["RegularGraph_Graph-3"], 0, [1,2,3,4,5]) # answer is 2
    assert spreading_minbudget(graphs["RegularGraph_Graph-2"], 0, [1,2,3,4,5,6,7]) > spreading_minbudget(graphs["RegularGraph_Graph-4"], 0, [1,2,3,4,5,6,7]) # answer is 2 
    assert spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,2,3,4,5,6]) > spreading_minbudget(graphs["RegularGraph_Graph-6"], 1, [0,2,3,4,5,6,7,8,9]) # answer is 1
    assert 3 == spreading_minbudget(graphs["RegularGraph_Graph-7"], 1, [0,2,3,4,5,6]) # answer is 3 
    assert 2 != spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [1,2,3,4,5,6,7,8,9,10,11,12,13,14]) # answer is 4
    

def test_save_subgroup_vertices():
    assert spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,2,3,4,5,6]) != spreading_minbudget(graphs["RegularGraph_Graph-1"], 0, [1,5,6]) # answer is 1 
    assert 1 == spreading_minbudget(graphs["RegularGraph_Graph-2"], 0, [1,3,4,5,6]) #answer is 1 
    assert spreading_minbudget(graphs["RegularGraph_Graph-3"], 0, [1,2,3,4,5]) > spreading_minbudget(graphs["RegularGraph_Graph-3"], 0, [1,3,5]) #answer is 1
    assert 2 > spreading_minbudget(graphs["RegularGraph_Graph-4"], 0, [2,3,5,7]) # anser is 1 
    assert 4 > spreading_minbudget(graphs["RegularGraph_Graph-6"], 1, [0,3,5,6,8,9]) #answer is 1 
    assert 2 == spreading_minbudget(graphs["RegularGraph_Graph-7"], 1, [4,2,5,6]) #answer is 2 
    assert spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [1,2,3,4,5,6,7,8,9,10,11,12,13,14]) != spreading_minbudget(graphs["RegularGraph_Graph-8"], 0, [1,3,4,5,6,9,10,12,14]) #answer is 3