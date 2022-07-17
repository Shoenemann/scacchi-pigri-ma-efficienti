#required
import chess
import chess.pgn
import re
import math
import os #for os.path.basename() only 

#source code
# import sys
# sys.path.append('../src')
import chessposition
from lightdb import LightDatabase
import parsepgn
import databaseprune
import analysisbasic
import display
import analysislight
import lightdb


# import specific methods
from chessposition import *
from parsepgn import *
from databaseprune import *
from analysisbasic import *
from display import *
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


  def visualize_basic_info(self,id):
    pos = self.all_positions[id]
    print("id:",id,end='')
    #"fen:",pos.board().fen())
    print("move order:", pos.move_order)

  def visualize_result(self,id):
    print("result%:",pos.white_percent,pos.draws_percent,pos.black_percent, "wa=",pos.wa,end='')
    print("(",pos.white_wins,pos.draws,pos.black_wins,"tot=",pos.count,")")


      




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
        self.white_percent = RichPosition.percent(self.white_wins,self.count)
        self.black_percent = RichPosition.percent(self.black_wins,self.count)
        self.draws_percent = RichPosition.percent(self.draws,self.count)
        self.wa = (self.white_wins - self.black_wins) / self.count
        self.white_advantage = self.wa

        # list of places of variations in the lightdatabase
        # type: [Ints]
        # self.light_moves = self.compute_light_moves(chessposition)
        # self.num_moves = len(self.light_moves)
   
        # for each study_depth we will evaluate the advantage of a student-player that arrives at this position
        # type: {Ints : Floats} 
        self.student_advantage = {}

    @staticmethod
    def percent(a,b):
        return math.floor(100*(a/b))



 ###################

    # board creation of the class RichPosition
