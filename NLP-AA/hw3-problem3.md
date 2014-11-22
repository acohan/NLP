#homework 3, part 3. (EM)
##1. Does the most probable tag sequence change? If so to what?

No the most probable tag sequence stays the same.
[{'b': 'C'}, {'a': 'V'}, {'r': 'C'}, {'b': 'C'}, {'a': 'V'}, {'r': 'C'}, {'a': 'V'}, {'b': 'C'}, {'a': 'V'}, {'r': 'C'}, {'b': 'C'}, {'a': 'V'}, {'r': 'C'}, {'a': 'V'}]

##2. How does the probability of the most probable sequence change?
The probability of this sequence increases substantially. Specifically it increases from 3.65989380422e-17 to 0.00207508392659.
The reason for that is that the transition probabilities from the first step of the EM, are more extreme.

##3. How does the total forward/backward probability change?
The total fw/bw probability also increases substantially. From 7.661059866669876e-17 to 0.0023143346408825037. The same argument applies here as well.
