import argparse
import select
import sys
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSpace import ComportamentalFANSpace
from ComportamentalFANSObservation import ComportamentalFANSObservation
from Diagnosis import Diagnosis
from Diagnosticator import Diagnosticator


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
    argGroup.add_argument('-f', '--file', dest='file', nargs=1,
                          type=argparse.FileType('r'),
                          help='File containing the ComportamentalFANetwork')
    argGroup.add_argument('-o', '--out-file', dest='out_file', nargs=1,
                          type=argparse.FileType('w+'), required=True,
                          help='File to output results')
    argGroup.add_argument('-O', '--obs-list', dest='obs_list', action='append',
                          help='List of observations')
    argGroup.add_argument('-d', '--diagnosis', dest='diagnosis',
                          action='store_true',
                          help='State that the diagnosis must be computed')

    args = argParser.parse_args()
    lines = ''
    if not args.file:
        if select.select([sys.stdin], [], [], 0.0)[0]:
            lines = [line.strip() for line in sys.stdin]
        else:
            print(('Use one between -f option or string unassociated '
                  'with -like option is mandatory or input redirection'),
                  file=sys.stderr)
    else:
        lines = [line.strip() for line in args.file[0]]

    cfaNetwork = UserIO.readInput(''.join(line for line in lines))

    if not cfaNetwork.check():
        print('The input describe a malformatted ComportamentalFANetwork',
              file=sys.stderr)

    options = {
        1: ComportamentalFANSpace,
        2: ComportamentalFANSObservation,
    }
    valid_result = True
    task_result = options[args.type[0]](cfaNetwork)
    task_result.build(args.obs_list)
    if args.type[0] == 2 and args.diagnosis:
        if task_result.is_correct():
            task_result = Diagnosis(task_result.space_states)
            task_result.diagnosis()
        else:
            print('Not valid observation', file=sys.stderr)
            valid_result = False
    elif args.type[0] == 1 and args.diagnosis:
        if task_result.is_correct():
            task_result = Diagnosticator(task_result.space_states)
            task_result.build()

    if valid_result:
        UserIO.write_result(task_result, args.out_file)


if __name__ == '__main__':
    main()
