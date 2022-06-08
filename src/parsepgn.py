import re

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