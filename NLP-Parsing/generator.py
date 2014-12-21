'''
Created on Dec 20, 2014

@author: rmn
'''
import csv
from numpy import log
from numpy import exp
from random import random
import sys
import re
sys.setrecursionlimit(10000)


def read_input(file_path):
    grammar = {}
    with open(file_path, 'Ub') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            if row[2] not in grammar:
                grammar[row[2]] = {row[3]: float(row[0])}
            else:
                grammar[row[2]][row[3]] = float(row[0])
    return grammar


def mySample(Expand):
    usamp = random()  # some number between 0 and 1
    cumul = 0  # cumulative distribution
    for p in Expand:  # `.' with p=0.5, `!' with p=0.25, and `?' with p=0.25
        cumul += Expand[p]  # for `.', this will be .5, for `!' .75, for `?' 1
        if usamp < cumul:  # if 0 <= usamp <= .5 return `.', and so on
            return p


def generate_parsetree(root, grammar):
    sample = mySample(grammar[root])
    if sample is None:
        print "sample is none"
        print root, sample
    samp = sample.split(' ')
    if len(samp) == 1:  # terminal
        return ('[.' + root + ' ' + sample + ' ]', log(grammar[root][sample]))
    else:
        sub_tree0 = generate_parsetree(samp[0], grammar)
        sub_tree1 = generate_parsetree(samp[1], grammar)
        out = '[.' + root + ' ' +\
            sub_tree0[0] +\
            ' ' + sub_tree1[0] +\
            ' ]'
        prob = sub_tree0[1] +\
            sub_tree1[1]
        return (out, prob)

if __name__ == '__main__':
    grammar = read_input('./grammar.csv')
#     print grammar
    tree = generate_parsetree('S', grammar)
    print '\\Tree ' + tree[0] + ' \\\\'
    print 'Negative log probability of the tree: %.4f \\\\' % tree[1]
    print 'Probability of the tree: %.20f \\\\' % exp(tree[1])
