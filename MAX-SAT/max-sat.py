# -*- coding: utf-8 -*-
import sys, time, math, random

emptyValue = None
state = [True, True, True, True]

def evaluateClause(clause, varsSet):
    result = False
    
    for i, var in enumerate(clause):
        if var == emptyValue:
            continue
        varValue = varsSet[i] if var else not(varsSet[i])
        result = result or varValue # time of check could be reduces once met True
    return result # reduce(lambda a, b: a or b, clause)
    
def evaluateFormula(formula, varsSet):
    result = True
    
    for clause in formula:
        result = result and evaluateClause(clause, varsSet) #could be reduced once False met

    return result
    #return reduce(lambda a, b: evaluateClause(a, varsSet) and evaluateClause(b, varsSet), formula)

def calculateTotalWeight(state, weights):
    weight = 0
    for i, var in enumerate(state):
        if var:
            weight += weights[i]
    return weight

def calculateCost(result, weight, weights):
    weightMean = 0.5 * sum(weights)
    return (1.0 if result else -1.0) * weightMean

def readFormula(f):
    
    def piecesToVars(pieces, numOfVars):
        
        vars = [emptyValue for x in range(numOfVars)]
        for var in pieces:
            varNumber = int(var)
            varNumberAbs = abs(varNumber) - 1
            #print varNumberAbs
            vars[varNumberAbs] = True if varNumber > 0 else False
        return vars
    
    clauseNumber = 0
    
    for l in f:
        l = l.strip()
        pieces = l.split(" ")
        startPiece = pieces[0]

        if startPiece == "c":
            continue

        if startPiece == "w":
            weights = map(int, pieces[1:])
            continue
        
        if startPiece == "p":
            if pieces[1] == "cnf":
                numOfVars = int(pieces[2])
                numOfClauses = int(pieces[3])
                clauses = [[emptyValue for x in range(numOfVars)] for x in range(numOfClauses)]
                continue

        varsPieces = pieces[:-1]

        varsSet = piecesToVars(varsPieces, numOfVars)
        clauses[clauseNumber] = varsSet
        clauseNumber += 1
    #print varsSet#, evaluateClause(varsSet, state)
    return clauses, weights

def frozen(value):
    return value/10#abs(math.log10(alpha)) / 10

def random_neighbour(stateToChange):
    tempState = list(stateToChange)
    elemNumber = random.randrange(0, len(stateToChange))
    tempState[elemNumber] = not(tempState[elemNumber])
    return tempState

def accept(delta, temperature):
    expo = math.exp(-abs(delta) / temperature)
    return random.random() < expo

def cool(temperature, alpha):
    return temperature * alpha


def main(argc, argv):
    if argc > 1:
        fileName = argv[1]
    else:
        fileName = emptyValue

    f = open(fileName or "data/3sat-formula.txt", "r")
    (clauses, weights) = readFormula(f)
    #print evaluateFormula(clauses, state), calculateTotalWeight(state, weights)

#print clauses, weights, fileName

    numOfClauses = len(clauses)
    numOfVars = len(clauses[0])
#print numOfVars

#Defaults:

    innerLoop = numOfClauses
    t0 = 10 ** math.ceil(math.log10(numOfClauses))
    alpha = 0.995

    if argc > 2:
        innerLoop = int(argv[2])

    if argc > 3:
        t0 = float(argv[3])

    if argc > 4:
        alpha = float(argv[4])

    print("inner loop = {}, t0 = {}, alpha = {}".format(innerLoop, t0, alpha))


    random.seed()
    initialState = [ random.random() >= 0.5 for i in range(numOfVars)]

    startTime = time.clock()

    t = t0
    currentState = initialState

    currentResult = evaluateFormula(clauses, currentState)
    currentCost = calculateTotalWeight(currentState, weights)
    currentCostBig = calculateCost(currentResult, currentCost, weights)

    bestState = currentState
    bestCost = currentCost
    bestCostBig = currentCostBig

    while ( t > frozen(t0) ):
        for i in range(innerLoop):
            newState = random_neighbour(currentState)
            
            newResult = evaluateFormula(clauses, newState)
            newCost = calculateTotalWeight(newState, weights)
            newCostBig = calculateCost(newResult, newCost, weights)
            
            currentResult = evaluateFormula(clauses, currentState)
            currentCost = calculateTotalWeight(currentState, weights)
            currentCostBig = calculateCost(currentResult, currentCost, weights)
            
            deltaCost = newCostBig - currentCostBig
            
            if (deltaCost > 0) or (accept(deltaCost, t)):
                currentState = newState
                currentCost = newCost
                currentCostBig = newCostBig

            if bestCostBig < currentCostBig:
                bestState = currentState
                bestCost = currentCost
                bestCostBig = currentCostBig
        
        

        t = cool(t, alpha)
#print t
    endTime = time.clock()

    print("Runtime: {:.8f}\nResult: sat = {}, weight = {}".format(endTime - startTime, evaluateFormula(clauses, bestState), bestCost))
    print (endTime - startTime), evaluateFormula(clauses, bestState), bestCost, bestState
    return 0





if "__main__" == __name__:
    sys.exit(main(len(sys.argv), sys.argv))