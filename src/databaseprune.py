def my_prune(database,threshold):
    copy_database = {k:pos for k,pos in database.items()}
    
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