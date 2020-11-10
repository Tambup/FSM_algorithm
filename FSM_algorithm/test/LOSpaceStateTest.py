import unittest
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSObservation import ComportamentalFANSObservation
from core.OutTransition import OutTransition
from core.State import State


class TestStringMethods(unittest.TestCase):
    def test_next_transition_valid(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        test = ComportamentalFANSObservation(cfaNetwork)
        test.build(['o3', 'o2'])
        outTransition = {
            'name': 't3a',
            'destination': '31',
            'link': [{
                'type': 'out',
                'link': 'L2',
                'event': 'e2'}],
            'observable': 'o3',
            'relevant': None}
        s1 = State('30', True, [outTransition])
        i, next = test._space_states[0].next_transition_state('o3')[s1]
        self.assertTrue(next[0] == s1._out_transitions[0])

    def test_next_transition_none(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        test = ComportamentalFANSObservation(cfaNetwork)
        test.build(['o3', 'o2'])
        next = test._space_states[6].next_transition_state('o3')
        self.assertFalse(len(next) > 0)

    def test_must_add_valid(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        test = ComportamentalFANSObservation(cfaNetwork)
        test.build(['o3', 'o2'])
        link = {
                'type': 'out',
                'link': 'L2',
                'event': 'e2'}
        outTr = OutTransition('t3a', '31', [link], ['o3'], [])
        space_state = test._space_states[0]
        self.assertTrue(space_state._must_add(outTr, ['o3']))

    def test_must_add_in_false(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        test = ComportamentalFANSObservation(cfaNetwork)
        test.build(['o3', 'o2'])
        link = {
                'type': 'in',
                'link': 'L2',
                'event': None}
        outTr = OutTransition('t3a', '31', [link], ['o3'], [])
        space_state = test._space_states[0]
        self.assertFalse(space_state._must_add(outTr, ['o3']))


if __name__ == '__main__':
    unittest.main()
