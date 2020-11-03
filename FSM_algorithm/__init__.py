import argparse
import select
import sys
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSpace import ComportamentalFANSpace
from ComportamentalFANSObservation import ComportamentalFANSObservation


def _execute(task, outFile):
    task.build()


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
        print("The input describe a malformatted ComportamentalFANetwork",
              file=sys.stderr)

    options = {
        1: ComportamentalFANSpace,
        2: ComportamentalFANSObservation
    }
    _execute(options[args.type[0]](cfaNetwork), args.out_file)


if __name__ == '__main__':
    main()
