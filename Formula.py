from dataclasses import dataclass
from abc import abstractmethod
import pydot
from TransitionSystem import TransitionSystem, transition_system, graph, labels


@dataclass
class Formula:
    @abstractmethod
    def label(self, t: TransitionSystem) -> set:
        pass


@dataclass
class TrueFormula(Formula):
    def label(self, t: TransitionSystem):
        return t.states


@dataclass
class AtomicFormula(Formula):
    a: str

    def label(self, t: TransitionSystem):
        return {state for state in t.labels if self.a in t.labels[state]}


@dataclass
class ConjFormula(Formula):
    def label(self, t: TransitionSystem):
        return self.f1.label(t).intersection(self.f2.label(t))

    f1: Formula
    f2: Formula


@dataclass
class NegFormula(Formula):
    def label(self, t: TransitionSystem):
        return TrueFormula().label(t).difference(self.f1.label(t))

    f1: Formula


@dataclass
class EFFormula(Formula):
    f1: Formula

    def label(self, t: TransitionSystem) -> set:
        return EUFormula(TrueFormula(), self.f1).label(t)


@dataclass
class AFFormula(Formula):
    def label(self, t: TransitionSystem):
        return AUFormula(TrueFormula(), self.f1).label(t)

    f1: Formula


@dataclass
class AUFormula(Formula):
    f1: Formula
    f2: Formula

    def label(self, t: TransitionSystem):
        satisfy_until = self.f2.label(t)
        for state in satisfy_until:
            satisfy_f1 = self.f1.label(t).intersection(t.predecessors[state])
            if len(satisfy_f1) > 0:
                satisfy_until = satisfy_until.union(satisfy_f1)
            else:
                break
        return satisfy_until


@dataclass
class EUFormula(Formula):
    f1: Formula
    f2: Formula

    def label(self, t: TransitionSystem):
        satisfy_until = self.f2.label(t)
        while True:
            satisfy_f1 = {state for state in self.f1.label(t) if
                          t.successors[state].intersection(satisfy_until) != set()}
            if satisfy_until == satisfy_until | satisfy_f1:
                break
            else:
                satisfy_until |= satisfy_f1
        return satisfy_until


@dataclass
class EXFormula(Formula):
    f1: Formula

    def label(self, t: TransitionSystem):
        return {state for state in t.states if len(t.successors[state].intersection(self.f1.label(t))) > 0}


@dataclass
class EGFormula(Formula):
    f1: Formula

    def label(self, t: TransitionSystem) -> set:
        satisfy_global = self.f1.label(t)
        while True:
            satisfy_global_diff = {state for state in satisfy_global if
                                   t.successors[state].intersection(satisfy_global) != set()}
            # satisfy_global_diff = {state for state in satisfy_global if
            #                        len(t.successors[state].intersection(satisfy_global)) > 0}
            if satisfy_global_diff == satisfy_global:
                return satisfy_global_diff
            else:
                satisfy_global = satisfy_global_diff


if __name__ == '__main__':
    # result_states = EGFormula(AtomicFormula('n2')).label(transition_system)
    result_states = NegFormula(ConjFormula(AtomicFormula('t1'), AtomicFormula('t2'))).label(transition_system)
    # result_states = TrueFormula().label(transition_system)
    # print(labels)
    print(result_states)
    for node in graph.get_nodes():
        node.set("label", node.get('label') + f" ({int(node.get_name())})")
        if int(node.get_name()) in result_states:
            node.set("style", "filled")
            node.set("fillcolor", "blue")
            node.set("fontcolor", "red")
    graph.write_svg('result.svg')



