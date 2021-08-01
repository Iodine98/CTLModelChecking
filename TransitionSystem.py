from dataclasses import dataclass, field
import pydot


@dataclass
class TransitionSystem:
    states: set[int]
    transitions: set[tuple[int, int]]
    labels: dict[int, set[str]]

    def __post_init__(self):
        self.successors: dict[int, set[int]] = self.create_successors()
        self.predecessors: dict[int, set[int]] = self.create_predecessors()

    def create_successors(self):
        successors: dict[int, set[int]] = {state: set() for state in self.states}
        for (source, sink) in self.transitions:
            successors[source].add(sink)
        return successors

    def create_predecessors(self):
        predecessors: dict[int, set[int]] = {state: set() for state in self.states}
        for (source, sink) in self.transitions:
            predecessors[sink].add(source)
        return predecessors

    # states = set(range(9))
    # transitions = {(0, 1), (1, 2), (2, 3), (1, 4), (4, 3), (4, 0), (3, 5),
    #                (0, 5), (5, 6), (6, 7), (5, 8), (8, 7), (8, 0), (7, 1)}
    # labels = {0: {"n1", "n2"}, 1: {"t1", "n2"}, 2: {"t1", "t2"}, 3: {"c1", "t2"},
    #           4: {"c1", "n2"}, 5: {"n1", "t2"},
    #           6: {"t1", "t2"}, 7: {"t1", "c2"}, 8: {"n1", "c2"}}
    # transition_system = TransitionSystem(states, transitions, labels)


graph = pydot.graph_from_dot_file('example.dot')[0]


def init_transitions(transit):
    for edge in graph.get_edges():
        if 'nodes' in edge.get_destination():
            for sink in edge.get_destination()['nodes'].keys():
                transit.add((int(edge.get_source()), int(sink)))
        else:
            transit.add((int(edge.get_source()), int(edge.get_destination())))
    return transit


def init_labels(nodes):
    for node in graph.get_nodes():
        nodes[int(node.get_name())] = node.get('label').strip('"')
    return nodes


transitions: set[tuple[int, int]] = init_transitions(set())
states = {int(state.get_name()) for state in graph.get_nodes()}
labels = init_labels({})
transition_system = TransitionSystem(states, transitions, labels)


