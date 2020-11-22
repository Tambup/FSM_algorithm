import json
from core.ComportamentalFANetwork import ComportamentalFANetwork
import pickle
from threading import Lock


mutex = Lock()
finished = False


def read_binary(binary_file):
    return pickle.load(binary_file)


def read_json(jsonText):
    bind_data = json.loads(jsonText)
    return ComportamentalFANetwork(name=bind_data['name'],
                                   CFAs=bind_data['comportamentalFA'])


def write_result(task, out_file, early_terminition=False):
    global finished
    with mutex:
        if not finished:
            finished = True
            result = json.dumps(task.dict_per_json(), indent=4)
            dot_index = out_file.name.rindex('.')
            bin_name = out_file.name[:dot_index+1] + 'pkl'
            with open(bin_name, 'wb') as output:
                pickle.dump(task, output, pickle.DEFAULT_PROTOCOL)
            if early_terminition:
                out_file.write('Forced to stop before termination!\n')
            out_file.write(result)
            out_file.write('\n')
            out_file.close()
