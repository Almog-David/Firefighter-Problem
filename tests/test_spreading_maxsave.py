import pytest
import networkx as nx
import json

from src.Firefighter_Problem import spreading_maxsave
from src.Utils import parse_json_to_networkx, calculate_gamma, calculate_epsilon, find_best_direct_vaccination

with open("src/graphs.json", "r") as file:
        json_data = json.load(file)
graphs = parse_json_to_networkx(json_data)

@pytest.mark.parametrize("graph_key, budget, source, targets", [
    ("RegularGraph_Graph-1", 1, -2, [1, 2, 3, 4, 5, 6]),
    ("RegularGraph_Graph-4", 1, 8, [1, 2, 4, 6, 7]),
    ("RegularGraph_Graph-6", 1, 10, [0, 2, 3, 5, 6, 7, 8, 9]),
    ("RegularGraph_Graph-8", 1, 17, [1, 7, 12, 14, 8, 3, 11, 2]),
    ("RegularGraph_Graph-3", 1, 6, [1, 3, 5]),
])
def test_source_not_in_graph(graph_key, budget, source, targets):
    with pytest.raises(ValueError):
        spreading_maxsave(graphs[graph_key], budget, source, targets)

@pytest.mark.parametrize("graph_key, budget, source, targets", [
    ("RegularGraph_Graph-2", 1, 0, [1, 2, 3, 9, 5, 16]),
    ("RegularGraph_Graph-3", 1, 4, [1, 2, 3, 6, 7]),
    ("RegularGraph_Graph-6", 1, 3, [0, 2, 5, 6, 7, 8, 10]),
    ("RegularGraph_Graph-8", 1, 11, [1, 3, 12, 19, 8, 10, 4, 2]),
    ("RegularGraph_Graph-7", 1, 2, [1, 3, -1, 5]),
])
def test_target_not_in_graph(graph_key, budget, source, targets):
    with pytest.raises(ValueError):
        spreading_maxsave(graphs[graph_key], budget, source, targets)

@pytest.mark.parametrize("graph_key, budget, source, targets", [
    ("RegularGraph_Graph-1", 1, 0, [1, 2, 3, 0, 4, 5, 6]),
    ("RegularGraph_Graph-3", 1, 1, [5, 1, 4]),
    ("RegularGraph_Graph-4", 1, 4, [1, 2, 3, 4, 5, 6, 7]),
    ("RegularGraph_Graph-6", 1, 0, [0, 3, 5, 6, 7, 8, 9]),
    ("RegularGraph_Graph-8", 1, 0, [13, 10, 8, 6, 5, 4, 3, 0, 1, 2]),
])
def test_source_is_target(graph_key, budget, source, targets):
    with pytest.raises(ValueError):
        spreading_maxsave(graphs[graph_key], budget, source, targets)

@pytest.mark.parametrize("graph_key, source, targets, expected_gamma, expected_direct_vaccination", [
    ("Dirlay_Graph-5", 0, [1, 2, 3, 4, 5 ,6 ,7 ,8], {
        1: [(2, 1), (4, 1), (1, 1), (1, 2)],
        2: [(2, 1)],
        3: [(2, 1), (5, 1), (3, 1), (3, 2)],
        4: [(4, 1)],
        5: [(5, 1)],
        6: [(4, 1), (5, 1), (6, 1), (6, 2)],
        7: [(5, 1), (7, 1), (7, 2)],
        8: [(4, 1), (5, 1), (6, 1), (6, 2), (7, 1), (7, 2), (8, 1), (8, 2), (8, 3)],
    }, {
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
        (8, 3): [8]
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
    }, [
        {(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)},
        {(3, 2), (4, 2), (5, 2), (6, 2)},
        {(5, 3)}
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

@pytest.mark.parametrize("graph_key, budget, source, targets, expected_length", [
    ("RegularGraph_Graph-1", 1, 0, [1, 2, 3, 4, 5, 6], 2),
    ("Dirlay_Graph-5", 2, 0, [1, 2, 3, 4, 5, 6, 7, 8], 3),
])
def test_strategy_length(graph_key, budget, source, targets, expected_length):
    graph = graphs[graph_key]
    calculated_strategy = spreading_maxsave(graph, budget, source, targets)
    
    assert len(calculated_strategy) == expected_length


@pytest.mark.parametrize("graph_key, budget, source, targets, expected_strategy", [
    ("RegularGraph_Graph-1", 1, 0, [1, 2, 3, 4, 5, 6], {(1, 1), (6, 2)}),
    ("Dirlay_Graph-5", 2, 0, [1, 2, 3, 4, 5, 6, 7, 8], {(5, 1), (2, 1), (8, 2)}),
])
def test_save_all_vertices(graph_key, budget, source, targets, expected_strategy):
    graph = graphs[graph_key]
    calculated_strategy = spreading_maxsave(graph, budget, source, targets)
    
    assert calculated_strategy == expected_strategy

@pytest.mark.parametrize("graph_key, budget, source, targets, expected_strategy", [
    ("RegularGraph_Graph-6", 2, 1, [3, 9, 0, 5, 6], {(2, 1), (0, 1)}),
    ("RegularGraph_Graph-4", 1, 0, [2, 6, 4], {(1, 1), (3, 2)}),
])
def test_save_subgroup_vertices(graph_key, budget, source, targets, expected_strategy):
    graph = graphs[graph_key]
    calculated_strategy = spreading_maxsave(graph, budget, source, targets)
    
    assert calculated_strategy == expected_strategy

    # TODO : add tests on big graphs (100 nodes) - sanity checks only.