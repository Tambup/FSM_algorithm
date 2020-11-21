import json
from core.ComportamentalFANetwork import ComportamentalFANetwork


def readInput(jsonText) -> ComportamentalFANetwork:
    bindData = json.loads(jsonText)
    return ComportamentalFANetwork(name=bindData['name'],
                                   CFAs=bindData['comportamentalFA'])


def write_result(task, out_file, early_terminition=False):
    result = json.dumps(task.dict_per_json(), indent=4)
    if early_terminition:
        out_file.write('Forced to stop before termination!\n')
    out_file.write(result)
    out_file.write('\n')
    out_file.close()
