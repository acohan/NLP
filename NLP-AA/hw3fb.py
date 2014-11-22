'''
Created on Oct 30, 2014

@author: rmn
'''
from numpy import log
from numpy import exp
from numpy import logaddexp
from copy import deepcopy

from tabulate import tabulate

path_emit = 'files/emit-cv.txt'
# path_emit = 'files/emit-cv-em.txt'
path_trans = 'files/trans-cv.txt'
# path_trans = 'files/trans-cv-em.txt'
path_observed = 'files/obs-cvbarbarabarbara.txt'
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


def run_fb(observed, emit, trans, tags):
    """
    Forward Backward
    Returns table of forward, backward and marginal probs
    :arg observed: the observed sequence list
    :arg emit: emission probabilities, format:
        {('hidden1','observed1'): 0.4, ...}
    :arg trans: transition probabilities, format:
        {('hidden1','hidden2'): 0.4, ...}
    :arg tags: a set of hidden variables, eg. set('C','V')

    """
    fwd = [{}] * (len(observed) + 2)  # initialize forward table
    fwd[0] = {t: 1 for t in tags}
    fwd[0]['#'] = 1
    tag_set = tags
    for i in range(len(observed)):
        d = {}
        for t in tags:
            probs = {}
            if i == 0:
                tag_set = {'#'}
            for t2 in tag_set:  # previous tag
                # probs stores the probability of element i to have
                # tag t given the previous tag is t2
                # then we use this to maximise
                probs[t2] = (fwd[i][t2]) * \
                    trans[(t2, t)] * emit[(t, observed[i])]
            a = sum(probs.values())
#                 a = sum(
#                     probs.values())
            d[t] = a
        fwd[i + 1] = d
        tag_set = deepcopy(tags)
    totalfw = sum(fwd[len(observed)].values())
    fwd[len(observed) + 1] = {t:
                              totalfw for t in tags}

    back = [{}] * (len(observed) + 2)  # initialize forward table
    back[len(observed) + 1] = {t: 1 for t in tags}
    back[len(observed)] = {t: 1 for t in tags}
    for i in reversed(range(len(observed) - 1)):
        d = {}
        for t in tags:
            probs = {}
            for t2 in tags:  # next tag
                # probs stores the probability of element i to have
                # tag t given the next tag is t2
                probs[t2] = back[i + 2][t2] * \
                    trans[(t, t2)] * emit[(t2, observed[i + 1])]
            a = sum(probs.values())
            d[t] = a
        back[i + 1] = d
    probs = {}
    for t2 in tags:  # next tag
        # probs stores the probability of element i to have
        # tag t given the next tag is t2
        probs[t2] = back[1][t2] * \
            trans[('#', t2)] * emit[(t2, observed[0])]
    totalbw = sum(probs.values())
    back[0] = {t: totalbw for t in tags}

    marginal = [{}] * (len(observed))
    input = [{}] * (len(observed) + 2)
    for i in range(len(observed)):
        input[i + 1] = observed[i]
    input[0] = '#'
    input[len(observed) + 1] = '$'
    for i in range(len(observed)):
        total = sum([(fwd[i + 1][t] * back[i + 1][t]) for t in tags])
        d = {t: (fwd[i + 1][t] * back[i + 1][t]) / float(total) for t in tags}
        marginal[i] = d

    print "-- Total Forward Probability: " + str(totalfw)
    print "-- Total Backward Probability: " + str(totalbw)
    print "---- Forward probabilities: ----- "
    print tabulate(zip(input, fwd))
    print "---- Backward probabilities: ----- "
    print tabulate(zip(input, back))
    print "---- Marginal probabilities ----"
    print tabulate(zip(observed, marginal))
    return fwd, back, marginal


def run_fb_logbase(observed, emit, trans, tags):
    """
    Forward Backward in logarithmic space
    Returns table of forward, backward and marginal negative log probs
    :arg observed: the observed sequence list
    :arg emit: emission probabilities, format:
        {('hidden1','observed1'): 0.4, ...}
    :arg trans: transition probabilities, format:
        {('hidden1','hidden2'): 0.4, ...}
    :arg tags: a set of hidden variables, eg. set('C','V')

    """
    fwd = [{}] * (len(observed) + 2)  # initialize forward table
    fwd[0] = {t: log(1) for t in tags}
    fwd[0]['#'] = log(1)
    for i in range(len(observed)):
        d = {}
        for t in tags:
            probs = {}
            if i == 0:
                tag_set = {'#'}
            for t2 in tag_set:  # previous tag
                # probs stores the probability of element i to have
                # tag t given the previous tag is t2
                # then we use this to sum
                probs[t2] = (fwd[i][t2]) + \
                    log(trans[(t2, t)]) + log(emit[(t, observed[i])])
            a = reduce(logaddexp, probs.values())
#                 a = sum(
#                     probs.values())
            d[t] = a
        fwd[i + 1] = d
        tag_set = deepcopy(tags)
    totalfw = reduce(logaddexp, fwd[len(observed)].values())
    fwd[len(observed) + 1] = {t: totalfw for t in tags}

    back = [{}] * (len(observed) + 2)  # initialize forward table
    back[len(observed) + 1] = {t: log(1) for t in tags}
    back[len(observed)] = {t: log(1) for t in tags}
    for i in reversed(range(len(observed) - 1)):
        d = {}
        for t in tags:
            probs = {}
            for t2 in tags:  # next tag
                # probs stores the probability of element i to have
                # tag t given the next tag is t2
                probs[t2] = back[i + 2][t2] + \
                    log(trans[(t, t2)]) + log(emit[(t2, observed[i + 1])])
            a = reduce(logaddexp, probs.values())
            d[t] = a
        back[i + 1] = d
    for t2 in tags:  # next tag
        # probs stores the probability of element i to have
        # tag t given the next tag is t2
        probs[t2] = back[1][t2] + \
            log(trans[('#', t2)]) + log(emit[(t2, observed[0])])
    totalbw = reduce(logaddexp, probs.values())
    back[0] = {t: totalbw for t in tags}

    marginal = [{}] * (len(observed))
    input = [{}] * (len(observed) + 2)
    for i in range(len(observed)):
        input[i + 1] = observed[i]
    input[0] = '#'
    input[len(observed) + 1] = '$'
    for i in range(len(observed)):
        total = reduce(
            logaddexp, [fwd[i + 1][t] + back[i + 1][t] for t in tags])
        d = {t: (fwd[i + 1][t] + back[i + 1][t]) - total for t in tags}
        marginal[i] = d

#     marginal = [{}] * (len(observed))
#     input = [{}] * (len(observed) + 2)
#     for i in range(len(observed)):
#         input[i + 1] = observed[i]
# input[0] = '#'
#     input[len(observed) + 1] = '$'
#     for i in range(len(observed)):
#         d = {t: fwd[i + 1][t] + back[i + 1][t] for t in tags}
#         marginal[i] = d
    print "-- Total Forward Negative Log Probability: %f" % totalfw
    print "-- Total Backward Negative Log Probability: %f" % totalbw
    print "---- Forward Neg. Log. probabilities: ----- "
    print tabulate(zip(input, fwd))
    print "---- Backward Neg. Log. probabilities: ----- "
    print tabulate(zip(input, back))
    print "---- Negative Log marginal probabilities ----"
    print tabulate(zip(observed, marginal))
    return fwd, back, marginal


if __name__ == '__main__':
    observed, emit, trans, tags = preprocess(
        path_observed, path_emit, path_trans)
    fwd, back, marginal = run_fb(observed, emit, trans, tags)
    fwd1, back1, marginal1 = run_fb_logbase(observed, emit, trans, tags)
#     print marginal
#     for t in marginal1:
#         print {k: exp(v) for k,v in t.iteritems()}
