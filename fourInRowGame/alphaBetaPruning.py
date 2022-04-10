import Game

# depth -> wll search the best move by the val of the state, depth mean how many moves foreword wll look
# more depth mean better execution but slower
DEPTH = 2


# made the next move:
# get the state ( board )  and return the new board after the move
def go(state):
    # if it humen turn choose the board with the minimum value
    if Game.isHumTurn(state):
        obj = abmin(state, DEPTH, Game.LOSS - 1, Game.VICTORY + 1)[1]
        return obj

    else:  # it computer turn, choose the maximunm value
        print("Turn of agent")
        obj = abmax(state, DEPTH, Game.LOSS - 1, Game.VICTORY + 1)[1]
        return obj


# s = the state (max's turn)
# d = max. depth of search
# a = alpha parametr for pruning min tree
# b = beta parametr for pruning max tree  
# returns [v, ns]: v = state s's value. ns = the state after recomended move.
#        if s is a terminal state ns=0.

def abmax(gm, d, a, b):
    # if depth is 0 we finished are calculation so we retuen the current value 
    if d == 0 or Game.isFinished(gm):
        return [Game.state_value(gm), gm]

    # find the state with the max value
    # intializing the max val for -infinite
    v = float("-inf")
    # ns = list of all the possible next states 
    ns = Game.getNext(gm)
    # initializing the bestowed
    bestMove = 0
    # go over all the possible next stats and find the max value
    for st in ns:
        # tmp = the choose of the min agent for the current check state
        tmp = abmin(st, d - 1, a, b)
        # if tmp value higher then the current max value update the max value and state
        if tmp[0] > v:
            v = tmp[0]
            bestMove = st
        if v >= b:  # the value higher from the b parameter
            # pruning: minimum will choose b anyway so it dosent matter if we will found higher value
            return [v, st]
        # v is are current choose so we update the 'a' parameter for minimum pruning to be hem
        if v > a:
            a = v
    return [v, bestMove]


# s = the state (min's turn)
# d = max. depth of search
# a,b = alpha and beta
# returns [v, ns]: v = state s's value. ns = the state after recommended move.
#        if s is a terminal state ns=0.
def abmin(gm, d, a, b):
    # print("now calculate abmin")
    # print("d=",d)
    # print("a=",a)
    # print("b=",b)

    if d == 0 or Game.isFinished(gm):
        # print("returns ", [game.value(gm), gm])
        return [Game.state_value(gm), 0]
    v = float("inf")

    ns = Game.getNext(gm)
    # print("next moves:", len(ns), " possible moves ")
    bestMove = 0
    for st in ns:
        tmp = abmax(st, d - 1, a, b)
        if tmp[0] < v:
            v = tmp[0]
            bestMove = st
        if v <= a:
            return [v, st]
        if v < b:  # gizum
            b = v
    return [v, bestMove]
