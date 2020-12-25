import argparse
import sys
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSpace import ComportamentalFANSpace
from ComportamentalFANSObservation import ComportamentalFANSObservation
from core.ComportamentalFANetwork import ComportamentalFANetwork
from Diagnosis import Diagnosis
from Diagnosticator import Diagnosticator
import threading
import signal


task_result = None
out_file = None


def term_program(signal, frame):
    global task_result
    global out_file
    UserIO.write_result(task=task_result,
                        out_file=out_file,
                        early_terminition=True)
    sys.exit(0)


def execute(args, input_read):
    global task_result
    options = {
        1: ComportamentalFANSpace,
        2: ComportamentalFANSObservation,
    }
    valid_result = True
    if isinstance(input_read, ComportamentalFANetwork):
        task_result = options[args.type[0]](input_read)
        task_result.build(args.obs_list)
    elif isinstance(input_read, ComportamentalFANSpace) \
            or isinstance(input_read, Diagnosticator) \
            or isinstance(input_read, ComportamentalFANSObservation):
        task_result = input_read
    if args.type[0] == 2 and args.diagnosis:
        if task_result.is_correct():
            task_result = Diagnosis(task_result.space_states, args.obs_list)
            task_result.diagnosis()
        else:
            print('Not valid observation', file=sys.stderr)
            valid_result = False
    elif args.type[0] == 1 and args.diagnosis:
        if isinstance(input_read, Diagnosticator):
            if args.obs_list:
                task_result.linear_diagnosis(args.obs_list)
        elif task_result.is_correct():
            task_result = Diagnosticator(task_result.space_states)
            task_result.build()
            if args.obs_list:
                task_result.linear_diagnosis(args.obs_list)

    if valid_result:
        UserIO.write_result(task_result, args.out_file[0])


def main():
    desc = 'A program to execute different computation on regex described \
        with finite state machines.'
    argParser = argparse.ArgumentParser(description=desc)
    argGroup = argParser.add_argument_group(title='Command list')
    argGroup.add_argument('-t', '--type', dest='type', required=True, nargs=1,
                          type=int, choices=[1, 2],
                          help='The task to accomplish. \n\t\t1 - \
                          Compute the Comportamental FA Network Space \n\t\t2 \
                          - Compute the CFANS relative to an observation')
    argGroup.add_argument('--json', dest='json', nargs=1,
                          type=argparse.FileType('r'),
                          help='File containing the ComportamentalFANetwork')
    argGroup.add_argument('--bin', dest='bin', nargs=1,
                          type=argparse.FileType('rb'),
                          help='File containing the binary structure')
    argGroup.add_argument('-o', '--out-file', dest='out_file', nargs=1,
                          type=argparse.FileType('w+'), required=True,
                          help='File to output results')
    argGroup.add_argument('-O', '--obs-list', dest='obs_list', action='append',
                          help='List of observations. Use -Oo1 -Oo2 if the \
                          observation is o1 followed by o2.')
    argGroup.add_argument('-d', '--diagnosis', dest='diagnosis',
                          action='store_true',
                          help='State that the diagnosis must be computed')
    argGroup.add_argument('-T', '--max-time', dest='max_time',
                          type=float, nargs=1,
                          help='Maximum execution time in seconds')

    args = argParser.parse_args()
    if args.json and args.bin \
            or not args.json and not args.bin:
        print('ERROR: use either json or bin option')
        sys.exit(1)
    elif args.json:
        lines = [line.strip() for line in args.json[0]]
        input_read = UserIO.read_json(''.join(line for line in lines))

        if not input_read.check():
            print('The input describe a malformatted ComportamentalFANetwork',
                  file=sys.stderr)
            sys.exit(1)
    elif args.bin:
        input_read = UserIO.read_binary(args.bin[0])

    global out_file
    out_file = args.out_file[0]
    signal.signal(signal.SIGINT, term_program)
    if args.max_time:
        t = threading.Thread(target=execute,
                             args=[args, input_read],
                             daemon=True)
        t.start()
        t.join(args.max_time[0])
        if t.is_alive():
            UserIO.write_result(task=task_result,
                                out_file=args.out_file[0],
                                early_terminition=True)
    else:
        execute(args, input_read)


if __name__ == '__main__':
    main()
