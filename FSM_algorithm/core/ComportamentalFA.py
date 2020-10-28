from core.State import State


class ComportamentalFA():
    def __init__(self, name, states):
        self.name = name
        self.states = []
        for state in states:
            self.states.append(State(name=state["name"], isInit=state["init"],
                               outTransitions=state["outTransition"]))
