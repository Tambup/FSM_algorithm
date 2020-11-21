from userInputOutput import UserInputOutput as UserIO


stop_event = None
out_file = None


def must_stop():
    return stop_event.is_set() if stop_event else False


def set_stop(event):
    global stop_event
    stop_event = event


def set_out_file(output_file):
    global out_file
    out_file = output_file


def close_all(task):
    UserIO.write_result(task=task, out_file=out_file)
