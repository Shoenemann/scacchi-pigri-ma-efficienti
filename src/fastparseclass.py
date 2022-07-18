import chess
import chess.pgn

# for clear_output
from IPython.display import clear_output


class FastDictionary:
  def __init__(self):
    #self.max_ply = maxply
    self.num_positions = 0
  
    self.all_positions = []

    self.new_position()

  def new_position(self):
    pos = FastPosition()
    self.all_positions.append(pos)
    self.num_positions += 1
    return self.num_positions - 1



class FastPosition:
  def __init__(self):
    #self.ply = ply

    self.move_variations = {}

    self.white_wins = 0 
    self.black_wins = 0
    self.count = 0    

  def update_count(self,game_result):
    self.count += 1

    if game_result == '1-0':
        self.white_wins += 1
    if game_result == '0-1':
        self.black_wins += 1



def fastparse_database(pgn,num_games,ply_depth,verbosity=1000):
  
  dictionary = FastDictionary()
  
  for i in range(num_games):
    if verbosity>0 and i%verbosity ==0:
      clear_output()
      print(i)

    game = chess.pgn.read_game(pgn)
    
    if game == None:
        break
        
    fastparse_game(dictionary,game,ply_depth,"normal")

  return dictionary



def fastenrich_database(pgn,num_games,ply_depth,dictionary,verbosity=1000):
    
  for i in range(num_games):
    if verbosity>0 and i%verbosity ==0:
      clear_output()
      print(i)
      

    game = chess.pgn.read_game(pgn)
    if game == None:
      break
        
    fastparse_game(dictionary,game,ply_depth,"enrich")

  return dictionary






def fastparse_game(fastdictionary,game,ply_depth,mode = "normal"):
    
    game_result = game.headers['Result']
    position = fastdictionary.all_positions[0]
    position.update_count(game_result)
    
    ply = 1

    for move in game.mainline_moves():
        uci = move.uci()

        if uci not in position.move_variations.keys():

            if mode == "enrich":
              # when we are in the mode "enrich", we update positions that are already in the database
              # if we encounter a completely new position, we just abort the game parse and pass to the next game
              break

            variation = fastdictionary.new_position()
            position.move_variations[uci]=variation

        else:
            variation = position.move_variations[uci]

        position = fastdictionary.all_positions[variation]
        position.update_count(game_result)

        ply += 1
        if ply == ply_depth:
          break
