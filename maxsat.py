#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import math
import random
import functools

class Formula:
    def __init__(self, f):
        self.variables_count = 0
        self.weights = []
        self.formula = []

        comment = False
        clause_index = 0

        def read_int(f, t=None):
            number = None

            while True:
                if None != t:
                    c = t
                    t = None
                else:
                    c = f.read(1)

                if 0 == len(c):
                    break

                c = c[0]

                if str.isdigit(c):
                    if None == number:
                        number = ''

                    number += c
                elif '-' == c and None == number:
                    number = '-'
                else:
                    break

            return int(number) if None != number else None

        while True:
            c = f.read(1)

            if 0 == len(c):
                break

            c = c[0]

            if 'c' == c:
                comment = True

            if 'p' == c:
                if comment:
                    continue

                f.read(5)

                self.variables_count = read_int(f)
                self.weights = [ 0 ] * self.variables_count
                clauses_count = read_int(f)
                self.formula = [ [] for i in range(clauses_count) ]

            elif 'w' == c:
                if comment:
                    continue

                f.read(1)

                for i in range(self.variables_count):
                    self.weights[i] = read_int(f)

            elif '\n' == c or '\r' == c:
                comment = False

            else:
                if comment:
                    continue

                while True:
                    t = read_int(f, c)
                    c = None

                    if 0 == t:
                        clause_index += 1
                        break
                    else:
                        self.formula[clause_index].append(t)

        del self.formula[clause_index:]

    def compute(self, x):
        clauses = map(lambda clause: functools.reduce(lambda t, i: (x[i - 1] if i > 0 else not(x[-i - 1])) or t, clause, False), self.formula)
        formula_result = functools.reduce(lambda a, b: a and b, clauses)

        weight = 0
        for i in range(len(x)):
            if x[i]:
                weight += self.weights[i]

        return (formula_result, weight)

def main(argc, argv):
    if argc < 2:
        print("usage: {} <formula.cnf> [<inner-loop>] [<t0>] [<alpha>]".format(argv[0]))
        return 1

    with open(argv[1], 'r') as f:
        formula = Formula(f)

    inner_loop = len(formula.formula) # clauses count.
    if argc >= 3:
        inner_loop = int(argv[2])

    t0 = 10 ** math.ceil(math.log10(len(formula.formula)))
    if argc >= 4:
        t0 = float(argv[3])

    alpha = 1.0
    # !!! alpha = 0.99
    if argc >= 5:
        alpha = float(argv[4])

    random.seed()

    print("inner-loop = {}, t0 = {}, alpha = {}".format(inner_loop, t0, alpha))

    start_time = time.clock()

    total_weight = 0.5 * sum(formula.weights)
    # print("total_weight = {}".format(total_weight))

    current_state = [ random.random() >= 0.5 for i in range(formula.variables_count)]

    # current_state = [ False ] * formula.variables_count

    current_cost = formula.compute(current_state)
    current_cost_real = (1.0 if current_cost[0] else -1.0) * total_weight + current_cost[1]

    # print("current_cost_real = {}".format(current_cost_real))

    current_temperature = t0

    best_state = current_state
    best_cost = current_cost
    best_cost_real = current_cost_real

    try:
        while True:
            print("t = {:.4f} best = {:.8f} current = {:.8f}".format(current_temperature, best_cost_real, current_cost_real))

            for i in range(inner_loop):
                # print("t = {:.4f} best = {:.8f}".format(current_temperature, best_cost_real))

                variable_to_change = random.randrange(0, formula.variables_count)
                new_state = list(current_state)
                new_state[variable_to_change] ^= True
                new_cost = formula.compute(new_state)
                new_cost_real = (1.0 if new_cost[0] else -1.0) * total_weight + new_cost[1]

                delta_cost = new_cost_real - current_cost_real

                e = math.exp(-abs(delta_cost) / current_temperature)
                r = random.random()

                if (delta_cost > 0) or (r < e):
                    current_state = new_state
                    current_cost = new_cost
                    current_cost_real = new_cost_real

                if best_cost_real < current_cost_real:
                    best_state = current_state
                    best_cost = current_cost
                    best_cost_real = current_cost_real

            current_temperature -= alpha
            # !!! current_temperature *= alpha

            if current_temperature <= abs(math.log10(alpha)) / 10:
                break
    except KeyboardInterrupt:
        print("Interrupted.")

    end_time = time.clock()

    print("Runtime: {:.8f}\nResult: sat = {}, weight = {}".format(end_time - start_time, best_cost[0], best_cost[1]))
    return 0

if "__main__" == __name__:
    sys.exit(main(len(sys.argv), sys.argv))
