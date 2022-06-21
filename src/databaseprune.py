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
import analysislight


# import specific methods
from chessposition import *
from parsepgn import *
from databaseprune import *
from analysisbasic import *
from display import *
from analysislight import *

from copy import deepcopy

# overview of the functions that are really used
from parsepgn import parse_new_game


def my_prune(database,threshold):
    copy_database = deepcopy(database)
    
    keys_to_delete = {k for k in database.keys() if database[k].multiplicity<threshold}
    
    for k in keys_to_delete:
        del copy_database[k]
        
    return copy_database


def prune(database,threshold):
    keys_to_delete = {k for k in database.keys() if database[k].multiplicity<threshold}
    for k in keys_to_delete:
        del database[k]

def root_game(database):
  root_id = list(database.keys())[0] 
  return databasee[root_id]