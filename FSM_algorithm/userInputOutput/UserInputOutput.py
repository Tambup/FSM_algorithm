import json
from core.ComportamentalFANetwork import ComportamentalFANetwork


def readInput(jsonText) -> ComportamentalFANetwork:
    bindData = json.loads(jsonText)
    return ComportamentalFANetwork(name=bindData['name'],
                                   CFAs=bindData['comportamentalFA'])


def write_result(task, out_file):
    result = json.dumps(task.dict_per_json(),  indent=4)
    out_file[0].write(result)
    out_file[0].write("\n")
