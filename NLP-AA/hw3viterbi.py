'''
Created on Oct 30, 2014

@author: rmn
'''
import json

path_emit = 'files/emit-cv.txt'
path_observed = 'files/obs-cvbarbarabarbara.txt'
path_trans = 'files/trans-cv.txt'

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

# print observed
# print trans
table = [{}] * (len(observed))  # initialize marginal probabilities
best_tag_seq = []
best_tags_probs = []
for i in range(len(observed)):
    print i
    print table
    if i == 0:
        # initialize
        d = {}
        for t in tags:
            d[t] = {
                'prob': trans[('#', t)] * emit[(t, observed[i])], 'best': '#'}
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
            d[t] = {'best': a, 'prob': b}
        table[i] = d


def max_label(elements):
    max = 0
    max_lbl = ''
    for k, v in elements.iteritems():
        if v['prob'] > max:
            max = v['prob']
            max_lbl = k
    return max_lbl

best_sequence = [{}] * len(observed)
best_sequence[len(
    observed) - 1] = {observed[len(observed) - 1]: max_label(table[len(observed) - 1])}
for i in reversed(range(len(observed) - 2)):
    best_sequence[i] = {
        observed[i]: table[i + 1][best_sequence[i + 1]]['best']}
print '\n'.join([observed[i] + ' ' + str(table[i]) for i in range(len(table))])
