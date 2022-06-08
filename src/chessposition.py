#required
import chess
import chess.pgn
import re

class ChessPosition:
    # self.__init__() 
    # is called the first time that a position is found in a database
    # chessgamenode : chess.GameNode object of the python-chess library
    def __init__(self,chessgamenode):
        self.set_basic_attributes(chessgamenode)
        
        self.set_counting_attributes()
        self.update(chessgamenode)
        
        self.set_strategy_attributes()
        
    ## Basic Attributes: 
    ## they are computed directly here in __init__() 
    def set_basic_attributes(self,chessgamenode):
    
        # board: chess.Board object
        # id: String object
        # turn: either chess.WHITE or chess.BLACK
        self.board = chessgamenode.board()
        self.id = self.my_fen_id(self.board.fen())
        self.turn = chessgamenode.turn() 
        
    ## Counting Attributes
    ## they are kept updated by update()
    ## while parsing the database    
    def set_counting_attributes(self):
        
        # moves: list of chess.Move
        # variation: dictionary {chess.Move : String id}
        # count_move : dictionary {chess.Move : Int}
        self.moves = []  
        self.variations = {}  
        self.count_move = {}
        
        # counters, nonnegative Integers
        self.multiplicity = 0
        self.white_wins = 0
        self.draws = 0
        self.black_wins = 0

    ## Strategy attributes
    ## they are computed in analysis()
    ## after the database has been completely parsed
    def set_strategy_attributes(self):
        
        # available_moves : list of chess.Move
        # reasonable_moves : list of chess.Move
        self.available_moves = []
        self.reasonable_moves = []
        
        # Notation: 
        # defence is the other, that will respond at the next ply
        
        # attack_advantage : dictionary {Int : Float in [-1,1]}
        # defence_advantage : dictionary {Int : Float in [-1,1]}
        # future_advantages : dictionary of dictionaries {chess.Move : {Int : Float in [-1,1]}}
        # future_defence_advantages : dictionary of dictionaries {chess.Move : {Int : Float in [-1,1]}}
        self.attack_advantage = {}
        self.defence_advantage = {}
        self.normalized_future_advantages = {}
        self.normalized_relative_advantages = {}
        self.future_defence_advantages = {}
        
        
        # attack_strategy : dictionary {Int : chess.Move}
        # defence_strategy : dictionary of dictionaries {Int : {chess.Move : Int}}
        # basic_def_strategy_encoded : dictionary {Int : chess.Move}
        self.attack_strategy = {}
        self.defence_strategy = {}        
        self.basic_strategy_encoded = {}
        
        
    
    # Utility functions
    # my_fen_id()
        
    def my_fen_id(self,fen_string):
        return re.sub('[0-9]+ [0-9]+$','FEN_id ',fen_string)
        
    # self.update() 
    # is called every time that a position is found in a database
    # in particular it is called on the first time it is found
    # chessgamenode : chess.GameNode object of the python-chess library
    def update(self,chessgamenode):
        self.multiplicity += 1
        
        game_result = chessgamenode.game().headers['Result']
        self.update_results(game_result)
        
        next_position = chessgamenode.next()
        if next_position == None:
            next_move = None
        else:
            next_move = next_position.move
            
        self.update_moves(next_move, next_position)
            
    def update_results(self,game_result):
        # with Python 3.10 you would have the syntax match...case...
        if game_result == '1-0':
            self.white_wins += 1
        if game_result == '1/2-1/2':
            self.draws += 1
        if game_result == '0-1':
            self.black_wins += 1
            
    def update_moves(self,next_move,next_position): 
        # I count also the situations in which the game does not continue (next_move = None)
        
        if next_move in self.moves:
            self.count_move[next_move] += 1

        else:
            self.moves.append(next_move)

            self.count_move[next_move] = 1
            
            if next_position==None:
                self.variations[next_move] = None
                return
            
            next_position_fen = next_position.board().fen()
            next_position_id = self.my_fen_id(next_position_fen)

            self.variations[next_move] = next_position_id