
import sys, time

def main(argv):

	f = open(argv[1], "r")
	cycles = 0
        total_relative_error = 0
        maximum_relative_error = 0
        average_relative_error = 0
	rh = 0
	rb = 0
	for l in f:
		#print l
		sp = l.split(" ")
		cap = int(sp[2])
		#print cap

		items = []
		for i in xrange(int(sp[1])):
			weight = int(sp[3+i*2])
			cost = int(sp[3+i*2+1])
			ratio = round(float(cost)/weight, 2)
			items.append([cost, weight, ratio, i])
		#print(items)
		h = heuristic(items, cap)
		b = brute_force(items, cap)
		#print h[0], b[0]
		#if h[0] == b[0]:
		#	print "Match"
		
		rh += h[2]
		rb += b[2]

                relative_error = abs(h[1] - b[1]) / float(b[1]);
                total_relative_error += relative_error;
                maximum_relative_error = max(maximum_relative_error, relative_error);
		#print relative_error
	

		cycles += 1
		#break

	f.close()
	print cycles
	average_relative_error = total_relative_error / cycles
	average_heuristic_time = rh / cycles
	average_brute_force_time = rb / cycles
	
	print maximum_relative_error, average_relative_error, average_heuristic_time, average_brute_force_time


	return 0

def heuristic(items, cap):
	num = len(items)
	start = time.clock()

	sortedItems = sorted(items, key=lambda x: x[2], reverse=True)
	knap = [0]*num
	sum = 0
	cost = 0
	for x in sortedItems:
		sum += x[1]
		if sum > cap:
			break;
		else:
			knap[x[3]] = 1
			cost += x[0]

	runTime = time.clock() - start
	return (knap, cost, runTime)
	
	

def brute_force(items, cap):
	num = len(items)
	start = time.clock()

	best_cost = 0

	for combination in range(0, 2 ** num):
		cost = 0
		weight = 0
		bitmask = 1
		tknap = [0]*num

		for i in range(0, num):
			if 0 != (combination & bitmask):
				cost += items[i][0]
				weight += items[i][1]
				tknap[items[i][3]] = 1

			bitmask <<= 1

		if weight <= cap and cost > best_cost:
			best_cost = cost
			knap = tknap


	runTime = time.clock() - start
	return (knap, best_cost, runTime)
	

if "__main__" == __name__:
	sys.exit(main(sys.argv))






