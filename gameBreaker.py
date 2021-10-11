firstPlayerWins = []
with open('firstPlayerWins.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        firstPlayerWins.append(eval(line))

secondPlayerWins = []
with open('secondPlayerWins.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        secondPlayerWins.append(eval(line))

draws = []
with open('draws.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        draws.append(eval(line))

moves = []
result = False
player = int(input('Player:\n'))

if player == 1:
    playerWins = firstPlayerWins
    opponentWins = secondPlayerWins
elif player == 2:
    playerWins = secondPlayerWins
    opponentWins = firstPlayerWins

def getValidMoves(moves):
    validMoves = []
    for position in range(9):
        if not position in moves:
            validMoves.append(position)

    return validMoves

def getPossibleOutcomes(moves):
    def filterCallback(outcome):
        return moves == list(outcome[:len(moves)])

    return tuple(filter(filterCallback, playerWins)), tuple(filter(filterCallback, opponentWins)), tuple(filter(filterCallback, draws))

def getNextStatistics(moves, nextMove):
    nextMoves = moves + [nextMove]
    nextPlayerWins, nextOpponentWins, nextDraws = getPossibleOutcomes(nextMoves)
    totalOutcomes = len(nextPlayerWins) + len(nextOpponentWins) + len(nextDraws)

    percentPlayerWins = len(nextPlayerWins) / totalOutcomes
    percentOpponentWins = len(nextOpponentWins) / totalOutcomes
    
    if percentPlayerWins == 0:
        shortestPlayerWin = 'Lose'
    else:
        shortestPlayerWin = (len(sorted(list(nextPlayerWins), key=lambda outcome: len(outcome))[0]) - len(moves) + 1) // 2
    
    if percentOpponentWins == 0:
        shortestOpponentWin = 'Lose'
    else:
        shortestOpponentWin = (len(sorted(list(nextOpponentWins), key=lambda outcome: len(outcome))[0]) - len(moves) + 1) // 2

    return [percentPlayerWins, shortestPlayerWin, percentOpponentWins, shortestOpponentWin, nextMove]

def sortNextStats(nextStatsContainer):
    if nextStatsContainer[1] == 1:
        return 0
    return -nextStatsContainer[0]

print('#-------------------------#')

while True:
    # Pre-loop check to ensure game still running
    if len(getValidMoves(moves)) < 1 or result:
        break

    # Basic move info display
    print(moves)
    if len(moves) % 2 + 1 == player:
        print('\n({}) Your turn:'.format(len(moves)))
    else:
        print('({}) Opponent\'s turn:'.format(len(moves)))

    # Calculate valid moves and outcomes statistics; sort by percent playerWins unless next move ends game
    nextStatsContainer = [getNextStatistics(moves, nextMove) for nextMove in getValidMoves(moves)]
    
    nextStatsContainer.sort(key=sortNextStats)
    
    # Display valid moves and outcomes statistics
    for nextStats in nextStatsContainer:
        print('[{}] {:^8.1%} {:<3} : {:^8.1%} {:<3}'.format(\
            nextStats[4], nextStats[0], 'Win' if nextStats[1] == 1 else nextStats[1], nextStats[2], 'Win' if nextStats[3] == 1 else nextStats[3]))

    # Update moves and possible outcomes
    move = int(input())
    moves.append(move)
    playerWins, opponentWins, draws = getPossibleOutcomes(moves)
    
    if len(opponentWins) == 0 and len(draws) == 0:
        result = 'Win'
    elif len(playerWins) == 0 and len(draws) == 0:
        result = 'Lose'
    elif len(opponentWins) == 0 and len(playerWins) == 0:
        result = 'Draw'

print('\n' + result)