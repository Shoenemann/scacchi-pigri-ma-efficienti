#required
import chess
import chess.pgn
import chess.svg
import re
import math
import os #for os.path.basename() only 
from chess import *
from chess.svg import *

#source code
# import sys
# sys.path.append('../src')
import chessposition
from lightdb import LightDatabase
import parsepgn
import databaseprune
import analysisbasic
import displaychess
import analysislight
import lightdb


# import specific methods
from chessposition import *
from parsepgn import *
from databaseprune import *
from analysisbasic import *
from displaychess import *
from analysislight import *
from lightdb import *






####################

# class RichDatabase

# initialization




class RichDatabase(LightDatabase):
  def __init__(self):
    self.all_positions = {}

  def import_from_fastdatabase(self,fastdatabase):

    for i in range(fastdatabase.num_positions):
        fast_position = fastdatabase.all_positions[i]
        self.all_positions[i] = RichPosition(fast_position)

    self.calculate_move_order()

  def calculate_move_order(self):
    for i,pos in self.all_positions.items():
        for uci,var_id in pos.move_variations.items():
            variation = self.all_positions[var_id]
            variation.move_order.extend(pos.move_order)
            variation.move_order.append(uci)

            variation.ply = pos.ply + 1
        

  

  ##################################

    # Visualization methods of class Rich Database

  def visualize_info(self,id):
    self.visualize_basic_info(id)
    self.visualize_result(id)
    self.visualize_board(id)

    self.visualize_continuations(id)


  #

  def visualize_basic_info(self,id):
    pos = self.all_positions[id]
    print("id:",id,end=' ')
    #"fen:",pos.board().fen())
    print("move order:", pos.move_order)
    print("fen:", pos.fen())

  def visualize_result(self,id):
    pos = self.all_positions[id]
    print("result:",pos.white_percent,pos.draws_percent,pos.black_percent, "wa=",pos.wa,end=' ')
    print("(",pos.white_wins,pos.draws,pos.black_wins,"tot=",pos.count,")")


  def visualize_board(self,id):
    pos = self.all_positions[id]
    board = pos.board()
    display(board)

  def visualize_continuations(self,id):
    pos = self.all_positions[id]

    other_count = pos.count
    other_wins = pos.white_wins
    other_draws = pos.draws
    other_loses = pos.black_wins 

    for uci,varid in pos.move_variations.items():
        variation = self.all_positions[varid]
        
        other_count -= variation.count
        other_wins -= variation.white_wins
        other_draws -= variation.draws
        other_loses -= variation.black_wins

        print("move:",uci,end = " ")
        print("id:",varid,end=" ")
        print(percent(variation.count,pos.count),end=" ")
        print("(",variation.count,")", end = " ")
        print("wa=",variation.wa)

    if other_count == 0 :
        print("other: none")
    else:
        other_white_advantage = (other_wins - other_loses) / other_count
        other_wa = percent(other_white_advantage,1,1) 
        
        print("other:",end=" ")
        print(percent(other_count,pos.count),end=" ")
        print("(",other_count,")", end = " ")
        print("wa=",variation.wa)


  #

  
      




##############################
####################################################################
####################################################################
###########################

  # class RichPosition

  # basic creation of the class





  
class RichPosition(LightPosition):
    def __init__(self,chessposition):

        #Here chessposition is a FastPosition object

        # it is not possible to deduce the ply at chessposition level. I will update it later at RichDictionary level
        self.ply = 0
        self.move_order = []

        self.move_variations = chessposition.move_variations

        self.count = chessposition.count
        self.white_wins = chessposition.white_wins
        self.black_wins = chessposition.black_wins
        self.draws = self.count - self.white_wins - self.black_wins
        self.white_percent = percent(self.white_wins,self.count)
        self.black_percent = percent(self.black_wins,self.count)
        self.draws_percent = percent(self.draws,self.count)
        self.white_advantage = (self.white_wins - self.black_wins) / self.count
        self.wa = percent(self.white_advantage,1,1)

        # list of places of variations in the lightdatabase
        # type: [Ints]
        # self.light_moves = self.compute_light_moves(chessposition)
        # self.num_moves = len(self.light_moves)
   
        # for each study_depth we will evaluate the advantage of a student-player that arrives at this position
        # type: {Ints : Floats} 
        self.student_advantage = {}



    ###################

    # board creation of the class RichPosition

    def board(self):
        board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        for uci in self.move_order:
            board.push(chess.Move.from_uci(uci))
        return board

    def fen(self):
        return self.board().fen()









####################
# ##################################
# #################################
#     ########






# utility methods methods

def percent_number(a,b,digits=0):
    ee  = 10**digits
    return math.floor(100*ee*(a/b))//ee

def percent(a,b,digits=0):
    return str(percent_number(a,b,digits)) + '%'


