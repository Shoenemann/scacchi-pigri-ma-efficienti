import re
import chess
import chess.pgn
from chessposition import ChessPosition
import fastparseclass
from fastparseclass import *



## known issues
# [] 
# in parsing the games we look if a key exists in a database
# we use `if new_id in dizionario.keys():`
# but it is not clear if it is the most efficient way to look this up
# []
# we are parsing games with python.chess
# this library is great, but it is a bit slow
# perhaps we can parse pgns with another lighter library
# and then call python.chess only when we need to visualize the strategy and so on


def gamenode_to_id(chessgamenode):
    return re.sub('[0-9]+ [0-9]+$','FEN_id ',chessgamenode.board().fen())

def gamenode_to_movestack(chessgamenode): 
    
    movestack =  chessgamenode.board().move_stack
    #this is a list of moves
    # lists are unhashable, so we need to convert to a string
    
    movestack_uci_str = [move.uci() for move in movestack]
    
    # the pyhon join() method is a little weird backward
    return "".join(movestack_uci_str)

#########################
##################
######



###
# parse new game: index by fen
# parse opening game: index by moves leading to the node
# parse a game and put it into a custom database
# dizionario : is the custom database of positions
def parse_opening_game(dizionario,new_game,depth):

    new_position = new_game

    for move in new_game.mainline_moves():  
        
        new_id = gamenode_to_movestack(new_position)

        if new_position.ply() == depth:
            is_end_leaf = True
        else:
            is_end_leaf = False

        if new_id in dizionario.keys():
            dizionario[new_id].update(new_position,is_end_leaf)
        else:
            dizionario[new_id] = ChessPosition(new_position,is_end_leaf)

        if new_position.ply() == depth:
            break
            
        new_position = new_position.variation(move)

def check_if_is_end_leaf(dizionario,new_position,mode,depth):
    # use this if the old database ply depth
    # is equal to the current depth
    # todo: need an attribute max_ply of the database
    if mode == 1:
        if new_position.ply() == depth:
                is_end_leaf = True
        else:
            is_end_leaf = False

    # use this if you are not sure that the two depths agree
    # so we need to check manually if it is indeed an end leaf
    # the algorithms can be greatly improved 
    # by looking at the available moves, instead of the dictionary keys lookup
    if mode == 2:
        next_position = new_position.next()
        next_id = gamenode_to_movestack(next_position)

        if next_id in dizionario.keys():
            is_end_leaf = False
        else:
            is_end_leaf = True
    
    if mode == 3:
        # I will write here the algorithm with available_moves_lookup
        return 3



# parse a game and put it into a custom database
# dizionario : is the custom database of positions
def parse_old_opening_game(dizionario,new_game,depth):
    
    new_position = new_game

    for move in new_game.mainline_moves():  
        
        new_id = gamenode_to_movestack(new_position)

        # this block is not very fast, I (luca) know how to 
        # implement it more efficiently, but let's just make it work for the moment
        # btw, we can package this into a method
        # "check if_is"
        is_end_leaf = check_if_is_end_leaf(dizionario,new_position,1,depth)

        if new_id in dizionario.keys():
            dizionario[new_id].update(new_position,is_end_leaf)
        else:
            break

        if new_position.ply() == depth:
            break
            
        new_position = new_position.variation(move)



#break earlier, if there are less than num_games games, in the pgn file
def parse_database(pgn,num_games,ply_depth):
    
    dictionary = {}
    
    for i in range(num_games):

        game = chess.pgn.read_game(pgn)
        
        if game == None:
            break
            
        parse_opening_game(dictionary,game,ply_depth)

    return dictionary

#break earlier, if there are less than num_games games, in the pgn file
def enrich_database(dictionary,pgn,num_games,ply_depth):
    
    for i in range(num_games):

        game = chess.pgn.read_game(pgn)
        
        if game == None:
            break
            
        parse_old_opening_game(dictionary,game,ply_depth)

    return 





######################
######################


# I did not implement is_end_leaf in the following two functions


# parse a game and put it into a custom database
# dizionario : is the custom database of positions
def parse_new_game(dizionario,new_game,depth):

    new_position = new_game

    for move in new_game.mainline_moves():  
        
        new_id = gamenode_to_id(new_position)

        if new_id in dizionario.keys():
            dizionario[new_id].update(new_position)
        else:
            dizionario[new_id] = ChessPosition(new_position)

        if new_position.ply() == depth:
            break
            
        new_position = new_position.variation(move)

# parse a game and put it into a custom database
# dizionario : is the custom database of positions
def parse_old_game(dizionario,new_game,depth):

    new_position = new_game

    for move in new_game.mainline_moves():  
        
        new_id = gamenode_to_id(new_position)

        if new_id in dizionario.keys():
            dizionario[new_id].update(new_position)
        else:
            break

        if new_position.ply() == depth:
            break
            
        new_position = new_position.variation(move)



#break earlier, if there are less than num_games games, in the pgn file
def parse_position_database(pgn,num_games,ply_depth):
    
    dictionary = {}
    
    for i in range(num_games):

        game = chess.pgn.read_game(pgn)
        
        if game == None:
            break
            
        parse_new_game(dictionary,game,ply_depth)

    return dictionary

#break earlier, if there are less than num_games games, in the pgn file
def enrich_position_database(dictionary,pgn,num_games,ply_depth):
    
    for i in range(num_games):

        game = chess.pgn.read_game(pgn)
        
        if game == None:
            break
            
        parse_old_game(dictionary,game,ply_depth)

    return 




def parse_database_verbose(pgn,num_games,ply_depth):
    
    dictionary = {}
    i=0
    
    while i < num_games:

        game = chess.pgn.read_game(pgn)
        
        #break earlier, if there are less than num_games games, in the pgn file
        if game == None:
            break
            
        i += 1
        parse_new_game(dictionary,game,ply_depth)
        
    file_name = pgnfile_name(pgn)
    num_positions = len(dictionary.keys())

    print(f"Read {i} games from {file_name}. Stored {num_positions} chess positions.")

    return dictionary
    

#########

import os
def pgnfile_name(io_textwrapper_object):

    path_file = io_textwrapper_object.name

    return os.path.basename(path_file)