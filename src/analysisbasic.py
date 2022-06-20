# analysis functions () 
# are to be called only when the database has been read in its entirety
# database : dictionary {String id : ChessPosition object}
###############
## analysis() is the main analysis function
## it calls all other analysis functions
##
## it is better to separate the cycles of attack and defence, 
## because the attack analysi depends on databasewise updated defence analysis and viceversa
###############
def analysis(database,num_iterations):
    
    print("how many positions at beginning", len(database.keys()))
    my_database = my_prune(database,5)
    print("how many positions after pruning", len(my_database.keys()))
    
    white_database = my_database #trim_unreasonable_moves(my_database,"white",0.1)
    black_database = my_database #trim_unreasonable_moves(my_database,"black",0.1)
    print("how many positions trimming white", len(white_database.keys()))
    print("how many positions trimming black", len(black_database.keys()))

    
    analysis_white(white_database,num_iterations)
    
    analysis_black(black_database,num_iterations)
    
    analysed_database = {k:pos for k,pos in database.items()}
    merge_analysis(analysed_database,white_database,black_database)
    
    return analysed_database
    
#####
## merging
#####
    
def merge_analysis(dd,wd,bd):
    
    for key in wd.keys():
    
        pos1 = dd[key]
        pos2 = wd[key]
        
        if pos2.turn == chess.WHITE:
            overwrite_attack_strategy(pos1,pos2)
        else:
            overwrite_defence_strategy(pos1,pos2)
            
    for key in bd.keys():
    
        pos1 = dd[key]
        pos2 = bd[key]
        
        if pos2.turn == chess.BLACK:
            overwrite_attack_strategy(pos1,pos2)
        else:
            overwrite_defence_strategy(pos1,pos2)

def overwrite_attack_strategy(pos1,pos2):
    pos1.available_moves = pos2.available_moves
    pos1.reasonable_moves = pos2.reasonable_moves

    pos1.attack_advantage = pos2.attack_advantage
    pos1.future_defence_advantages = pos2.future_defence_advantages

    pos1.attack_strategy = pos2.attack_strategy
    
def overwrite_defence_strategy(pos1,pos2):
    pos1.available_moves = pos2.available_moves
    
    pos1.defence_advantage = pos2.defence_advantage
    pos1.normalized_future_advantages = pos2.normalized_future_advantages
    pos1.normalized_relative_advantages = pos2.normalized_relative_advantages
    
    pos1.defence_strategy = pos2.defence_strategy   
    pos1.basic_strategy_encoded = pos2.basic_strategy_encoded
####################
## 
## analysis_white() plays as white 
##    student = chess.WHITE , opponent = chess.BLACK
##
## analysis_black() plays as black
##    student = chess.BLACK , opponent = chess.WHITE
##
####################

def analysis_white(database,num_iterations):
    analysis_student(database,num_iterations,chess.WHITE)
    
def analysis_black(database,num_iterations):
    analysis_student(database,num_iterations,chess.BLACK)

## student is either chess.WHITE or chess.BLACK
## opponent is the opposite
def analysis_student(database,num_iterations,student):
    
    student_positions = [key for key in database.keys() if database[key].turn == student]
    opponent_positions = [key for key in database.keys() if database[key].turn != student]
    
    analysis_reset(database)
    analysis_start(database)
    
    for i in range(num_iterations):
        
        for key in student_positions:
            position = database[key]
            analysis_attack(position,database)
            
        for key in opponent_positions:
            position = database[key]
            analysis_defence(position,database)
####################
# analysis_reset()
####################
def analysis_reset(database):
    for pos in database.values():
        pos.set_strategy_attributes()
###########################
## analysis_start is the first function that has to be called on a database
## it calculates the available moves and the advantage that the position gives even if no study of its tree is done
## a reasonable move is one that is not unpopular: I am putting a threshold 10%
###########################
def analysis_start(database):
    ### print("starting",database)
    for position in database.values():   
        calculate_zeroth_advantage(position)
        calculate_available_moves(position,database)
        calculate_reasonable_moves(position,database,0.1)
        
def trim_unreasonable_moves(database,player,threshold):
     
    if player == "white":
        student_turn = chess.WHITE
    else:
        student_turn = chess.BLACK

    visited_reasonable_keys = []
    unvisited_reasonable_keys = []
    
    # the empty board is
    # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - FEN_id
    # so it is reasonable to start from here
    #
    # when we will have more complex 'root positions', we will refactor this part of the code
    
    unvisited_reasonable_keys.append("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - FEN_id ")
    
    while len(unvisited_reasonable_keys) > 0:
        new_key = unvisited_reasonable_keys.pop(0)        
        position = database[new_key]
        
        calculate_available_moves(position,database)
        
        if position.turn == student_turn:
            calculate_reasonable_moves(position,database,threshold)
            
            follow_moves = position.reasonable_moves
        else:
            follow_moves = position.available_moves
            
        follow_variations_keys = [position.variations[move] for move in follow_moves]
        
        for k in follow_variations_keys:
            if k not in visited_reasonable_keys:
                if k not in unvisited_reasonable_keys:
                    unvisited_reasonable_keys.append(k)
        
        visited_reasonable_keys.append(new_key)
        
    return {key:database[key] for key in visited_reasonable_keys}
   
        
def calculate_reasonable_moves(position,database,threshold):
    position.reasonable_moves = []
    
    for move in position.available_moves:
        popularity = position.count_move[move]/position.multiplicity
        if popularity > threshold:
            position.reasonable_moves.append(move)
            
def calculate_available_moves(position,database):
    position.available_moves = []
    
    for move,variation in position.variations.items(): 
        if variation in database.keys():
            position.available_moves.append(move)  

    for move in position.available_moves:
        position.available_variations[move] = position.variations[move]
        position.available_variations_movestack[move] = position.variations[move] 
            
def calculate_zeroth_advantage(position):
    white_advantage = (position.white_wins - position.black_wins) / position.multiplicity

    if position.turn == chess.WHITE:
        position.attack_advantage[0] = white_advantage
        position.defence_advantage[0] = 0-white_advantage
    else:
        position.defence_advantage[0] = white_advantage
        position.attack_advantage[0] = 0-white_advantage
        
    position.attack_strategy[0] = None
    position.defence_strategy[0] = {k:0 for k in position.available_moves}           

##########################
##########################
## analysis_attack() is very easy
## it just looks at the possible moves
## then chooses the move that promises highest advantage if studied at some depth
##
## calculate_variations_advantage() studies all available variations after one move, playing them as the defence
####################################

def analysis_attack(position,database): 
    
    if len(position.reasonable_moves) ==0 :
        return
    
    calculate_variations_advantages(position,database)
    # future_defence_advantages : dictionary of dictionaries {chess.Move : {Int : Float in [-1,1]}}
    variations_advantages = position.future_defence_advantages
    
    variations_knowledge_depth = {m: len(variations_advantages[m]) for m in position.reasonable_moves}
    knowledge_depth = min(variations_knowledge_depth.values())
    
    ##
    ## the fact that we study only up to knowledge_depth is questionable.
    ## I will need to improve this point with upper bounds on unexplored branches
    ##
    
    for d in range(knowledge_depth): 
        
        slice_advantages = {move:variations_advantages[move][d] for move in position.reasonable_moves}
        
        best_move = max(slice_advantages,key=slice_advantages.get)
        
        position.attack_strategy[d+1] = best_move
        position.attack_advantage[d+1] = slice_advantages[best_move]  
        
def calculate_variations_advantages(position,database):
    for move in position.reasonable_moves:
        chess_variation = database[position.variations[move]]
        
        position.future_defence_advantages[move] = chess_variation.defence_advantage
        
###################
###################
## analysis_defence is the core function
## it takes into account all possible variations that can be studied
## and for each of these variations it balances difficulty of study and gained advantages
## in the end, it tells how much effort to put in the study of each variation


def analysis_defence(position,database):

    if len(position.available_moves) ==0 :
        # if there are no available moves in the database, then we are not even able to study further, after this position
        return
    
    # enter each variation and imagine to play as the attack 
    calculate_future_advantages(position,database)

    branches = position.normalized_relative_advantages
    max_depth = {m:len(branches[m]) for m in position.available_moves }

    for m in position.available_moves:
        if max_depth[m] == 0:
            # if max_depth[m]==0 it means that the variation exists in the database after one move, 
            # but we cannot study it because we do not have any second ply as countermove in the database
            # 
            # admittedly, the fact that we return the analysis completely if one tiny branch has no 2-depth moves is questionable
            # another approach would be to restrict the available moves and continue the analysis
            #
            # another better approach would be to estimate the maximum advantage we could theoretically gain from a nonvisited branch
            # 
            # another better approach would be to queue the missing position in the requests for database expansions
            return
        
    # setup_study_branches()
    # branches[m][0] tells this:
    #   if we study only a One-Move continuation after Move m, how much do we gain in terms of winning probability? 
    branches_study_depth = {m:0 for m in position.available_moves}
    branches_advantages = {m:branches[m][0] for m in position.available_moves}

    
    studying = True
    total_study_depth = 0
    
    # knowledge reset
    #position.basic_strategy_encoded = {}
    #zeroth_advantage = position.defence_advantage[0]
    #position.defence_advantage = {}
    #position.defence_advantage[0] = zeroth_advantage
        
    while studying:
        
        ### begin debug
        if position.id == list(dizionario.keys())[0]:
            display(branches_study_depth)
        ### end debug
        
        # this is the next move of the opponent that is best to study now
        best_next_move = max(branches_advantages,key=branches_advantages.get)
         
        position.basic_strategy_encoded [total_study_depth] = best_next_move

        total_study_depth += 1
        
        # position.defence_advantage[0] has already been computed in analysis_start. Otherwise error
        advantage_increment = branches_advantages[best_next_move]
        new_advantage =  position.defence_advantage[total_study_depth-1] + advantage_increment
        
        position.defence_advantage[total_study_depth] = new_advantage
        
        # now we "study_one_more_node()"
        new_depth = branches_study_depth[best_next_move] + 1
        branches_study_depth[best_next_move] = new_depth
        
        # parse_basic_strategy()
        position.defence_strategy[total_study_depth] = {m:d for m,d in branches_study_depth.items()}
        
        if new_depth == max_depth[best_next_move]:
            studying = False
        else: 
            # todo: update_study_branches() 
            # todo optimization: estimate_upperbound_advantage() 
            branches_advantages[best_next_move] = branches[best_next_move][new_depth]
            

def delta(lista):
	return {i: lista[i+1]-lista[i] for i in range(len(lista)-1)}

def calculate_future_advantages(position,database):
	position.normalized_future_advantages = {}
	position.normalized_relative_advantages = {}
	
	for move in position.available_moves:
		variation = position.variations[move]
		
		future_advantage = database[variation].attack_advantage
		relative_advantage = delta(future_advantage)
		
		probability = position.count_move[move] / float(position.multiplicity)
		normalized_future_advantage =  {i:adv*probability for i,adv in future_advantage.items()}
		normalized_relative_advantage = {i:adv*probability for i,adv in relative_advantage.items()}
		
		position.normalized_future_advantages[move] = normalized_future_advantage
		position.normalized_relative_advantages[move] = normalized_relative_advantage
			


######################


def compute_end_leaf_advantage(position,database):
    if position.end_leaf_count == 0:

        position.end_leaf_white_advantage = 0 

        return 
        
    a= position.end_leaf_white_wins
    b= position.end_leaf_black_wins
    c= position.end_leaf_count
    position.end_leaf_white_advantage = (a-b) / float(c)