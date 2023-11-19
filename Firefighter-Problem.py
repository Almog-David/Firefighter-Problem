import networkx as nx
from Utils import *

"""
Examples of graphs that we will use in the following runing examples:
G1 = nx.Digraph  G1.add_nodes_from([0,1,2,3,4,5,6])
G1.add_edges_from([(0,1),(0,2),(1,2),(1,4),(2,3),(2,6),(3,5)])

G2 = nx.Digraph  G2.add_nodes_from([0,1,2,3,4,5,6,7,8])
G2.add_edges_from([(0,2),(0,4),(0,5),(2,1),(2,3),(4,1),(4,6),(5,3),(5,6),(5,7),(6,7),(6,8),(7,8)])

G3 = nx.Digraph  G3.add_nodes_from([0,1,2,3,4,5])
G3.add_edges_from([(0,1),(0,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,5),(4,5)])
"""


def spreading_maxsave(Graph:nx.DiGraph, budget:int, source:int, targets:list) -> list:
    """
    "Approximability of the Firefighter Problem - Computing Cuts over Time",
    by Elliot Anshelevich, Deeparnab Chakrabarty, Ameya Hate, Chaitanya Swamy (2010)
    https://link.springer.com/article/10.1007/s00453-010-9469-y
    
    Programmers: Shaked Levi, Almog David, Yuval Bobnovsky

    spreading_maxsave: Gets a directed graph, budget, source node, and list of targeted nodes that we need to save
    and return the best vaccination strategy that saves the most nodes from the targeted nodes list.
    
    Example1:
    >>> spreading_maxsave(G1,1,0,G1.nodes())
    [(1,1),(6,2)]

    Example2:
    >>> spreading_maxsave(G2,2,0,G2.nodes())
    [(5,1),(2,1),(8,2)]
    """
    infected_nodes = []
    vaccinated_nodes = []
    vaccination_strategy = []
    can_spread = True
    Graph.nodes[source]['status'] = 'infected'
    infected_nodes.append(source)
    display_graph(Graph)
    gamma, direct_vaccinations = calculate_gamma(Graph, source, targets)
    epsilon = calculate_epsilon(direct_vaccinations)
    while(can_spread):
        time_step = 0
        spread_vaccination(Graph, vaccinated_nodes)
        display_graph(Graph)
        for i in range(budget):
            vaccination = find_best_direct_vaccination(Graph,direct_vaccinations,epsilon[time_step],targets)
            if vaccination != ():
                vaccination_strategy.append(vaccination)
                chosen_node = vaccination[0]
                vaccinate_node(Graph, chosen_node)
                display_graph(Graph)
                vaccinated_nodes.append(chosen_node)
        can_spread = spread_virus(Graph,infected_nodes)
        display_graph(Graph)
        time_step = time_step + 1
    
    return vaccination_strategy

def spreading_minbudget(Graph:nx.DiGraph, source:int, targets:list)-> int:
    """
    "Approximability of the Firefighter Problem - Computing Cuts over Time",
    by Elliot Anshelevich, Deeparnab Chakrabarty, Ameya Hate, Chaitanya Swamy (2010)
    https://link.springer.com/article/10.1007/s00453-010-9469-y
    
    Programmers: Shaked Levi, Almog David, Yuval Bobnovsky

    spreading_minbudget: Gets a directed graph, source node, and list of targeted nodes that we need to save
    and returns the minimum budget that saves all the nodes from the targeted nodes list.

    Example1:
    >>> spreading_minbudget(G2,0,[2,6,1,8])
    2

    Example2:
    >>> spreading_minbudget(G2,0,G2.nodes())
    3
    """
    return 0
    
def non_spreading_minbudget(Graph:nx.DiGraph, source:int, targets:list)->int:
    """
    "Approximability of the Firefighter Problem - Computing Cuts over Time",
    by Elliot Anshelevich, Deeparnab Chakrabarty, Ameya Hate, Chaitanya Swamy (2010)
    https://link.springer.com/article/10.1007/s00453-010-9469-y
    
    Programmers: Shaked Levi, Almog David, Yuval Bobnovsky

    non_spreading_minbudget: Gets a directed graph, source node, and list of targeted nodes that we need to save
    and returns the minimum budget that saves all the nodes from the targeted nodes list.
    """
    return 0

def non_spreading_dirlaynet_minbudget(Graph:nx.DiGraph, source:int, targets:list)->int:
    """
    "Approximability of the Firefighter Problem - Computing Cuts over Time",
    by Elliot Anshelevich, Deeparnab Chakrabarty, Ameya Hate, Chaitanya Swamy (2010)
    https://link.springer.com/article/10.1007/s00453-010-9469-y
    
    Programmers: Shaked Levi, Almog David, Yuval Bobnovsky

    non_spreading_dirlaynet_minbudget: Gets a directed graph, source node, and list of targeted nodes that we need to save
    and returns the minimum budget that saves all the nodes from the targeted nodes list.
    """
    return 0


if __name__ == "__main__":
    G2 = nx.DiGraph()
    G2.add_node(0, status = 'target')
    G2.add_node(1, status = 'target')
    G2.add_node(2, status = 'target')
    G2.add_node(3, status = 'target')
    G2.add_node(4, status = 'target')
    G2.add_node(5, status = 'target')
    G2.add_node(6, status = 'target')
    G2.add_edges_from([(0,1),(0,2),(1,3),(2,3),(1,4),(2,6),(3,5)])
    strategy = spreading_maxsave(G2,1, 0, [1,2,3,4,5,6])
    print(strategy)
   