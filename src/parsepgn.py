import re
import chess
import chess.pgn
from chessposition import ChessPosition


def gamenode_to_id(chessgamenode):
    return re.sub('[0-9]+ [0-9]+$','FEN_id ',chessgamenode.board().fen())

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

def parse_database(pgn,num_games,ply_depth):
    
    dictionary = {}
    
    for i in range(num_games):

        game = chess.pgn.read_game(pgn)
        
        #break earlier, if there are less than num_games games, in the pgn file
        if game == None:
            break
            
        parse_new_game(dictionary,game,ply_depth)

    return dictionary



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