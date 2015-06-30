
import sys, time, functools, math, random

class Instance:
    
    def __init__(self):
        self.Id = 0;
        self.N = 0;
        self.M = 0;
        self.Items = [];

    def solve(self, method, cycles, t, alpha):
        
        solver = None
        
        if 'dynamic' == method:
            solver = self.__solve_dynamic;
        elif 'sa' == method:
            solver = lambda: self.__solve_simulated_annealing(t, alpha);

        running_time = 0
        cost = 0
        for cycle in range(0, cycles):
            result = solver();
            cost = result[0]
            running_time += result[1]

        return (cost, running_time / cycles)

    def __solve_dynamic(self):
        start = time.clock();

        table = [[None for j in range(self.N + 1)] for i in range(self.M + 1)];
        table[0][0] = 0; # (weight, items) -> cost.
        node_queue = [(0, 0)];

        while 0 != len(node_queue):
            node = node_queue.pop(0)
            node_value = table[node[0]][node[1]];


            if (node[1] <= self.N - 1):
                next_node = (node[0], node[1] + 1);
                old_value = table[next_node[0]][next_node[1]]
                if None == old_value or node_value > old_value:
                    table[next_node[0]][next_node[1]] = node_value;
                    node_queue.append(next_node);

                if node[0] + self.Items[node[1]].Weight <= self.M:
                    next_node = (node[0] + self.Items[node[1]].Weight, node[1] + 1);

                    old_value = table[next_node[0]][next_node[1]]
                    new_value = node_value + self.Items[node[1]].Cost;

                    if None == old_value or new_value > old_value:
                        table[next_node[0]][next_node[1]] = new_value;
                        node_queue.append(next_node);

        cost = 0
        for i in range(self.M, -1, -1):
            new_cost = table[i][self.N];
            if None == new_cost:
                continue;

            cost = max(cost, new_cost);


        end = time.clock();
        running_time = end - start;
        return (cost, running_time);

    def __solve_simulated_annealing(self, t, alpha):
        def evaluate_solution(solution):
            cost = weight = 0
            bitmask = 1
            for i in range(self.N):
                if 0 != (solution & bitmask):
                    cost += self.Items[i].Cost
                    weight += self.Items[i].Weight

                bitmask <<= 1

            return (weight <= self.M, cost)

        start = time.clock();

        total_cost = functools.reduce(lambda i1, i2: i1 + i2.Cost, self.Items, 0)

        current_temperature = t

        while True:
            current_state = random.getrandbits(self.N)
            current_cost = evaluate_solution(current_state)
            if current_cost[0]:
                current_cost = current_cost[1]
                break

        best_state = current_state
        best_cost = current_cost

        while True:

            for i in range(self.N):
                new_state = current_state ^ (1 << random.randrange(self.N))
                new_cost = evaluate_solution(new_state)

                acceptable = new_cost[0]
                if acceptable:
                    new_cost = new_cost[1]
                else:
                    new_cost = new_cost[1] - total_cost

                delta_cost = new_cost - current_cost

                e = math.exp(-abs(delta_cost) / current_temperature)
                r = random.random()

                if (delta_cost > 0) or (r < e):
                    current_state = new_state
                    current_cost = new_cost

                if acceptable and best_cost < current_cost:
                    best_cost = current_cost
                    best_state = current_state

            if current_temperature < abs(math.log10(alpha)) / 10:
                break

            current_temperature *= alpha

        end = time.clock();
        running_time = end - start;
        return (best_cost, running_time);

class Item:
    def __init__(self):
        self.Weight = 0;
        self.Cost = 0;

def main(argc, argv):
    random.seed();

    filename = "../inst/knap_40.inst.dat"

    cycles = 1

    t = 11

    alpha = 0.9

    method = "sa"

    instances = [];
    with open(filename, mode = "r") as f:
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

    total_runtime = 0
    average_runtime = 0

    total_relative_error = 0
    maximum_relative_error = 0
    average_relative_error = 0

    for instance in instances:
        print("Solving instance {} using {}... ".format(instance.Id, method));
        result = instance.solve(method, cycles, t, alpha);
        print("Result: {}, Time: {}.".format(result[0], result[1]));
        total_runtime += result[1]

        if 'sa' == method:
            exact_result = instance.solve('dynamic', 1, t, alpha);
            relative_error = abs(result[0] - exact_result[0]) / float(exact_result[0]);
            total_relative_error += relative_error;
            maximum_relative_error = max(maximum_relative_error, relative_error);

    average_runtime = total_runtime / len(instances);
    print("Total runtime: {}, average runtime: {}.".format(total_runtime, average_runtime));

    if 'sa' == method:
        average_relative_error = total_relative_error / len(instances);
        print("Maximum relative error: {}, average relative error: {}.".format(maximum_relative_error, average_relative_error));

    return 0;

if "__main__" == __name__:
    sys.exit(main(len(sys.argv), sys.argv));
