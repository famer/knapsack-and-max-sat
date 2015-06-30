
import sys, time, functools, math

class Instance:
    def __init__(self):
        self.Id = 0;
        self.N = 0;
        self.M = 0;
        self.Items = [];
    
    def solve(self, method, cycles, eps):
        solver = None
        
        if 'bruteforce' == method:
            solver = self.__solve_bruteforce;
        elif 'dynamic' == method:
            solver = self.__solve_dynamic;
        elif 'fptas' == method:
            solver = lambda: self.__solve_fptas(eps);
        
        running_time = 0
        cost = 0
        for cycle in range(0, cycles):
            result = solver();
            cost = result[0]
            running_time += result[1]
        
        return (cost, running_time / cycles)
    
    def __solve_bruteforce(self):
        start = time.clock();
        
        best_cost = 0;
        original_upper_bound = functools.reduce(lambda i1, i2: i1 + i2.Cost, self.Items, 0);
        
        for combination in range(0, 2 ** self.N):
            cost = 0;
            upper_bound = original_upper_bound
            weight = 0;
            bitmask = 1;
            
            for i in range(0, self.N):
                if 0 != (combination & bitmask):
                    cost += self.Items[i].Cost;
                    weight += self.Items[i].Weight;
                else:
                    upper_bound -= self.Items[i].Cost;
                    
                    if upper_bound <= best_cost:
                        break;
        
                            bitmask <<= 1;
                                
                                if i == self.N - 1 and weight <= self.M and cost > best_cost:
                                    best_cost = cost;
                                
                                end = time.clock();
                                    running_time = end - start;
                                        return (best_cost, running_time);

def __solve_dynamic(self):
    start = time.clock();
        
    table = [[None for j in range(self.N + 1)] for i in range(self.M + 1)];
    table[0][0] = 0; #(weight, items) -> cost.
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

def __solve_fptas(self, eps):
    start = time.clock();
    
    max_cost = functools.reduce(lambda i1, i2: max(i1, i2.Cost), self.Items, 0);
    k = eps * max_cost / self.N;
    categorized_costs = [math.floor(i.Cost / k) for i in self.Items];
    
    height = sum(categorized_costs);
    table = [[None for j in range(self.N + 1)] for i in range(height + 1)];
    table[0][0] = (0, []); # (cost, items) -> (weight, taken_items).
    node_queue = [(0, 0)];
    
    while 0 != len(node_queue):
        node = node_queue.pop(0)
        node_value = table[node[0]][node[1]];
        
        if (node[1] <= self.N - 1):
            next_node = (node[0], node[1] + 1);
            old_value = table[next_node[0]][next_node[1]]
            if None == old_value or node_value[0] < old_value[0]:
                table[next_node[0]][next_node[1]] = node_value;
                node_queue.append(next_node);
        
            if node[0] + categorized_costs[node[1]] <= height:
                next_node = (node[0] + categorized_costs[node[1]], node[1] + 1);
                
                old_value = table[next_node[0]][next_node[1]]
                new_value = node_value[0] + self.Items[node[1]].Weight;
                
                if None == old_value or new_value < old_value[0]:
                    table[next_node[0]][next_node[1]] = (new_value, node_value[1] + [node[1]]);
                    node_queue.append(next_node);

    cost = 0
    for i in range(height, -1, -1):
        new_weight = table[i][self.N];
        if None == new_weight:
            continue;
        
        if new_weight[0] <= self.M:
            for item in new_weight[1]:
                cost += self.Items[item].Cost;
            break;

    end = time.clock();
    running_time = end - start;
    return (cost, running_time);

class Item:
    def __init__(self):
        self.Weight = 0;
        self.Cost = 0;

def main(argc, argv):
    
    cycles = 1
    if 4 == argc:
        cycles = int(argv[3])
    
    eps = 0.1
    if 5 == argc:
        eps = float(argv[4])

    method = argv[1]

    instances = [];
    with open(argv[2], mode = "r") as f:
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
        print("Solving instance {} using {}... ".format(instance.Id, method), end='');
        result = instance.solve(method, cycles, eps);
        print("Result: {:8}, Time: {:24.16f}.".format(result[0], result[1]));
        total_runtime += result[1]
        
        if 'fptas' == method:
            exact_result = instance.solve('dynamic', 1, 0);
            relative_error = abs(result[0] - exact_result[0]) / exact_result[0];
            total_relative_error += relative_error;
            maximum_relative_error = max(maximum_relative_error, relative_error);

    average_runtime = total_runtime / len(instances);
    print("Total runtime: {:24.16f}, avg runtime: {:24.16f}.".format(total_runtime, average_runtime));
    
    if 'fptas' == method:
        average_relative_error = total_relative_error / len(instances);
        print("Maximum relative error: {:.8f}, average relative error: {:.8f}.".format(maximum_relative_error, average_relative_error));

    return 0;

if "__main__" == __name__:
    sys.exit(main(len(sys.argv), sys.argv));




