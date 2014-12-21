'''
Created on Dec 20, 2014

@author: rmn
'''

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
from tabulate import tabulate
sys.setrecursionlimit(10000)


def read_input(file_path):
    terminals = {}
    non_terminals = {}
    with open(file_path, 'Ub') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            if len(row[3].split()) == 1:
                if row[3] not in terminals:
                    terminals[row[3]] = {row[2]: log(float(row[0]))}
                else:
                    terminals[row[3]][row[2]] = log(float(row[0]))
            else:
                if row[3] not in non_terminals:
                    non_terminals[row[3]] = {row[2]: log(float(row[0]))}
                else:
                    non_terminals[row[3]][row[2]] = log(float(row[0]))
    return (terminals, non_terminals)


def cyk(sentence, terminals, non_terminals):
    tokens = re.findall(r"[\w']+|[.,!?;]", sentence)
    table = [[dict() for _ in range(len(tokens))] for _ in range(len(tokens))]
    pointers = [['-' for _ in range(len(tokens))]
                for _ in range(len(tokens))]
    #init (width = 0)
    for i in range(len(tokens)):
        table[i][i] = terminals[tokens[i]]
    # Continue
    for width in range(1, len(tokens)):
        for i in range(0, len(tokens)):
            for mid in range(i, min((i + width, len(tokens) - 1))):
                #                 print "i:%d mid:%d width:%d" % (i, mid, width)
                #                 print min((i + width, len(tokens) - 1))
                if mid < len(tokens) - 1 and i + width < len(tokens):
                    if table[i][mid] != {} and table[mid + 1][i + width] != {}:
                        candidates0 = table[i][mid]
                        candidates1 = table[mid + 1][i + width]
                        maxx = float('-inf')
                        best = ''
                        correct = {}
                        pointer = {}
                        for k in candidates0:
                            for k1 in candidates1:
                                if k + ' ' + k1 in non_terminals:
                                    key = k + ' ' + k1
                                    for npkey in non_terminals[key].keys():
                                        correct[npkey] =\
                                            non_terminals[key][npkey] +\
                                            candidates0[k] + candidates1[k1]
                                        pointer[npkey] = (
                                            (i, mid), (mid + 1, i + width))
#                                     if candidates0[k] + candidates1[k1] > maxx:
#                                         best = k + ' ' + k1
#                                         pointer = (
#                                             (i, mid), (mid + 1, i + width))
#                                         maxx = candidates0[k] + candidates1[k1]
#                         if best != '':
                            if correct != {}:
                                table[i][
                                    i + width] = correct
                                pointers[i][i + width] = pointer
    print sentence
    print tabulate(table)
    print tabulate(pointers)

    def reconstruct(i, j):
        if i == j:
            return '[.' + max(table[i][i], key=table[i][i].get) +\
                ' ' + tokens[i] + ' ]'
        else:
            if type(pointers[i][j]) != str and type(pointers[i][j]) != str:
                key = max(table[i][j], key=table[i][i].get)
                return '[.' + key + ' ' + reconstruct(pointers[i][j][key][0][0], pointers[i][j][key][0][1]) +\
                    ' ' + \
                    reconstruct(
                        pointers[i][j][key][1][0], pointers[i][j][key][1][1]) + ' ]'

    if not (table[0][len(tokens) - 1] != {}):
        print "No parse tree is found for the sentence."
    else:
        print '\\Tree ' + reconstruct(0, len(tokens) - 1)
        print "Negative log probability: %f.4" % table[0][len(tokens) - 1].values()[0]


if __name__ == '__main__':
    grammar = read_input('./grammar.csv')
#     grammar = read_input('./modified.csv')
#     print grammar
    cyk('the pickle bid the sandwich',
        grammar[0], grammar[1])
