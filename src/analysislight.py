
def analysis_atk(position,lightdb,max_study): 
    
    if len(position.light_moves) ==0 :
        return
    
    for move in position.light_moves:
        variation = lightdb.all_positions[move]

        # the analysis of best move is based on advantages of variations
        position.analysis_data[move] = variation.student_advantage

    
    for d in range(max_study): 
        
        slice_advantages = {move:analysis_data[move][d] for move in position.light_moves}
        
        if len(slice_advantages) == 0:
            break

        best_move = max(slice_advantages,key=slice_advantages.get)
        
        position.attack_strategy[d+1] = best_move
        position.student_advantage[d+1] = slice_advantages[best_move]  
    