import unittest
from core.OutTransition import OutTransition


class TestStringMethods(unittest.TestCase):
    def test_null_events(self):
        link1 = {
            'type': None,
            'link': None,
            'event': None
        }

        out_transition1 = OutTransition('t2a', '21', [link1], [], [])
        self.assertFalse(out_transition1.links is None)

    def test_null_event(self):
        link1 = {
            'type': None,
            'link': None,
            'event': None}
        OutTransition('t2a', '21', [link1], [], [])

    def test_check_with_null(self):
        link1 = [{
            'type': 'in',
            'link': 'L2',
            'event': 'e2'},
            {
            'type': None,
            'link': None,
            'event': None}]
        out_transition1 = OutTransition('t2a', '21', link1, [], [])
        self.assertFalse(out_transition1.check())

    def test_same_event_same_type(self):
        link1 = {
            'type': 'in',
            'link': 'L2',
            'event': 'e2'}
        link2 = {
            'type': 'in',
            'link': 'L2',
            'event': 'e2'}
        OutTransition('t2a', '21', [link1, link2], [], [])


if __name__ == '__main__':
    unittest.main()
