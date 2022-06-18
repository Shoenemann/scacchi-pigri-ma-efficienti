
def analysis_atk(position,lightdb,max_study): 
    
    if position.num_moves ==0 :
        return
    
    for move in position.light_moves:
        variation = lightdb[move]

        # the analysis of best move is based on advantages of variations
        position.analysis_data[move] = variation.student_advantage

    
    for d in range(max_study): 
        
        slice_advantages = {move:analysis_data[move][d] for move in position.light_moves}
        
        if len(slice_advantages) == 0:
            break

        best_move = max(slice_advantages,key=slice_advantages.get)
        
        position.attack_strategy[d+1] = best_move
        position.student_advantage[d+1] = slice_advantages[best_move]




def analysis_def(position,lightdb,max_study):

    if position.num_moves ==0 :
        # if there are no available moves in the database, then we are not even able to study further, after this position
        return
    

    for m in range(position.num_moves):

        move = position.light_moves[m]
        variation = lightdb[move]

        # the analysis of best move is based on advantages of variations
        # these advantages are normalized by probability of entering the variation

        prob = position.move_probability[move]

        position.analysis_data[m] = {depth,prob*adv for depth,adv in variation.student_advantage.items()}

    # the missing part is the consideration of moves that are not ... considered
    # in a sense it is like having an extended light move array, where
    # we add 'none' at the end... it will be easy but I disregard in this commit
    if position.num_moves == 1:

        position.student_advantage = position.analysis_data[position.light_moves[0]]

        position.defence_strategy = [d: position.light_moves[0] for for d in range(len(position.student_advantage))]

        return

    for m in range(1,position.num_moves):

        if m==1:
            study1 = position.analysis_data[0]
        else:
            study1 = position.auxiliary_advantages[m-1]

        study2 = position.analysis_data[m]
            
        #compute auxiliary_advantages[m]
        #and auxiliary_efforts[m]
        mth_analysis_pair = distribute_study_efforts(study1,study2,max_study)

        position.auxiliary_advantages[m] = mth_analysis_pair["advantages"]
        position.auxiliary_efforts[m] = mth_analysis_pair["efforts"]

    
    position.student_advantage = position.auxiliary_advantages[position.num_moves]
    
    max_study_effort = len(position.student_advantage)
    # from the auxiliary efforts one can reconstruct the strategy
    position.defence_strategy = parse_light_defence_strategy(position,max_study_effort)


def distribute_study_efforts(study1,study2,max_study):

    auxiliary_efforts = {}
    auxiliary_advantages = {}

    len1=len(study1)
    len2=len(study2)

    for d in range(max_study+1):

        if d  > len1+len2-2:
            break

        if len2>d:
            i_min = 0
        else: 
            i_min = d-len2+1

        if len1>d:
            i_max = d
        else: 
            i_max = len1-1

        auxiliary_sums = [ study1[i]+study2[d-i] for i in range(i_min,i_max+1) ]

        auxiliary_efforts[d] = max(auxiliary_sums,key=auxiliary_sums.get)
        auxiliary_advantages[d] = auxiliary_sums[auxiliary_efforts[d]]
    
    return {"advantages": auxiliary_advantages,"efforts":auxiliary_efforts}

def parse_light_defence_strategy(position,max_study_effort):

    strategy = {}

    for d in range(max_study_effort):

        strategy[d] = {}
        remaining_effort = d

        for m in reversed(range(1,position.num_moves)):

            strategy[d][m] = remaining_effort - position.auxiliary_study_efforts[m]
            remaining_effort = position.auxiliary_study_efforts[m]

        strategy[d][0] = remaining_effort

    return strategy



