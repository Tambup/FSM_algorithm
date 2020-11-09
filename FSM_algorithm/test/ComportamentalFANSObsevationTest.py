import unittest
from ComportamentalFANSObservation import ComportamentalFANSObservation
from userInputOutput import UserInputOutput as UserIO
from core.State import State
from SpaceState import SpaceState
from LOSpaceState import LOSpaceState


class TestStringMethods(unittest.TestCase):
    def test_dfs_visit_corresct_observation(self):
        out_exp_1 = {
            'name': 't2a',
            'destination': '21',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e2'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': 'o2',
            'relevant': None}
        out_exp_2 = {
            'name': 't3b',
            'destination': '30',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': None}
        out_exp_3 = {
            'name': 't3c',
            'destination': '31',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': 'f'}
        ss_exp = LOSpaceState([State('20', True, [out_exp_1]),
                               State('31', False, [out_exp_2, out_exp_3])],
                              {'L2': SpaceState.NULL_EVT,
                               'L3': SpaceState.NULL_EVT})
        ss_exp.obs_index = 2
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSObservation(cfaNetwork)
        fanSpace._initialize()
        fanSpace._dfs_visit(fanSpace._space_states[0], ['o3', 'o2'], 0)
        self.assertTrue(ss_exp == fanSpace._space_states[8])

    def test_dfs_visit_not_correct_observation(self):
        out_exp_1 = {
            'name': 't2a',
            'destination': '21',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e2'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': 'o2',
            'relevant': None}
        out_exp_2 = {
            'name': 't3a',
            'destination': '31',
            'link': [{
                'type': 'out',
                'link': 'L2',
                'event': 'e2'}],
            'observable': 'o3',
            'relevant': None}
        ss_exp = LOSpaceState([State('20', True, [out_exp_1]),
                               State('30', True, [out_exp_2])],
                              {'L2': SpaceState.NULL_EVT,
                               'L3': SpaceState.NULL_EVT})
        ss_exp.obs_index = 0
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSObservation(cfaNetwork)
        fanSpace._initialize()
        fanSpace._dfs_visit(fanSpace._space_states[0], ['o2'], 0)
        dim = len(fanSpace._space_states)
        self.assertFalse(ss_exp != fanSpace._space_states[dim-1])

    def test_dfs_visit_not_correct_state(self):
        out_exp_1 = {
            'name': 't2a',
            'destination': '21',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e2'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': 'o2',
            'relevant': None}
        out_exp_2 = {
            'name': 't3b',
            'destination': '30',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': None}
        out_exp_3 = {
            'name': 't3c',
            'destination': '31',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': 'f'}
        ss_exp = LOSpaceState([State('20', True, [out_exp_1]),
                               State('31', False, [out_exp_2, out_exp_3])],
                              {'L2': 'e2',
                               'L3': 'e3'})
        ss_exp.set_link('L2', 'e2')
        ss_exp.set_link('L3', 'e3')
        ss_exp.obs_index = 3  # with ['o3', 'o2', 'o3'] is contained
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSObservation(cfaNetwork)
        fanSpace._initialize()
        fanSpace._dfs_visit(fanSpace._space_states[0], ['o3', 'o2'], 0)
        self.assertFalse(ss_exp in fanSpace.space_states)

    def test_dfs_visit_index_counting(self):
        out_exp_1 = {
            'name': 't2a',
            'destination': '21',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e2'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': 'o2',
            'relevant': None}
        out_exp_2 = {
            'name': 't3b',
            'destination': '30',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': None}
        out_exp_3 = {
            'name': 't3c',
            'destination': '31',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': 'f'}
        ss_exp = LOSpaceState([State('20', True, [out_exp_1]),
                               State('31', False, [out_exp_2, out_exp_3])],
                              {'L2': 'e2',
                               'L3': 'e3'})
        ss_exp.set_link('L2', 'e2')
        ss_exp.set_link('L3', 'e3')
        ss_exp.obs_index = 3  # with ['o3', 'o2', 'o3'] is contained
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSObservation(cfaNetwork)
        fanSpace._initialize()
        fanSpace._dfs_visit(fanSpace._space_states[0], ['o3', 'o2', 'o3'], 0)
        self.assertTrue(ss_exp in fanSpace.space_states)

    def test_get_nexts_correct(self):
        out_exp_1 = {
            'name': 't2a',
            'destination': '21',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e2'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': 'o2',
            'relevant': None}
        out_exp_2 = {
            'name': 't3b',
            'destination': '30',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': None}
        out_exp_3 = {
            'name': 't3c',
            'destination': '31',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': 'f'}
        state_exp_1 = State('20', True, [out_exp_1])
        state_exp_2 = State('31', False, [out_exp_2, out_exp_3])
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace_check = ComportamentalFANSObservation(cfaNetwork)
        fanSpace_check._initialize()
        next = fanSpace_check._get_nexts(fanSpace_check._space_states[0],
                                         fanSpace_check._space_states[0].
                                         next_transition_state('o3'),
                                         ['o3', 'o2'])
        self.assertTrue(state_exp_1, state_exp_2 in next[0][0].states)

    def test_get_nexts_no_correct_state(self):
        out_exp_1 = {
            'name': 't2a',
            'destination': '25',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e2'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': 'o2',
            'relevant': None}
        state_exp_1 = State('20', True, [out_exp_1])
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace_check = ComportamentalFANSObservation(cfaNetwork)
        fanSpace_check._initialize()
        next = fanSpace_check._get_nexts(fanSpace_check._space_states[0],
                                         fanSpace_check._space_states[0].
                                         next_transition_state('o3'),
                                         ['o3', 'o2'])
        self.assertFalse(state_exp_1 in next[0][0].states)

    def test_get_nexts_no_correct_osservation(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace_check = ComportamentalFANSObservation(cfaNetwork)
        fanSpace_check._initialize()
        next = fanSpace_check._get_nexts(fanSpace_check._space_states[0],
                                         fanSpace_check._space_states[0].
                                         next_transition_state('o2'),
                                         ['o3', 'o2'])
        self.assertFalse(len(next) > 0)

    def test_prune_correct(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSObservation(cfaNetwork)
        fanSpace._initialize()
        fanSpace._dfs_visit(fanSpace._space_states[0], ['o3', 'o2'], 0)
        mantain_dict = {}
        fanSpace._prune(fanSpace._space_states[0], mantain_dict)
        not_in = fanSpace.space_states[4]
        self.assertTrue(not_in not in mantain_dict.keys() and
                        len(mantain_dict) + 1 == len(fanSpace._space_states))


if __name__ == '__main__':
    unittest.main()
