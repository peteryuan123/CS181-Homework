# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game

expr = logic.Expr
ps_expr = logic.PropSymbolExpr

pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def z(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    A = expr("A")
    B = expr("B")
    C = expr("C")

    s1 = A | B
    s2 = (~A) % (~B | C)
    s3 = logic.disjoin([~A, ~B, C])

    return logic.conjoin([s1, s2, s3])    

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = expr("A")
    B = expr("B")
    C = expr("C")
    D = expr("D")

    s1 = C % (B | D)
    s2 = A >> (~B & ~D)
    s3 = ~(B & ~C) >> A
    s4 = ~D >> C

    return logic.conjoin([s1, s2, s3, s4])

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    Alive = []
    Born = []
    Killed = []

    Alive.append(ps_expr("WumpusAlive",0))
    Alive.append(ps_expr("WumpusAlive",1))
    Born.append(ps_expr("WumpusBorn",0))
    Killed.append(ps_expr("WumpusKilled",0))

    s1 = Alive[1] % (( Alive[0] & ~Killed[0]) | (~Alive[0] & Born[0]))
    s2 = ~(Alive[0] & Born[0])
    s3 = Born[0]

    return logic.conjoin([s1, s2, s3])

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    cnf = logic.to_cnf(sentence)
    return logic.pycoSAT(cnf)

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)
    


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    item_list = []
    for i in range(len(literals)):
        cur = literals[i]
        for item in literals[i+1:]:
            new = ~cur | ~item
            item_list.append(new)

    return logic.conjoin(item_list)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    item_list = []
    for i in range(len(literals)):
        cur = literals[i]
        for item in literals[i+1:]:
            new = ~cur | ~item
            item_list.append(new)

    at_most_one = logic.conjoin(item_list)
    
    none_is_true = logic.disjoin(literals)
    
    s = at_most_one & none_is_true

    return s 


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"

    act_list = []    
    for item in model.keys():
        if (model[item]):
            pars = logic.PropSymbolExpr.parseExpr(item)
            if(pars[0] in actions):
                act_list.append(pars)

    act_list = sorted(act_list, key=lambda act_list : int(act_list[1]))

    final = []
    for item in act_list:
        final.append(item[0])
    return final



def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    P = logic.PropSymbolExpr("P",x,y,t)
    walls = walls_grid.asList()
    actions = []
    
    if((x-1,y) not in walls):
        actions.append(logic.PropSymbolExpr("P",x-1,y,t-1) & logic.PropSymbolExpr("East",t-1))
    if((x,y-1) not in walls):
        actions.append(logic.PropSymbolExpr("P",x,y-1,t-1) & logic.PropSymbolExpr("North",t-1))
    if((x,y+1) not in walls):
        actions.append(logic.PropSymbolExpr("P",x,y+1,t-1) & logic.PropSymbolExpr("South",t-1))
    if((x+1,y) not in walls):
        actions.append(logic.PropSymbolExpr("P",x+1,y,t-1) & logic.PropSymbolExpr("West",t-1))

    act = atLeastOne(actions)
    P = P % act

    return P


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    valid_action = ["North","South","West","East"]
    wall_list = walls.asList()
    start_p = problem.getStartState()
    final_p = problem.getGoalState()

    initial_literal = []

    for i in range(1,width+1):
        for j in range(1, height+1):
            if((i,j) not in wall_list):
                if((i,j) == start_p):
                    initial_literal.append(logic.PropSymbolExpr("P",i,j,0))
                else:
                    initial_literal.append(~logic.PropSymbolExpr("P",i,j,0))

    initial_state = logic.conjoin(initial_literal)
    history_actions = []
    history_transitions = []

    for t in range(50):
        goal_state = logic.PropSymbolExpr("P",final_p[0],final_p[1],t)

        if (t == 0):
            sentence = goal_state & initial_state 
        else:
            transition_literals_of_t = []

            for i in range(1,width+1):
                for j in range(1,height+1):
                    if((i,j) not in wall_list):
                        transition_literals_of_t.append(pacmanSuccessorStateAxioms(i, j, t, walls))


            transition_logic = logic.conjoin(transition_literals_of_t)

            action_list = []
            for action in valid_action:
                action_list.append(logic.PropSymbolExpr(action,t-1))
            action_logic = exactlyOne(action_list)

            history_transitions.append(transition_logic)
            history_actions.append(action_logic)

            history_action_conj = logic.conjoin(history_actions)
            history_transition_conj = logic.conjoin(history_transitions)
            sentence = logic.conjoin(initial_state, history_transition_conj, history_action_conj, goal_state)
          
        model = findModel(sentence)
        if (model != False):
            return extractActionSequence(model, valid_action)

    return None


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    
    valid_action = ["North","South","West","East"]
    wall_list = walls.asList()

    start_p = problem.getStartState()[0]
    food_list = problem.getStartState()[1].asList()

    initial_literal = []
    for i in range(1,width+1):
        for j in range(1, height+1):
            if((i,j) not in wall_list):
                if((i,j) == start_p):
                    initial_literal.append(logic.PropSymbolExpr("P",i,j,0))
                else:
                    initial_literal.append(~logic.PropSymbolExpr("P",i,j,0))

    initial_state = logic.conjoin(initial_literal)
    history_actions = []
    history_transitions = []

    for t in range(50):
        
        goal_list = []
        for food in food_list:
            temp = []
            for h in range(t+1):
                temp.append(logic.PropSymbolExpr("P",food[0],food[1],h))
                
            goal_list.append(logic.disjoin(temp))
            
        goal_state = logic.conjoin(goal_list)
        
        if (t == 0):
            sentence = goal_state & initial_state 
        else:
            transition_literals_of_t = []

            for i in range(1,width+1):
                for j in range(1,height+1):
                    if((i,j) not in wall_list):
                        transition_literals_of_t.append(pacmanSuccessorStateAxioms(i, j, t, walls))


            transition_logic = logic.conjoin(transition_literals_of_t)

            action_list = []
            for action in valid_action:
                action_list.append(logic.PropSymbolExpr(action,t-1))
            action_logic = exactlyOne(action_list)

            history_transitions.append(transition_logic)
            history_actions.append(action_logic)

            history_action_conj = logic.conjoin(history_actions)
            history_transition_conj = logic.conjoin(history_transitions)
            sentence = logic.conjoin(initial_state, history_transition_conj, history_action_conj, goal_state)
         
        model = findModel(sentence)
        if (model != False):
            return extractActionSequence(model, valid_action)

    return None    


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    