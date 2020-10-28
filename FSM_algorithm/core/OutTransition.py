from enum import Enum


class OutTransition():
    def __init__(self, name, destination, links, observable, relevant):
        self.name = name
        self.destination = destination
        self.links = {
            link['link']: (link['type'], link['event']) for link in links
            }
        self.observable = observable
        self.relevant = relevant
