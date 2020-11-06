import unittest
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSpace import ComportamentalFANSpace
from core.OutTransition import OutTransition
from SpaceState import SpaceState
from core.State import State


class TestStringMethods(unittest.TestCase):
    def test_maintain(self):
        f = open("sample/FSCNetwork.sample.json", "r")
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        a = cfaNetwork._comportamentalFAs[0]._states[0]
        b = cfaNetwork._comportamentalFAs[1]._states[0]
        check = SpaceState([a, b], {'L2', 'L3'})
        test = ComportamentalFANSpace(cfaNetwork)
        test.build()
        self.assertTrue(test._space_states.__contains__(check))

    def test_next_transition_valid(self):
        f = open("sample/FSCNetwork.sample.json", "r")
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        test = ComportamentalFANSpace(cfaNetwork)
        test.build()
        outTransition = {
            "name": "t3a",
            "destination": "31",
            "link": [{
                "type": "out",
                "link": "L2",
                "event": "e2"}],
            "observable": ["o3"],
            "relevant": []}
        s1 = State('30', True, [outTransition])
        next = test._space_states[0].next_transition_state()[s1]
        self.assertTrue(next[0] == s1._out_transitions[0])

    def test_next_transition_none(self):
        f = open("sample/FSCNetwork.sample.json", "r")
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        test = ComportamentalFANSpace(cfaNetwork)
        test.build()
        next = test._space_states[12].next_transition_state()
        self.assertFalse(len(next) > 0)

    def test_must_add_valid(self):
        f = open("sample/FSCNetwork.sample.json", "r")
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        test = ComportamentalFANSpace(cfaNetwork)
        test.build()
        link = {
                "type": "out",
                "link": "L2",
                "event": "e2"}
        outTr = OutTransition('t3a', '31', [link], ['o3'], [])
        space_state = test._space_states[0]
        self.assertTrue(space_state._must_add(outTr))

    def test_must_add_in_false(self):
        f = open("sample/FSCNetwork.sample.json", "r")
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        test = ComportamentalFANSpace(cfaNetwork)
        test.build()
        link = {
                "type": "in",
                "link": "L2",
                "event": None}
        outTr = OutTransition('t3a', '31', [link], ['o3'], [])
        space_state = test._space_states[0]
        self.assertFalse(space_state._must_add(outTr))


if __name__ == '__main__':
    unittest.main()
