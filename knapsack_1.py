#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys;
import time;
import functools;

class Instance:
    def __init__(self):
        self.Id = 0;
        self.N = 0;
        self.M = 0;
        self.Items = [];

    def solve(self, method, cycles):
        if 'bruteforce' == method:
            return self.__solve_bruteforce(cycles);
        elif 'heuristic' == method:
            return self.__solve_heuristic(cycles);
        else:
            raise Exception("Unknown solving method: {}".format(method));

    def __solve_bruteforce(self, cycles):
        start = time.clock();

        for cycle in range(0, cycles):
            best_cost = 0;

            for combination in range(0, 2 ** self.N):
                cost = 0;
                weight = 0;
                bitmask = 1;

                for i in range(0, self.N):
                    if 0 != (combination & bitmask):
                        cost += self.Items[i].Cost;
                        weight += self.Items[i].Weight;

                    bitmask <<= 1;

                if weight <= self.M and cost > best_cost:
                    best_cost = cost;

        end = time.clock();
        running_time = (end - start) / cycles;
        return (best_cost, running_time);

    def __solve_heuristic(self, cycles):
        start = time.clock();

        for cycle in range(0, cycles):
            cost = 0;
            weight = 0;

            sorted_items = sorted(self.Items, key = functools.cmp_to_key(lambda item1, item2: item1.Cost / item1.Weight >= item2.Cost / item2.Weight));

            for i in sorted_items:
                if weight + i.Weight <= self.M:
                    cost += i.Cost
                    weight += i.Weight

        end = time.clock();
        running_time = (end - start) / cycles;
        return (cost, running_time);

class Item:
    def __init__(self):
        self.Weight = 0;
        self.Cost = 0;

def main(argc, argv):
    if 2 > argc:
        print("Usage: {} <instances> [<cycles>]\n".format(argv[0]));
        return 1;

    cycles = 1
    if 3 == argc:
        cycles = int(argv[2])

    instances = [];
    with open(argv[1], mode = "r") as f:
        for l in f:
            line_splitted = l.split(' ');
            new_instance = Instance();
            new_instance.Id = int(line_splitted[0]);
            new_instance.N = int(line_splitted[1]);
            new_instance.M = int(line_splitted[2]);

            for i in range(3, len(line_splitted), 2):
                new_item = Item();
                new_item.Weight = int(line_splitted[i + 0]);
                new_item.Cost = int(line_splitted[i + 1]);
                new_instance.Items.append(new_item);

            instances.append(new_instance);

        f.close();

    exact_result = {}

    for method in ["bruteforce", "heuristic"]:
        total_runtime = 0
        average_runtime = 0

        total_relative_error = 0
        maximum_relative_error = 0
        average_relative_error = 0

        for instance in instances:
            print("Solving instance {} using {}... ".format(instance.Id, method), end='');
            result = instance.solve(method, 4096 if 'heuristic' == method else cycles);
            print("Result: {:8}, Time: {:24.16f}.".format(result[0], result[1]));
            total_runtime += result[1]

            if 'bruteforce' == method:
                exact_result[instance] = result;
            elif 'heuristic' == method:
                relative_error = abs(result[0] - exact_result[instance][0]) / exact_result[instance][0];
                total_relative_error += relative_error;
                maximum_relative_error = max(maximum_relative_error, relative_error);

        average_runtime = total_runtime / len(instances);
        print("Total runtime: {:24.16f}, average runtime: {:24.16f}.".format(total_runtime, average_runtime));

        if 'heuristic' == method:
            average_relative_error = total_relative_error / len(instances);
            print("Maximum relative error: {:.8f}, average relative error: {:.8f}.".format(maximum_relative_error, average_relative_error));

    return 0;

if "__main__" == __name__:
    sys.exit(main(len(sys.argv), sys.argv));
