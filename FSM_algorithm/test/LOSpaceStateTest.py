import unittest
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSObservation import ComportamentalFANSObservation
from core.OutTransition import OutTransition
from core.State import State


class TestStringMethods(unittest.TestCase):
    def test_next_transition_valid(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.read_json(''.join(line for line in lines))
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
        successors = test._space_states[0].next_transition_state('o3')
        nonces = [tr[0]._nonce for _, tr in successors.values()]
        for nonce in nonces:
            s1.out_transitions[0]._nonce = nonce
            try:
                i, next = successors[s1]
                break
            except KeyError:
                pass
        self.assertTrue(next[0] == s1._out_transitions[0])

    def test_next_transition_none(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.read_json(''.join(line for line in lines))
        test = ComportamentalFANSObservation(cfaNetwork)
        test.build(['o3', 'o2'])
        next = test._space_states[6].next_transition_state('o3')
        self.assertFalse(len(next) > 0)

    def test_must_add_valid(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.read_json(''.join(line for line in lines))
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
        cfaNetwork = UserIO.read_json(''.join(line for line in lines))
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
