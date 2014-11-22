#Code for homework 3, viterbi, forward-backward

##Problem 1. Viterbi
The code for problem 1 is in the file: hw3viterbi.py. both in regular probabilities and logbase probabilities.
Both functions are included in the __main__ method.
The input file can be specified in the beginning of the file (defaults: emit-cv.txt and trans-cv.txt). 
corresponding functions:
run_viterbi
run_viterbi_logbase


##Problem 2. Forward backward
The code for problem 2 is in the file: hw3fb.py. Both regular probabilities and logbase probabilities are implemented. 
Both functions are included in the __main__ method.
The input file can be specified in the beginning of the file (defaults: emit-cv.txt and trans-cv.txt).
Corresponding functions:
run_fb
run_fb_logbase

##Problem 3. EM
The updated spreadsheet is included in the file/cvbar_spreadsheet(1).xlsx
Now instead of only values, the formulas for 1 step of the EM are included.
The transition and emission estimate from this 1 step are then included in input files: emit-cv-em.txt and trans-cv-em.txt

###1. Does the most probable tag sequence change? If so to what?

No the most probable tag sequence stays the same.
[{'b': 'C'}, {'a': 'V'}, {'r': 'C'}, {'b': 'C'}, {'a': 'V'}, {'r': 'C'}, {'a': 'V'}, {'b': 'C'}, {'a': 'V'}, {'r': 'C'}, {'b': 'C'}, {'a': 'V'}, {'r': 'C'}, {'a': 'V'}]

###2. How does the probability of the most probable sequence change?
The probability of this sequence increases substantially. Specifically it increases from 3.65989380422e-17 to 0.00207508392659.
The reason for that is that the transition probabilities from the first step of the EM, are more extreme.

##3. How does the total forward/backward probability change?
The total fw/bw probability also increases substantially. From 7.661059866669876e-17 to 0.0023143346408825037. The same argument applies here as well.


