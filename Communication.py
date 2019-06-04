import socketio
import requests
import random
from Othello import *
from aiohttp import web
from minimax_a_b import Minimax
import copy

class Communication:
    def __init__(self):
        print("prueba")
        self.sio = socketio.Client()
        self.game = Othello()
        self.id = 142857

    def connect(self, ip):
        @self.sio.on('connect')

        def on_connect():
            self.sio.emit('signin', {
                'user_name': 'jenbarillas',
                'tournament_id': self.id,
                'user_role': 'player'
                })

        @self.sio.on('ok_signin')
        def on_signin():
            print('Success!')

        @self.sio.on('ready')
        def on_ready(data):
            gameID = data.get('game_id')
            playerTurnID = data.get('player_turn_id')
            board = data.get('board')

            print('Recived board: ')
            self.game.setBoard(board)
            # mini_max!
            mini_max = Minimax(player=(playerTurnID), enemy=((playerTurnID%2) + 1))
            # copy game
            newGame = copy.deepcopy(self.game)
            newGame.moves = []
            # Predicts future moves and gets the first one
            new = mini_max.minimax_a_b_p(newGame, maximizingPlayer=True, depth=50)
            # if it returns none, probably means there is no other position
            if new == None:
                print('NO MORE MOVES')
                positionAttack = 0
                newGame.printBoard()
            elif new.moves == []:
                print('NO MORE MOVES')
                positionAttack = 0
            else:
                x,y = new.moves[0]
                print('TESTING {} {}'.format(x,y))

                # if self.game.checkIfAvailable(x=(x+1), y=(y+1), player=1):
                #     positionAttack = ((y+1)-1)*8 + (x+1)
                # else:
                #     print('[-] THAT WAS NOT SUPPOSED TO HAPPEN!')
                #     newGame.printBoard()
                #     print('TESTING {} {}'.format(x,y))

                positionAttack = y*8+x

            print(positionAttack)
            # Mostramos el board
            # print('Attack on : ({},{})'.format(x,y) )
            self.game.printBoard()

            self.sio.emit('play', {
                'tournament_id': self.id,
                'player_turn_id': playerTurnID,
                'game_id': gameID,
                'movement': positionAttack
                })

        @self.sio.on('finish')
        def on_finish(data):
            gameID = data.get('game_id')
            playerTurnID = data.get('player_turn_id')
            winnerTurnID = data.get('winner_turn_id')
            board = data.get('board')

            print('{},{},{},{}'.format(gameID, playerTurnID, winnerTurnID, board))
            print('GAME FINISH {}'.format(winnerTurnID))
            self.game.setBoard(board)
            self.game.printBoard()

            self.game.reset()

            self.sio.emit('player_ready', {
                'tournament_id': self.id,
                'player_turn_id': playerTurnID,
                'game_id': gameID
                })

        self.sio.connect(ip)
        self.sio.wait()


othelo_game = Communication()
othelo_game.connect('http://192.168.1.148:4000/')#,'jenbarillas',142857)
# othelo_game.connect('http://localhost:4000/','jenbarillas',12)
