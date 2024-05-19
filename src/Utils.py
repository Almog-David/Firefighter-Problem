import networkx as nx
import networkx.algorithms.connectivity as algo 
import matplotlib.pyplot as plt
import numpy as np
import math
import copy

node_colors = {
    'target': 'gray',
    'infected': 'red',
    'vaccinated': 'blue',
    'directly vaccinated': 'green',
    'default' : "#00FFD0"
}

def validate_parameters(graph:nx.DiGraph, source:int, targets:list)->None:
    """
    Validate the source and target nodes in the graph.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    - source (int): Source node.
    - targets (list): List of target nodes to save.

    Raises:
    - ValueError: If the source node is not in the graph.
    - ValueError: If the source node is in the targets list.
    - ValueError: If any target node is not in the graph.
    """
    graph_nodes = list(graph.nodes())
    if source not in graph_nodes:
        raise ValueError("Error: The source node isn't on the graph")
        exit()
    if source in targets:
        raise ValueError("Error: The source node can't be a part of the targets list, since the virus is spreading from the source")
        exit()
    if not all(node in graph_nodes for node in targets):
        raise ValueError("Error: Not all nodes in the targets list are on the graph.")
        exit()

"Spreading:"
def calculate_gamma(graph:nx.DiGraph, source:int, targets:list)-> dict:
    """
    Calculate Gamma and S(u,t)  based on the calculation in the article.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    - source (int): Source node.
    - targets (list): List of target nodes to save.

    Returns:
    - gamma (dict): Dictionary of vaccination options.
    - direct_vaccination (dict): Dictionary of direct vaccination strategies - S(u,t).
    """
    gamma = {}
    direct_vaccination = {}
    unreachable_nodes = []
    path_length = dict(nx.all_pairs_shortest_path_length(graph))
    for key in graph.nodes:
        vaccination_options = []
        for node in graph.nodes:
                if path_length[source].get(key) is not None and path_length[node].get(key) is not None:
                    s_to_v = path_length[source].get(key)
                    u_to_v = path_length[node].get(key)
                    max_time = s_to_v - u_to_v
                    if max_time > 0:
                        for i in range(1,max_time+1):
                            option = (node,i)
                            vaccination_options.append(option)
                            if option not in direct_vaccination:
                                direct_vaccination[option] = []
                            if key in targets:
                                direct_vaccination[option].append(key)

        # if the virus can't reach to the node - it's automatically saved 
        if not vaccination_options:
            unreachable_nodes.append(key)
        if key != source:                       
            gamma[key] = vaccination_options

    # add all the unreachable nodes to the vaccination strategy - every strategy can save them 
    for strategy in direct_vaccination:
        for node in unreachable_nodes:
            if node in targets:
                direct_vaccination[strategy].append(node)
    
    #print("Gamma is: " + str(gamma))
    #print("S(u,t) is: " + str(direct_vaccination))
    return gamma, direct_vaccination

def calculate_epsilon(direct_vaccinations:dict)->list:
    """
    Calculate Epsilon based on the calculation in the article.

    Parameters:
    - direct_vaccinations (dict): Dictionary of direct vaccination strategies.

    Returns:
    - epsilon (list): List of direct vaccination groups by time step.
    """
    epsilon = []
    sorted_dict = dict(sorted(direct_vaccinations.items(), key=lambda item: item[0][1]))

    # Iterate over the sorted dictionary and populate the result list
    current_time_step = None
    current_group = []
    for key, value in sorted_dict.items():
        if current_time_step is None or key[1] == current_time_step:
            current_group.append(key)
        else:
            epsilon.append(current_group)
            current_group = [key]
        current_time_step = key[1]

    # Append the last group
    if current_group:
        epsilon.append(current_group)
    
    #print("Epsilon is: " + str(epsilon))
    return epsilon

def find_best_direct_vaccination(graph:nx.DiGraph, direct_vaccinations:dict, current_time_options:list, targets:list)->tuple:
    """
    Find the best direct vaccination strategy for the current time step that saves more new node in targets.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    - direct_vaccinations (dict): Dictionary of direct vaccination strategies.
    - current_time_options (list): List of current time step vaccination options.
    - targets (list): List of target nodes.

    Returns:
    - best_vaccination (tuple): Best direct vaccination option.
    """
    best_vaccination = () 
    nodes_saved = {}
    common_elements = None
    max_number = -1
    for option in current_time_options:
        if(graph.nodes[option[0]]['status'] == 'target'):
            nodes_list = direct_vaccinations.get(option)
            common_elements = set(nodes_list) & set(targets)
            if len(common_elements) > max_number:
                best_vaccination = option
                nodes_saved = common_elements
                max_number = len(common_elements)

    if nodes_saved is not None:
        targets[:] = [element for element in targets if element not in nodes_saved]
    
    #if best_vaccination != ():
       # print("The best direct vaccination is: " + str(best_vaccination) + " and it's saves nodes: " + str(nodes_saved))
    return best_vaccination

def spread_virus(graph:nx.DiGraph, infected_nodes:list)->bool:
    """
    Spread the virus from infected nodes to their neighbors.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    - infected_nodes (list): List of currently infected nodes.

    Returns:
    - bool: True if there are new infections, False otherwise.
    """
    new_infected_nodes = []
    for node in infected_nodes:
        for neighbor in graph.neighbors(node):
            if graph.nodes[neighbor]['status'] == 'target':
                graph.nodes[neighbor]['status'] = 'infected'
                new_infected_nodes.append(neighbor)
    infected_nodes.clear()
    for node in new_infected_nodes:
        infected_nodes.append(node)  
    #display_graph(graph)
    return bool(infected_nodes)

def spread_vaccination(graph:nx.DiGraph, vaccinated_nodes:list)->None:
    """
    Spread the vaccination from vaccinated nodes to their neighbors.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    - vaccinated_nodes (list): List of currently vaccinated nodes.
    """
    new_vaccinated_nodes = []
    for node in vaccinated_nodes:
        for neighbor in graph.neighbors(node):
            if graph.nodes[neighbor]['status'] == 'target':
                graph.nodes[neighbor]['status'] = 'vaccinated'
                new_vaccinated_nodes.append(neighbor)
    vaccinated_nodes.clear()
    for node in new_vaccinated_nodes:
        vaccinated_nodes.append(node) 
    #display_graph(graph)              
    return

def vaccinate_node(graph:nx.DiGraph, node:int)->None:
    """
    Directly vaccinate a specific node in the graph.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    - node (int): Node to be vaccinated.
    """
    graph.nodes[node]['status'] = 'directly vaccinated'
    #display_graph(graph)
    return

def clean_graph(graph:nx.DiGraph)->None:
    """
    Reset the graph to its base state where all nodes are targets.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    """
    for node in graph.nodes:
        graph.nodes[node]['status'] = 'target'
    return

"Non-Spreading:"

def adjust_nodes_capacity(graph:nx.DiGraph, source:int)->list:
    """
    Adjust the capacity of nodes based on the layer they belong to.
    The capacity is based on the formula in the article at the DirLayNet algorithm section.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    - source (int): Source node.

    Returns:
    - layers (list): List of nodes grouped by layers.
    """
    layers = (list(nx.bfs_layers(graph,source)))
    harmonic_sum = 0.0
    for i in range(1,len(layers)):
        harmonic_sum = harmonic_sum + 1/i
    for index in range(1,len(layers)):
        for node in layers[index]:
            graph.nodes[node]['capacity'] = 1/(index*harmonic_sum)
    print("Layers: ", layers)       
    return layers

def create_st_graph(graph:nx.DiGraph, targets:list)->nx.DiGraph:
    """
    Create an s-t graph from the original graph for use in connectivity algorithms.

    Parameters:
    - graph (nx.DiGraph): Original directed graph.
    - targets (list): List of target nodes.

    Returns:
    - G (nx.DiGraph): s-t graph.
    """
    G = copy.deepcopy(graph)
    G.add_node('t', status = 'target')
    for node in targets:
        G.add_edge(node,'t')
    #display_graph(G)
    return G

def graph_flow_reduction(graph:nx.DiGraph, source:int)->nx.DiGraph:
    """
    Perform flow reduction on the graph to find the minimum s-t cut.

    Parameters:
    - graph (nx.DiGraph): Original directed graph.
    - source (int): Source node.

    Returns:
    - H (nx.DiGraph): Graph after flow reduction.
    """
    H = nx.DiGraph()
    for node in graph.nodes:
        in_node, out_node = f'{node}_in', f'{node}_out'
        H.add_nodes_from([in_node, out_node])
        if node == source or node == 't':
            H.add_edge(in_node, out_node, weight=float('inf'))
        else:
            H.add_edge(in_node, out_node, weight=graph.nodes[node]['capacity'])
    for edge in graph.edges:
        H.add_edge(f'{edge[0]}_out', f'{edge[1]}_in', weight=float('inf'))
    display_graph(H)
    return H

def min_cut_N_groups(graph:nx.DiGraph, source:int) -> list: 
    """
    Find the minimum cut and group nodes accordingly.

    Parameters:
    - graph (nx.DiGraph): Graph after flow reduction.
    - source (int): Source node.

    Returns:
    - n_groups (list): List of nodes in the minimum cut.
    """
    flow_graph = algo.minimum_st_node_cut(graph,f'{source}_out','t_in') #run algo on the graph after reduction and get the min-cut
    n_groups = {int(item.split('_')[0]) for item in flow_graph} # split it to the groups accordingly.
    return n_groups

def calculate_vaccine_matrix(layers:list, min_cut_nodes:list)->np.matrix: 
    """
    Calculate the vaccine matrix based on the calculation in the article at the DirLayNet algorithm section.

    Parameters:
    - layers (list): List of nodes grouped by layers.
    - min_cut_nodes (list): List of nodes in the minimum cut.

    Returns:
    - matrix (np.matrix): Vaccine matrix.
    """
    nodes_list = [] # = N_i 
    print(layers, min_cut_nodes)
    for i in range(1,len(layers)):
        common_elements = set(min_cut_nodes) & set(layers[i])
        nodes_list.append(common_elements)
    print(nodes_list)
    matrix = np.zeros((len(layers)-1, len(layers)-1))
    for i in range (len(layers)-1):
        for j in range(i, len(layers)-1):
            matrix[i][j] = ((len(nodes_list[j])/(j+1))) # here we can chose ceil or floor.
    print(matrix)
    return matrix
    

def matrix_to_integers_values(matrix:np.matrix) -> np.matrix: #TODO: THIS 
    """
    Convert matrix values to integers.

    Parameters:
    - matrix (np.matrix): Input matrix.

    Returns:
    - np.matrix: Matrix with integer values.
    """
    return

def min_budget_calculation(matrix:np.matrix) -> int :
    """
    Calculate the minimum budget from the matrix.

    Parameters:
    - matrix (np.matrix): Input matrix.

    Returns:
    - int: Minimum budget.
    """
    # integral_matrix = matrix_to_integers_values(matrix) TODO : make this work.
    i = j = 0
    matrix_size = len(matrix[i])
    row_sum = [0]*matrix_size
    for i in range(matrix_size):
        for j in range(matrix_size):
            print(matrix[i][j])
            row_sum[i] += matrix[i][j]
    print(row_sum)
    return int(max(row_sum))

def display_graph(graph:nx.DiGraph)->None:
    """
    Display the graph using Matplotlib.

    Parameters:
    - graph (nx.DiGraph): Directed graph.
    """
    pos = nx.shell_layout(graph)
    colors = [node_colors.get(data.get('status', 'default'), 'default') for node, data in graph.nodes(data=True)]
    nx.draw(graph, pos, node_color=colors, with_labels=True, font_weight='bold')
    
    if nx.get_edge_attributes(graph, 'weight'):
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()
    return

def parse_json_to_networkx(json_data):
    """
    Parse JSON data to create Networkx graphs.

    Parameters:
    - json_data (dict): JSON data containing graph information.

    Returns:
    - graphs (dict): Dictionary of Networkx graphs.
    """
    graphs = {}
    
    for graph_type, graph_data in json_data.items():
        for graph_name, graph_info in graph_data.items():
            
            graph_key = f"{graph_type}_{graph_name}"
            if "vertices" not in graph_info or not isinstance(graph_info["vertices"], list) or not graph_info["vertices"]:
                raise KeyError(f"Error parsing {graph_type}_{graph_name}: 'vertices' must be a non-empty list.")

            if "edges" not in graph_info or not isinstance(graph_info["edges"], list) or not graph_info["edges"]:
                raise KeyError(f"Error parsing {graph_type}_{graph_name}: 'edges' must be a non-empty list.")

            vertices = graph_info["vertices"]
            edges = [(edge["source"], edge["target"]) for edge in graph_info["edges"]]
            
            G = nx.DiGraph()
            G.add_nodes_from(vertices, status="target")
            G.add_edges_from(edges)
                
            graphs[graph_key] = G

    return graphs