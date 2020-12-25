import unittest
from FSM_algorithm.core import State


class TestStringMethods(unittest.TestCase):

    def test_has_no_exit(self):
        out_transition = {
            'name': 't2a',
            'destination': '21',
            'link': [],
            'observable': None,
            'relevant': None}
        s1 = State('20', True, [out_transition])
        self.assertFalse(s1.no_exit())

    def test_has_exit(self):
        out_transition = {
            'name': 't2a',
            'destination': '21',
            'link': [],
            'observable': None,
            'relevant': None}
        s1 = State('21', True, [out_transition])
        self.assertTrue(s1.no_exit())

    def test_check_null_out_transitions(self):
        out_transition = {
            'name': None,
            'destination': None,
            'link': [{
                'type': None,
                'link': None,
                'event': None}],
            'observable': None,
            'relevant': None}
        s1 = State('21', True, [out_transition])
        self.assertTrue(s1.check)

    def test_check_null_out_transition(self):
        out_transition = {
            'name': 't2a',
            'destination': '21',
            'link': [{
                'type': None,
                'link': None,
                'event': None}],
            'observable': None,
            'relevant': None}
        s1 = State('21', True, [out_transition])
        self.assertFalse(s1.check())

    def test_check_duplicate_out_transaction(self):
        out_transition1 = {
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
            'observable': None,
            'relevant': None}
        out_transition2 = {
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
            'observable': None,
            'relevant': None}
        s1 = State('21', True, [out_transition1, out_transition2])
        self.assertFalse(s1.check())

    def test_out_transaction(self):
        out_transition1 = {
            'name': 't2a',
            'destination': '21',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e3'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': None}
        out_transition2 = {
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
            'observable': None,
            'relevant': None}
        s1 = State('21', True, [out_transition1, out_transition2])
        self.assertTrue(s1.check)


if __name__ == '__main__':
    unittest.main()
