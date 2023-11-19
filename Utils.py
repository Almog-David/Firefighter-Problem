import networkx as nx
import matplotlib.pyplot as plt

node_colors = {
    'target': 'gray',
    'infected': 'red',
    'vaccinated': 'blue',
    'directly_vaccinated': 'green',
}

def calculate_gamma(graph:nx.DiGraph, source:int, targets:list)-> dict:
    return 0

def calculate_epsilon(direct_vaccinations:dict)->list:
    return 0

def find_best_direct_vaccination(direct_vaccinations:dict, current_time_options:list, targets:list)->tuple:
    return 0

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

def display_graph(graph:nx.DiGraph)->None:
    colors = [node_colors[data['status']] for node, data in graph.nodes(data=True)]
    pos = nx.shell_layout(graph)
    nx.draw(graph, pos, node_color=colors, with_labels=True, font_weight='bold')
    plt.show()
    return


if __name__ == "__main__":