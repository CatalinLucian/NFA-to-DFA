===============================================================================
Name and surname: Patrascu Catalin-Lucian
						NFA to DFA
===============================================================================

		Subset Construction

	'Subset Construction' is the algorithm implemented in the project.
Its main use is for converting a nondeterministic finite automata to a
deterministic one. In a general sense, a DFA has many advantages over an NFA
and it is used more widely computationally because it is more restrictive 
and as its name says, deterministic. One particular example is when analyzing 
if a word is accepted by a language: in the DFA we can only consider len(word)
steps to check whether the word is accepted, whereas in an NFA with eps
transitions there can be more tree ramifications for reaching a conclusion. 

        In the implementation I used 2 classes, one for DFA, one for NFA, both
of them being used in labs of LFA class course.
        The given NFA was read from a file and its principal fields and
characteristics are the following: 
* 0 is always initial state
* 'numberOfStates' is the given numner of states
* 'alphabet' is the alphabet of the language described by the NFA
* 'finalStates' is a set of all final states
* 'delta' is a dictionary representing all transitions of the NFA
* states are considered integers from 0 to 'numberOfStates' - 1
	The first method implemented was 'epsilonClosure(state)'.
Given a starting state it returns a set of all states reachable from
starting state going only through epsilon transtions. The idea of the function
is that it considers a state as a vertex, epsilon transitions as edges and 
runs an iterative DFS from starting state. In this way I found how deep can I
go through epsilon transitions.
	The bread and butter of the homework is the method 'nfaToDfa'.
The idea can be summarized in some steps:
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
At the end I get a DFA characterized by a total number of states, an initial state,
a set of final states, the same alphabet, a new 'delta' function
The data structures used in the implementation are documented in the source code.
	For the coding style I used the 4 spaces identation convention recognized
by Python.                                     
