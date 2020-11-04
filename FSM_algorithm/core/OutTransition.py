class OutTransition():
    def __init__(self, name, destination, links, observable, relevant):
        self._name = name
        self._destination = destination
        self._links = frozenset(
            (link['link'], link['type'], link['event']) for link in links
            )
        self._observable = observable
        self._relevant = relevant

    @property
    def name(self):
        return self._name

    @property
    def destination(self):
        return self._destination

    @property
    def observable(self):
        return self._observable

    @property
    def relevant(self):
        return self._relevant

    @property
    def links(self):
        return self._links

    def in_links(self):
        return [link[0] for link in self._links if link[1] == 'in']

    def out_links(self):
        return [link[0] for link in self._links if link[1] == 'out']

    def check(self):
        if self._destination is None:
            return False

        for link in self._links:
            if link[0] is None or link[1] is None or link[1] is None:
                return False

        in_link_exist = False
        for _, link_type, _ in self._links:
            if link_type == 'in':
                if in_link_exist:
                    return False
                in_link_exist = True

        for link in self._links:
            for inner_link in self._links:
                if link is not inner_link:
                    if link[1] == 'out' and inner_link[1] == 'out':
                        if link[0] == inner_link[0]:
                            return False
        return True

    def __eq__(self, obj):
        if isinstance(obj, OutTransition):
            if self._name == obj.name and self._destination == obj.destination:
                if self._links is not None and self._observable is not None \
                        and self._relevant is not None \
                        and obj.links is not None \
                        and obj.observable is not None \
                        and obj.relevant is not None:
                    if self._same_vectors(obj):
                        return True
        return False

    def __hash__(self):
        return hash((self._name, self._destination, self._links))

    def _same_vectors(self, obj):
        return all(elem in self._links for elem in obj.links) and \
                all(elem in obj.links for elem in self._links) and \
                all(elem in self._observable for elem in obj.observable) and \
                all(elem in obj.observable for elem in self._observable) and \
                all(elem in self._relevant for elem in obj.relevant) and \
                all(elem in obj.relevant for elem in self._relevant)

    def sameEvents(self, oth_links):
        both_null = False
        if self._links is None or oth_links is None:
            if self._links is not None or oth_links is not None:
                return False
            else:
                both_null = True

        if not both_null:
            for link in self._links:
                is_contained = False
                for oth_link in oth_links:
                    if link[2] == oth_link[2]:
                        if link[1] == oth_link[1]:
                            is_contained = True
                            break
                if not is_contained:
                    return False

            for oth_link in oth_links:
                is_contained = False
                for link in self._links:
                    if link[2] == oth_link[2]:
                        if link[1] == oth_link[1]:
                            is_contained = True
                            break
                if not is_contained:
                    return False
            return True

        return False
