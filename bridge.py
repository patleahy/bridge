# Solution to the bridge and touch problem. 
#
# Pass a list of people's names and times to cross the bridge
#
# Example: 
#   python3 bridge.py me 1 assistant 2 janitor 5 prof 10
#
# Don't use the same name twice.
#
# The runtime complexity of this is terrible (see https://oeis.org/A167484). 
# This can only resinable be run up to 6 people.
#
# There is a solution in n^2 time.
# See http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.296.7287&rep=rep1&type=pdf

import copy
import sys

# Enumerate all the ways that crossing can happen. Two people will cross and one person will return each time.
# By convention people wat to travel from left to right accross the bridge.
#
def main(people):
    
    # Get the trivial cases out of the way.
    if len(people) == 1:
        print_steps(people, { 'steps': [ list(people.keys())[0] ], 'time': list(people.values())[0] })
        return
    elif len(people) == 2:
        print_steps(people,  { 'steps': [ list(people.keys()) ], 'time': max(people.values()) })
        return

    # How many crossings are needed fo this many people
    step_count = len(people) * 2 - 3

    # Setup the initial state.
    states = [ { 
        'sides': { name: 'left' for name in people },
        'time': 0, 
        'lamp': 'left', 
        'steps': [],
        'key': ''
    } ]
    
    keys = set([ '' ] )
    
    names = list(people.keys())
    names.sort()

    # For each crossing replace states with all the possible states we could be after the crossing.
    for _ in range(step_count):
        new_states = []

        for key in keys:
            states_for_key = [state for state in states if state['key'] == key]
            states_for_key.sort(key = lambda state: state['time'])

            new_states.extend(next_steps(names, people, states_for_key[0]))
        
        states = new_states

        keys = set(state['key'] for state in states)

    print(f'n={len(people)} o={len(states)}')

    # Select the fastest of the options and print it.
    states.sort(key = lambda state: state['time'])
    print_steps(people, states[0])


# For a given state return all the states which could occur after one more crossing.
#
def next_steps(names, people, state):

    people_waiting = [name for name in state['sides'] if state['sides'][name] == state['lamp']]
    
    if state['lamp'] == 'left':

        # If the torch is on the left then enumerate all states when a pairs of people cross from left to right.
        # Alice and Bill is the same as Bill and Alice so only include them once, 'a < b' ensures this.

        for pair in ([a, b] for a in people_waiting for b in people_waiting if a != b and a < b):
            new_state = copy.deepcopy(state)
            new_state['lamp'] = 'right'
            new_state['sides'][pair[0]] = 'right'
            new_state['sides'][pair[1]] = 'right'
            new_state['time'] = new_state['time'] + max(people[pair[0]], people[pair[1]])
            new_state['steps'].append(pair)
            new_state['key'] = ''.join([new_state['sides'][name][0] for name in names]) + 'R'
            yield new_state
    else:
        # If the torch is on the right the enumerate all the states after one person crosses from right to left.

        for single in people_waiting:
            new_state = copy.deepcopy(state)
            new_state['lamp'] = 'left'
            new_state['sides'][single] = 'left'
            new_state['time'] = new_state['time'] + people[single]
            new_state['steps'].append(single)
            new_state['key'] = ''.join([new_state['sides'][name][0] for name in names]) + 'L'
            yield new_state


# Print the steps to get to a given state
#
def print_steps(people, state):
    i = 0
    steps = state['steps']
    for step in steps:
        if isinstance(step, list):
            print(f'Crossing {step[0]} and {step[1]} time {max(people[step[0]], people[step[1]])}')
        else:
            print(f'Returning {step} {people[step]}')
    
    print(f'Total time {state["time"]}')


if __name__ == '__main__':
    people = { sys.argv[i] : int(sys.argv[i+1]) for i in range(1, len(sys.argv), 2) }
    main(people)
