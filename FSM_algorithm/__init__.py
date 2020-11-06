import argparse
import select
import sys
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSpace import ComportamentalFANSpace
from ComportamentalFANSObservation import ComportamentalFANSObservation
from core.State import State
from core.OutTransition import OutTransition


def _execute(task, out_file, param=None):
    task.build(param)
    UserIO.write_result(task, out_file)


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

    test = ComportamentalFANSpace(cfaNetwork)
    test.build()
    space = test._space_states
    print(space[0]._links['L3'])

    outTransition = {
            "name": "t3a",
            "destination": "31",
            "link": [{
                "type": "out",
                "link": "L2",
                "event": "e2"}],
            "observable": ["o3"],
            "relevant": []}
    link = {
            "type": "out",
            "link": "L2",
            "event": "e2"}
   



    
    '''
    param = args.obs_list
    options = {
        1: ComportamentalFANSpace,
        2: ComportamentalFANSObservation
    }
    _execute(options[args.type[0]](cfaNetwork), args.out_file, param=param)
    '''


if __name__ == '__main__':
    main()
