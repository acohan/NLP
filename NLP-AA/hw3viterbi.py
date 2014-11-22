'''
Created on Oct 30, 2014

@author: rmn
'''
from numpy import log
from tabulate import tabulate

path_emit = 'files/emit-cv.txt'
# path_emit = 'files/emit-cv-em.txt'
path_trans = 'files/trans-cv.txt'
# path_trans = 'files/trans-cv-em.txt'
path_observed = 'files/obs-cvbarbarabarbara.txt'


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


def run_viterbi(observed, emit, trans, tags, verbose=False):
    table = [{}] * (len(observed))  # initialize marginal probabilities
    for i in range(len(observed)):
        if i == 0:
            # initialize
            d = {}
            for t in tags:
                d[t] = {
                    'prob': trans[('#', t)] *
                    emit[(t, observed[i])], 'best_prev': '#'}
            table[i] = d
        else:
            d = {}
            for t in tags:
                probs = {}
                for t2 in tags:  # previous tag
                    # probs stores the probability of element i to have
                    # tag t given the previous tag is t2
                    # then we use this to maximise
                    probs[t2] = table[i - 1][t2]['prob'] * \
                        trans[(t2, t)] * emit[(t, observed[i])]
                a, b = max(
                    probs.iteritems(), key=lambda x: x[1])
                d[t] = {'best_prev': a, 'prob': b}
            table[i] = d

    best_sequence = [{}] * len(observed)
    best_sequence[len(
        observed) - 1] = {observed[len(observed) - 1]:
                          max(table[len(observed) - 1].iteritems(), key=lambda x: x[1])[0]}
    for i in reversed(range(len(observed) - 1)):
        best_sequence[i] = {
            observed[i]:
            table[i + 1][best_sequence[i + 1].
                         values()[0]]['best_prev']}
    if verbose:
        print tabulate(table)
    return best_sequence,\
        max(table[len(observed) - 1].items(),
            key=lambda x: x[1]['prob'])[1]['prob']


def run_viterbi_logbase(observed, emit, trans, tags, verbose=False):
    table = [{}] * (len(observed))  # initialize marginal probabilities
    for i in range(len(observed)):
        if i == 0:
            # initialize
            d = {}
            for t in tags:
                d[t] = {
                    'prob': log(trans[('#', t)]) +
                    log(emit[(t, observed[i])]), 'best_prev': '#'}
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
                d[t] = {'best_prev': a, 'prob': b}
            table[i] = d

    best_sequence = [{}] * len(observed)
    best_sequence[len(
        observed) - 1] = {observed[len(observed) - 1]:
                          max(table[len(observed) - 1].iteritems(), key=lambda x: x[1])[0]}
    for i in reversed(range(len(observed) - 1)):
        best_sequence[i] = {
            observed[i]:
            table[i + 1][best_sequence[i + 1].
                         values()[0]]['best_prev']}
    if verbose:
        print tabulate(table)
    return best_sequence,\
        max(table[len(observed) - 1].items(),
            key=lambda x: x[1]['prob'])[1]['prob']


if __name__ == '__main__':
    observed, emit, trans, tags = preprocess(
        path_observed, path_emit, path_trans)
    print "Best Sequence: %s \n Probability: %s " %\
        run_viterbi(observed, emit, trans, tags, verbose=False)
    print "Best Sequence: %s \n Neg Log Probability: %s " %\
        run_viterbi_logbase(observed, emit, trans, tags, verbose=False)
