import json
from core.ComportamentalFANetwork import ComportamentalFANetwork


def readInput(jsonText) -> ComportamentalFANetwork:
    bindData = json.loads(jsonText)
    return ComportamentalFANetwork(name=bindData["name"],
                                   CFAs=bindData["comportamentalFA"])
