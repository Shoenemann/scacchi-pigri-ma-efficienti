## colors

import math 

def transparent_green(percent):
    decimal = 16+math.floor(239*percent)
    hexx = str(hex(decimal))[2:]
    return "#209920"+hexx

def blue():
    return "#3344ff"

def orange():
    return "#777700"


######################

## given a position of an analyzed database,and
## given a study depth, 
## display the strategy to study

def display_white_strategy(database,position,depth):
    if position.turn == chess.WHITE:
        display_full_attack_strategy(database,position,depth,None)
    else:
        display_full_defence_strategy(database,position,depth,None)
        
def display_black_strategy(database,position,depth):
    if position.turn == chess.BLACK:
        display_full_attack_strategy(database,position,depth,None)
    else:
        display_full_defence_strategy(database,position,depth,None)
        
####################

def display_full_attack_strategy(database,position,depth,previous_move):
    
    if depth ==0:
        return
    
    
    best_move = position.attack_strategy[depth]
    display_board_with_moves(position,[],best_move,previous_move)
    
    new_position = database[position.variations[best_move]]
    display_full_defence_strategy(database,new_position,depth-1,best_move)
    
    
def display_full_defence_strategy(database,position,depth,previous_move):
    
    if depth ==0:
        return
    
    child_moves = {move:d for move,d in position.defence_strategy[depth].items() if d!=0}
    display_board_with_moves(position,child_moves.keys(),None,previous_move)
    
    for move,new_depth in child_moves.items():
        
        if new_depth == 0:
            return
            
        new_position = database[position.variations[move]]
        display_full_attack_strategy(database,new_position,new_depth,move)
    
    
#####################
    
    
def display_board_with_moves(pos,greenmoves,bluemove,orangemove):
    arr = []
    
    for move in greenmoves:
        col = transparent_green(0.9)
        arr.append(chess.svg.Arrow(move.from_square,move.to_square, color=col))
        
    if bluemove != None:
        move = bluemove
        col = blue()
        arr.append(chess.svg.Arrow(move.from_square,move.to_square, color=col))
    
    if orangemove != None:
        move = orangemove
        col = orange()
        arr.append(chess.svg.Arrow(move.from_square,move.to_square, color=col))
        
    svg = chess.svg.board(pos.board,arrows=arr, size=300)
    display(svg)


###############

def display_root_strategy(database,turn):
    first_game_id = list(database.keys())[0] 
    first = database[first_game_id]
    
    
    if turn==chess.WHITE:
        max_depth = len(first.attack_advantage) - 1
        
        display_white_strategy(database,first,max_depth)
    
    if turn==chess.BLACK: 
        max_depth = len(first.defence_advantage) - 1
        
        display_black_strategy(database,first,max_depth) 
    
############



def display_basic_attributes(pos):
    print("Displaying basic attributes...")
    print(pos.id)
    print("White to move? ",pos.turn)
    #print(chess.WHITE)
    #print(pos.turn== chess.WHITE)
    display(pos.board)
    print("End display basic attributes.")
    print("------------")
    
def display_counting_attributes(pos):
    print("Displaying counting attributes")
    print("total: ",pos.multiplicity)
    print("white, draws, black: ", pos.white_wins,pos.draws,pos.black_wins)
    display(pos.moves)
    arr = []
    for move in pos.available_moves:
        col = transparent_green(pos.count_move[move]/pos.multiplicity)
        arr.append(chess.svg.Arrow(move.from_square,move.to_square, color=col))
    svg = chess.svg.board(pos.board,arrows=arr, size=300)
    display(svg)
    display(pos.variations)
    display(pos.count_move)
    
    print("End display counting attributes.")
    print("------------")
    
def display_strategy_attributes(pos):
    print("Displaying strategy attributes")
    print("available_moves: all but ", len(pos.moves)-len(pos.available_moves))
    display(pos.available_moves)
    print("advantages: attack, fut def, defence, normalized fut, normal relative,")
    display(pos.attack_advantage)
    display(pos.future_defence_advantages)
    display(pos.defence_advantage)
    display(pos.normalized_future_advantages)
    display(pos.normalized_relative_advantages)
    print("strategies: attack, defence, basic encoded")
    display(pos.attack_strategy)    
    display(pos.defence_strategy)
    display(pos.basic_strategy_encoded)
    display(pos.board)
    
    print("End display strategy attributes.")
    print("------------")

def display_attack_strategy(pos):
    print("Displaying attack strategy")
    print("reasonable moves")
    display(pos.reasonable_moves)
    print("advantages: attack")
    display(pos.attack_advantage)
    print("strategy:")
    display(pos.attack_strategy) 
    print("popularity:")
    popularity = {move:pos.count_move[move]/pos.multiplicity for move in pos.attack_strategy.values() if move != None}
    display(popularity)
    #
    arr = []
    for move in popularity.keys():
        col = transparent_green(popularity[move])
        arr.append(chess.svg.Arrow(move.from_square,move.to_square, color=col))
    svg = chess.svg.board(pos.board,arrows=arr, size=300)
    display(svg)
    #
    print("data:")
    display(pos.future_defence_advantages) 
    for move in pos.reasonable_moves:
        lvar = pos.variations[move]
        pvar = adizionario[lvar]
        print(pvar.available_moves)
    #display(pos.board)
    print("End display attack strategy.")
    print("------------")
    

def display_defence_strategy(pos):
    print("Displaying defence strategy")
    print("available_moves: all but ", len(pos.moves)-len(pos.available_moves))
    display(pos.available_moves)
    print("advantages: defence, strategy")
    display(pos.defence_advantage)
    display(pos.defence_strategy)
    print("data: normalized fut, normal relative")
    display(pos.normalized_future_advantages)
    display(pos.normalized_relative_advantages)
    print("strategy basic encoded")   
    display(pos.basic_strategy_encoded)
    display(pos.board)
    
    print("End display strategy attributes.")
    print("------------")
    print("Displaying defence strategy")
    