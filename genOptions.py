import multiprocessing

threadCount = 8

def checkForWinner(board):
    for i in range(3):
        if ((board[i * 3] == board[i * 3 + 1] and board[i * 3] == board[i * 3 + 2]) and board[i * 3]):
            return board[i * 3]
    
    for i in range(3):
        if ((board[i] == board[i + 3] and board[i] == board[i + 6]) and board[i]):
            return board[i]
    
    if (((board[0] == board[4] and board[0] == board[8]) or (board[2] == board[4] and board[2] == board[6])) and board[4]):
        return board[4]
    
    return False

def getStrategy(number):
    remainder = None
    strategy = []
    for i in range(9):
        remainder = number % 9
        number = number // 9
        strategy.insert(0, remainder)
    return strategy

def threadProcess(offset):
    print('Thread {} started'.format(offset))
    strategyNumber = 6000000 + offset

    firstPlayerWins = set()
    secondPlayerWins = set()
    draws = set()

    while True:
        while True:
            board = [None, None, None, None, None, None, None, None, None]
            moves = []
            strategy = getStrategy(strategyNumber)  

            if strategyNumber % 1000000 == 0:
                print('Strategy: {} ({:.2%})'.format(strategyNumber, strategyNumber/(387420489 - 6000000)))
            
            if strategyNumber >= 387420489:
                break

            try:
                if len(set(strategy)) < 9:
                    raise Exception
                
                for i in range(len(strategy)):
                    if board[strategy[i]] == None:
                        board[strategy[i]] = i % 2 + 1
                        moves.append(strategy[i])
                    else:
                        raise Exception

                    winner = checkForWinner(board)
                    if winner == 1:
                        firstPlayerWins.add(tuple(moves))
                        break
                    if winner == 2:
                        secondPlayerWins.add(tuple(moves))
                        break

            except Exception:
                strategyNumber += threadCount
                continue

            if winner != 1 and winner != 2:
                draws.add(tuple(moves))
            
            strategyNumber += threadCount
            
            break

        if strategyNumber >= 387420489:
            break
    
    return [firstPlayerWins, secondPlayerWins, draws]

if __name__ == '__main__':
    p = multiprocessing.Pool(processes=threadCount)
    data = p.map(threadProcess, [i for i in range(threadCount)])
    p.close()

    firstPlayerWins = set()
    secondPlayerWins = set()
    draws = set()
    for thread in data:
        firstPlayerWins.update(thread[0])
        secondPlayerWins.update(thread[1])
        draws.update(thread[2])

    print('Finished:')
    print(len(firstPlayerWins), len(draws), len(secondPlayerWins))
    with open('firstPlayerWins.txt', 'w') as file:
        firstPlayerWins = [str(value) for value in firstPlayerWins]
        file.write(str('\n'.join(firstPlayerWins)))

    with open('secondPlayerWins.txt', 'w') as file:
        secondPlayerWins = [str(value) for value in secondPlayerWins]
        file.write(str('\n'.join(secondPlayerWins)))

    with open('draws.txt', 'w') as file:
        draws = [str(value) for value in draws]
        file.write(str('\n'.join(draws)))