import networkx as nx
import networkx.algorithms.connectivity as algo 
import matplotlib.pyplot as plt
import copy

node_colors = {
    'target': 'gray',
    'infected': 'red',
    'vaccinated': 'blue',
    'directly vaccinated': 'green',
    'default' : "#00FFD0"
}

def calculate_gamma(graph:nx.DiGraph, source:int, targets:list)-> dict:
    gamma = {}
    direct_vaccination = {}
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
        gamma[key] = vaccination_options

    return gamma, direct_vaccination

def calculate_epsilon(direct_vaccinations:dict)->list:
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

    return epsilon

def find_best_direct_vaccination(graph:nx.DiGraph, direct_vaccinations:dict, current_time_options:list, targets:list)->tuple:
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

    if common_elements is not None:
        targets[:] = [element for element in targets if element not in nodes_saved]
    return best_vaccination


def spread_virus(graph:nx.DiGraph, infected_nodes:list)->bool:
    new_infected_nodes = []
    for node in infected_nodes:
        for neighbor in graph.neighbors(node):
            if graph.nodes[neighbor]['status'] == 'target':
                graph.nodes[neighbor]['status'] = 'infected'
                new_infected_nodes.append(neighbor)
    infected_nodes.clear()
    for node in new_infected_nodes:
        infected_nodes.append(node)  

    return bool(infected_nodes)

def spread_vaccination(graph:nx.DiGraph, vaccinated_nodes:list)->None:
    new_vaccinated_nodes = []
    for node in vaccinated_nodes:
        for neighbor in graph.neighbors(node):
            if graph.nodes[neighbor]['status'] == 'target':
                graph.nodes[neighbor]['status'] = 'vaccinated'
                new_vaccinated_nodes.append(neighbor)
    vaccinated_nodes.clear()
    for node in new_vaccinated_nodes:
        vaccinated_nodes.append(node)            
    return

def vaccinate_node(graph:nx.DiGraph, node:int)->None:
    graph.nodes[node]['status'] = 'directly vaccinated'
    return

def clean_graph(graph:nx.DiGraph)->None:
    for node in graph.nodes:
        graph.nodes[node]['status'] = 'target'
    return


def display_graph(graph:nx.DiGraph)->None:
    pos = nx.shell_layout(graph)
    colors = [node_colors.get(data.get('status', 'default'), 'default') for node, data in graph.nodes(data=True)]
    nx.draw(graph, pos, node_color=colors, with_labels=True, font_weight='bold')
    
    if nx.get_edge_attributes(graph, 'weight'):
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()
    return

def create_st_graph(graph:nx.DiGraph, targets:list)->nx.DiGraph:
    G = copy.deepcopy(graph)
    G.add_node('t', status = 'target')
    for node in targets:
        G.add_edge(node,'t')
    return G

def graph_flow_reduction(graph:nx.DiGraph, source:int)->list:
    H = nx.DiGraph()
    for node in graph.nodes:
        in_node, out_node = f'{node}_in', f'{node}_out'
        H.add_nodes_from([in_node, out_node])
        if node == source or node == 't':
            H.add_edge(in_node, out_node, weight=float('inf'))
        else:
            H.add_edge(in_node, out_node, weight=graph.nodes[node]['weight'])
    for edge in graph.edges:
        H.add_edge(f'{edge[0]}_out', f'{edge[1]}_in', weight=float('inf'))
    display_graph(H)
    # the return is giving a different result then expected 
    return algo.minimum_st_edge_cut(H,f'{source}_in','t_out')
    


if __name__ == "__main__":
    G2 = nx.DiGraph()
    G2.add_node(0, status = 'target', weight = 1)
    G2.add_node(1, status = 'target', weight = 2)
    G2.add_node(2, status = 'target', weight = 2)
    G2.add_node(3, status = 'target', weight = 3)
    G2.add_node(4, status = 'target', weight = 3)
    G2.add_edges_from([(0,1),(0,2),(1,3),(1,4),(2,3),(2,4)])
    H = create_st_graph(G2, [1,2,3,4])
    print(graph_flow_reduction(H,0))
    #print(list(nx.bfs_layers(G2,0)))
    
        