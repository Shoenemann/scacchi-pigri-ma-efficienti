import re
import chess
import chess.pgn
from chessposition import ChessPosition

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
    return chessgamenode.board().move_stack()

###
# parse new game: index by fen
# parse opening game: index by moves leading to the node

# parse a game and put it into a custom database
# dizionario : is the custom database of positions
def parse_opening_game(dizionario,new_game,depth):

    new_position = new_game

    for move in new_game.mainline_moves():  
        
        new_id = gamenode_to_movestack(new_position)

        if new_id in dizionario.keys():
            dizionario[new_id].update(new_position)
        else:
            dizionario[new_id] = ChessPosition(new_position)

        if new_position.ply() == depth:
            break
            
        new_position = new_position.variation(move)



# parse a game and put it into a custom database
# dizionario : is the custom database of positions
def parse_old_opening_game(dizionario,new_game,depth):

    new_position = new_game

    for move in new_game.mainline_moves():  
        
        new_id = gamenode_to_movestack(new_position)

        if new_id in dizionario.keys():
            dizionario[new_id].update(new_position)
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
            
        parse_new_opening_game(dictionary,game,ply_depth)

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