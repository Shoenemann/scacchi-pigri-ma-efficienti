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
import parsepgn
import databaseprune
import analysisbasic
import display


# import specific methods
from chessposition import *
from parsepgn import *
from databaseprune import *
from analysisbasic import *
from display import *

# overview of the functions that are really used
from parsepgn import parse_new_game

#############################################
##      Table of contents
##   1. class light attack position
##   2. class light database


#############################################
##     1.       class light position



class LightPosition:
    def __init__(self,chessposition,fen2id):

        self.ply = chessposition.ply

        # list of places of variations in the lightdatabase
        # type: [Ints]
        self.light_moves = self.compute_light_moves(chessposition,fen2id)
        self.num_moves = len(self.light_moves)

        # the advantage estmates the quantity (wins-loses)/games
        # type: Float
        self.white_advantage = (chessposition.white_wins - chessposition.black_wins) / chessposition.multiplicity
        
        # for each study_depth we will evaluate the advantage of a student-player that arrives at this position
        # type: {Ints : Floats} 
        self.student_advantage = {}

    def compute_light_moves(self,chessposition,fen2id):

        # maybe I should not iterate over the variations, but over the reasonable moves
        # [] check this

        light_moves = []


        # type ChessPosition.variations_movestack: 
        # dictionary {chess.Move : String id}
        for varFEN in chessposition.available_variations_movestack.values():
          # it is not actually a FEN, 
          # but it is a string that identifies the game position 
          # see parsepgn.py  
          if varFEN == None:
            continue

          light_variation_id = fen2id[varFEN]

          light_moves.append(light_variation_id)

        return light_moves

class LightAttackPosition(LightPosition):
    def __init__(self,chessposition,fen2id):
        super().__init__(chessposition,fen2id)

        #self.student_advantage[0]
        if chessposition.turn == chess.WHITE:
            self.student_advantage[0]=self.white_advantage
        else:
            self.student_advantage[0] = 0-self.white_advantage

        # for every study_depth we choose the move that gives best advantage, or none
        self.attack_strategy = { 0: None }

        # this is explained in analysislight.analysis_atk
        self.analysis_data = {}


class LightDefencePosition(LightPosition):
    def __init__(self,chessposition,fen2id):
        super().__init__(chessposition,fen2id)

        #self.student_advantage[0]
        if chessposition.turn == chess.WHITE:
            self.student_advantage[0] = 0-self.white_advantage
        else:
            self.student_advantage[0]= self.white_advantage

        self.move_probability = self.compute_move_probabilities(chessposition,fen2id)
        
        self.other_moves_student_advantage = self.compute_other_moves_student_advantage(chessposition)

        # the following data structure requires some explanation
        # the explanation will be given in the analysis function
        # in analysislight.analysis_def
        self.analysis_data = {}
        self.auxiliary_advantages = {}
        self.auxiliary_efforts = {}
        
        self.defence_strategy = {}

    def compute_other_moves_student_advantage(self,chessposition):
        
        # after having used compute_end_leaf_advantage
        if chessposition.end_leaf_white_advantage == 0.0:

            compute_end_leaf_advantage(chessposition)

        other_moves_white_advantage = chessposition.end_leaf_white_advantage

        if chessposition.turn == chess.WHITE:
            return 0-other_moves_white_advantage
        else:
            return other_moves_white_advantage


    def compute_move_probabilities(self,chessposition,fen2id):
        # maybe I should not iterate over the variations, but over the reasonable moves
        # [] check this

        probability_moves = {}

        # type ChessPosition.variations_movestack: 
        # dictionary {chess.Move : String id}
        for move, varFEN in chessposition.available_variations_movestack.items():
          # it is not actually a FEN, 
          # but it is a string that identifies the game position 
          # see parsepgn.py  
          if varFEN == None:
            continue

          light_variation_id = fen2id[varFEN]

          probability_moves[light_variation_id] = chessposition.count_move[move] / float(chessposition.multiplicity)
	
        probability_moves["other moves"] = chessposition.end_leaf_count / float(chessposition.multiplicity)

        return probability_moves

####################################

class LightDatabase:
    def __init__(self,database,player,maxply):
        
        fen_ids = list(database.keys())
        self.id2fen = {i : fen_ids[i] for i in range(len(fen_ids))}
        self.fen2id = {fen_ids[i] : i for i in range(len(fen_ids))}

        self.max_ply = maxply
        self.num_positions = len(fen_ids)


        
        for position in database.values():   
            calculate_available_moves(position,database)

        self.all_positions = {}
        # compute all_positions
        for i in range(self.num_positions):

            chessposition = database[fen_ids[i]]

            self.all_positions[i] = self.new_light_position(chessposition,player,self.fen2id)


        self.positions_by_ply = {}
        for p in range(maxply+1):
            self.positions_by_ply[p] = [ ids for ids, pos in self.all_positions.items() if pos.ply == p ]

            if len(self.positions_by_ply[p]) == 0:
                
                self.positions_by_ply.pop(p,None)

                self.max_ply = p-1
                break

    def new_light_position(self,chessposition,player,fen2id):

        ply = chessposition.ply

        if player == "white" and ply%2 == 0: 
            return LightAttackPosition(chessposition,fen2id)

        if player == "black" and ply%2 == 1: 
            return LightAttackPosition(chessposition,fen2id)

        if player == "white" and ply%2 == 1: 
            return LightDefencePosition(chessposition,fen2id)

        if player == "black" and ply%2 == 0: 
            return LightDefencePosition(chessposition,fen2id)

