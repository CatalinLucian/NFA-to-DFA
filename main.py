import sys
from typing import List, Tuple, Set, Dict

from collections import deque

State = int
Word = str
Configuration = Tuple[State, Word]
Transition = Tuple[State, Word, List[State]]
EPSILON = ""


class DFA:
    def __init__(self, numberOfStates: int, alphabet: Set[chr], finalStates: Set[State],
                 delta: Dict[Tuple[State, chr], State]):
        self.numberOfStates = numberOfStates
        self.states = set(range(self.numberOfStates))
        self.alphabet = alphabet
        self.initialState = 0
        self.finalStates = finalStates
        self.delta = delta

    def __str__(self):
        string = 'Automatul rezultat are ' + str(self.numberOfStates) + ' stari' + '\n' + \
                 'Stari finale: ' + str(self.finalStates) + '\n' + \
                 'Tranzitii: '

        for i in self.delta:
            string += str(i) + ' : ' + str(self.delta[i]) + '\n'
        return string

    """
    Writes DFA to file in the following form:
        <number of states in the DFA>
        <list of final states in the DFA>
        for every transition in delta
        <transition> 
    :param outputFile: file being written to
    :return: 
    """
    def writeToFile(self, outputFile):

        outputFile.write(str(self.numberOfStates) + '\n')
        finalDfaStates = list(self.finalStates)
        for i in range(len(finalDfaStates)):
            if i == len(finalDfaStates) - 1:
                outputFile.write(str(finalDfaStates[i]) + '\n')
            else:
                outputFile.write(str(finalDfaStates[i]) + " ")

        for transition in self.delta:
            outputFile.write(str(transition[0]) + " ")
            outputFile.write(transition[1] + " ")
            outputFile.write(str(self.delta[transition]) + '\n')

        return

class NFA:
    def __init__(self, numberOfStates: int, alphabet: Set[chr], finalStates: Set[State],
                 delta: Dict[Tuple[State, chr], Set[State]]):
        self.numberOfStates = numberOfStates
        self.states = set(range(self.numberOfStates))
        self.alphabet = alphabet
        self.initialState = 0
        self.finalStates = finalStates
        self.delta = delta

    def __str__(self):
        string = 'Automatul are ' + str(self.numberOfStates) + ' stari' + '\n' + \
                 'Stari finale: ' + str(self.finalStates) + '\n' + \
                 'Tranzitii: '

        for i in self.delta:
            string = string + str(i) + str(delta[i]) + ' '
        return string

    """
    Calculates the Epsilon Closure for a state in DFA
    Given a starting state we should return a list of all
    states reachable from starting states going only through
    epsilon transtions
    For this we can consider a directed graph with states as
    vertices and epsilon transitions as edges
    On this graph we run DFS with given starting state as source
    :param state: state to which we want its epsilon closure
    :return: a set of all reachable states 
    """
    def epsilonClosure(self, state: State) -> Set[State]:
        toBeReturned = set()

        # aux is a dictionary only with epsilon transitions
        # it is included in delta
        # can be seen as an adjacency list of my graph
        aux = {}
        for i in self.delta:
            if i[1] == EPSILON:
                aux[i[0]] = self.delta[i]

        # run a DFS on the aux adjacency list
        stack = deque()
        # visited keeps track of visited states
        visited = [0 for i in range(self.numberOfStates)]

        if state in aux:
            for i in aux[state]:
                stack.append(i)
                toBeReturned.add(i)

        visited[state] = 1

        while stack:
            current = stack.pop()
            if visited[current] == 0:
                if current in aux:
                    for i in aux[current]:
                        stack.append(i)
                        toBeReturned.add(i)
                visited[current] = 1

        toBeReturned.add(state)
        return toBeReturned

    """
    Apply subset construction on my initial NFA to obtain a DFA
    First of all I form the initial DFA state by calculating
    the epsilon closure of 0. The principal data structures used
    in the algorithm are a queue (where I enqueue the new states
    to be analyzed) and a 'visited' list (which tells whether a
    DFA state was analyzed before or not).
    The principal idea of the algo can be summarized in few steps:
    1. The initial DFA state is the epsilon closure of 0
    2. Add the initial DFA state to a queue
    3. For every front DFA state of the queue do the following after dequeing it
    4. If it was visited then I should not analyze it because it was 
    analyzed before
    5. If not visited, then I iterate through every letter of the alphabet
    6. For every letter form a new set of states which consists of the states
    reachable from every state of the newly formed DFA state, through current
    letter in one step
    7. For every state in the previous constructed set, apply its epsilon closure
    resulting in a potentially new set. This set is a new DFA state
    8. Append it to queue
    9. Populate delta of DFA
    10. Mark the current state as visited
    11. Repeat steps 3-10 while queue is not empty 
    12. Identify all the final states 
    13. In the end there is some manipulation of data structures for the DFA
    to be returned correctly 
    :return: The newly formed DFA
    """
    def nfaToDfa(self):
        # this is the initial state of the DFA
        initialStateDfa = self.setToOrderedTuple(self.epsilonClosure(0))
        numberOfDfaStates = 0
        codificationDict = {}
        deltaDFA = {}
        final_states = set()

        # init queue
        q = deque()
        # and list which keeps track of visited states
        visited = []

        q.append(initialStateDfa)

        while q:
            # take the current DFA state
            currentDFAState = q.popleft()
            # if it wasn't visited before
            if currentDFAState not in visited:
                numberOfDfaStates += 1
                # then for every transition in my NFA of the form
                # (nfaState, letter) -> newNfaState
                # where 'nfaState' is every state of my DFA state
                for letter in self.alphabet:
                    aux = set()
                    for s in currentDFAState:
                        if (s, letter) in self.delta:
                            # Form a new DFA state consisting of
                            # my newNFAStates states and their
                            # epsilon closure
                            aux.update(self.delta[(s, letter)])
                            temp = self.setToOrderedTuple(aux)
                            for i in temp:
                                aux.update(self.epsilonClosure(i))
                    # add new transitionj to my DFA
                    deltaDFA[(currentDFAState, letter)] = self.setToOrderedTuple(aux)
                    # append new state to q
                    q.append(self.setToOrderedTuple(aux))
                    codificationDict[currentDFAState] = numberOfDfaStates - 1
                # mark the analyzed DFA state as visited
                visited.append(currentDFAState)

        deltaAfterDecoding = {}
        for transition in deltaDFA:
            x = codificationDict[transition[0]]
            y = codificationDict[deltaDFA[transition]]
            deltaAfterDecoding[(x, transition[1])] = y

        for transition in deltaDFA:
            for j in transition[0]:
                if j in self.finalStates:
                    final_states.add(codificationDict[transition[0]])

        dfa = DFA(numberOfDfaStates, self.alphabet, final_states, deltaAfterDecoding)

        return dfa

    """
    I used an ordered tuple to keep track of the DFA state
    For example: After subset construction, the DFA state
    '012' will be codificated as the tuple (0, 1, 2)
    I used tuples because it is immutable and can be key in 
    dictionary 
    :param mySet: The DFA state 
    :return: The DFA state as ordered tuple
    """
    def setToOrderedTuple(self, mySet: Set[State]):
        s = sorted(mySet)
        return tuple(s)

if __name__ == '__main__':

    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w+")
    input = input_file.read().splitlines()

    numberOfStates = int(input[0])
    final_states = set(map(int, input[1].rstrip().split(" ")))

    delta = {}

    for i in range(2, len(input)):
        line = input[i].split()
        state = int(line[0])
        symbol = line[1]
        if symbol == 'eps':
            symbol = EPSILON
        aux = line[2:]
        next_states = set([int(i) for i in aux])
        delta[(state, symbol)] = next_states

    initial_states = 0
    alphabet = set()
    for transition in delta:
        alphabet.add(transition[1])
    if EPSILON in alphabet:
        alphabet.remove(EPSILON)
    states = [str(i) for i in range(numberOfStates)]

    nfa = NFA(numberOfStates, alphabet, final_states, delta)
    result = nfa.nfaToDfa()
    result.writeToFile(output_file)


