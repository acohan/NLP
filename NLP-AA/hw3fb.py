'''
Created on Oct 30, 2014

@author: rmn
'''
from numpy import log

path_emit = 'files/emit-cv.txt'
path_observed = 'files/obs-cvbarbarabarbara.txt'
path_trans = 'files/trans-cv.txt'
start_character = '#'
end_character = '$'


def preprocess(path_observed, path_emit, path_trans, tags={'C', 'V'}):
    trans = {}
    emit = {}
    tags = {'C', 'V'}
    with open(path_trans, 'rb') as mf:
        data = mf.read()
    for line in data.split('\n'):
        if line != '':
            e = line.split(' ')
            trans[(e[0], e[1])] = float(e[2])

    with open(path_emit, 'rb') as mf:
        data = mf.read()
    for line in data.split('\n'):
        if line != '':
            e = line.split(' ')
            emit[(e[0], e[1])] = float(e[2])

    line = open(path_observed, 'rb').read().split('\n')[0]
    observed = line.split(' ')[:-1]
    return observed, emit, trans, tags

# print observed
# print trans


def run_forward(observed, emit, trans, tags):
    fwd = [{}] * (len(observed) + 2)  # initialize forward table
    fwd[0] = {t: 1 for t in tags}
    for i in range(len(observed)):
        if i == 1:
            # initialize
            d = {}
            for t in tags:
                d[t] = trans[('#', t)] *\
                    emit[(t, observed[i])]
            fwd[i + 1] = d
        else:
            d = {}
            for t in tags:
                probs = {}
                for t2 in tags:  # previous tag
                    # probs stores the probability of element i to have
                    # tag t given the previous tag is t2
                    # then we use this to maximise
                    probs[t2] = fwd[i][t2] * \
                        trans[(t2, t)] * emit[(t, observed[i])]
                a = sum(
                    probs.values())
                d[t] = a
            fwd[i + 1] = d
    fwd[len(observed) + 1] = {t:
                              sum(fwd[len(observed)].values()) for t in tags}

    back = [{}] * (len(observed) + 2)  # initialize forward table
    back[len(observed) + 1] = {t: 1 for t in tags}
    for i in reversed(range(len(observed))):
        if i == len(observed):
            # initialize
            d = {t: 1 for t in tags}
            back[i + 1] = d
        else:
            d = {}
            for t in tags:
                probs = {}
                for t2 in tags:  # next tag
                    # probs stores the probability of element i to have
                    # tag t given the next tag is t2
                    probs[t2] = back[i+2][t2] * \
                        trans[(t, t2)] * emit[(t2, observed[i])]
                a = sum(
                    probs.values())
                d[t] = a
            back[i + 1] = d
    back[0] = {t: sum(back[1].values()) for t in tags}
    
    marginal = [{}] * (len(observed)) 
    for i in range(len(observed)):
        d = {t:fwd[i+1][t]*back[i+1][t] for t in tags}
        marginal[i] = d
        
    print back[0]
    print fwd[len(fwd)-1]
    print marginal


def run_viterbi_logbase(observed, emit, trans, tags):
    table = [{}] * (len(observed))  # initialize marginal probabilities
    for i in range(len(observed)):
        if i == 0:
            # initialize
            d = {}
            for t in tags:
                d[t] = {
                    'prob': log(trans[('#', t)]) +
                    log(emit[(t, observed[i])]), 'best': '#'}
            table[i] = d
        else:
            d = {}
            for t in tags:
                probs = {}
                for t2 in tags:  # previous tag
                    # probs stores the probability of element i to have
                    # tag t given the previous tag is t2
                    # then we use this to maximise
                    probs[t2] = table[i - 1][t2]['prob'] +\
                        log(trans[(t2, t)]) + log(emit[(t, observed[i])])
                a, b = max(
                    probs.iteritems(), key=lambda x: x[1])
                d[t] = {'best': a, 'prob': b}
            table[i] = d

    best_sequence = [{}] * len(observed)
    best_sequence[len(
        observed) - 1] = {observed[len(observed) - 1]:
                          min(table[len(observed) - 1].iteritems(), key=lambda x: x[1])[0]}
    for i in reversed(range(len(observed) - 1)):
        best_sequence[i] = {
            observed[i]:
            table[i + 1][best_sequence[i + 1].
                         values()[0]]['best']}
#     print '\n'.join([observed[i] + ' ' + str(table[i])
#                      for i in range(len(table))])
    return best_sequence,\
        min(table[len(observed) - 1].items(),
            key=lambda x: x[1]['prob'])[1]['prob']


if __name__ == '__main__':
    observed, emit, trans, tags = preprocess(
        path_observed, path_emit, path_trans)
    print run_forward(observed, emit, trans, tags)
