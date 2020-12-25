from .ComportamentalFA import ComportamentalFA


class ComportamentalFANetwork():
    def __init__(self, name, CFAs):
        self._name = name
        self._comportamentalFAs = []
        for cfa in CFAs:
            self._comportamentalFAs.append(ComportamentalFA(name=cfa["name"],
                                           states=cfa["state"]))

    @property
    def name(self):
        return self._name

    @property
    def comportamentalFAs(self):
        return self._comportamentalFAs

    def in_links(self):
        return {link for compFa in self._comportamentalFAs
                for link in compFa.in_links()}

    def out_links(self):
        return {link for compFa in self._comportamentalFAs
                for link in compFa.out_links()}

    def check(self):
        if self._comportamentalFAs is None:
            return False

        if len(self._comportamentalFAs) < 1:
            return False

        for compFA in self._comportamentalFAs:
            if compFA is None:
                return False

        for compFA in self._comportamentalFAs:
            if not compFA.check():
                return False

        if len(self._comportamentalFAs) > 1:
            for compFA in self._comportamentalFAs:
                for in_link in compFA.in_links():
                    num_out = 0
                    for inner_compFA in self._comportamentalFAs:
                        if compFA is not inner_compFA:
                            inner_in_links = inner_compFA.in_links()
                            if set([in_link]).issubset(inner_in_links):
                                return False

                            for inner_out_link in inner_compFA.out_links():
                                if in_link == inner_out_link:
                                    num_out += 1
                                if num_out > 1:
                                    return False

                    if num_out != 1:
                        return False

                for out_link in compFA.out_links():
                    num_in = 0
                    for inner_compFA in self._comportamentalFAs:
                        if compFA is not inner_compFA:
                            inner_out_links = inner_compFA.out_links()
                            if set([out_link]).issubset(inner_out_links):
                                return False

                            for inner_in_link in inner_compFA.in_links():
                                if out_link == inner_in_link:
                                    num_in += 1
                                if num_in > 1:
                                    return False

                    if num_in != 1:
                        return False

        return True
