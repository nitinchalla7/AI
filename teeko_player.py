import random
import copy
from pprint import pprint

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    counter = 0
    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        def test_place(board, move, piece):
            if len(move) > 1:
                board[move[1][0]][move[1][1]] = ' '
            board[move[0][0]][move[0][1]] = piece
            return board
        
        def get_valid_locations(state):
            valid_locations = []
            for r in range(5):
                for c in range(5):
                    if state[r][c] == ' ':
                        valid_locations.append([r,c])
            return valid_locations
        def heuristic_game_value(state):
            return self.score_board(state, self.my_piece)
    
        def minimax(board, depth, alpha, beta, max_player):
           #pprint(locals())
           #input()
           counter = 0
           source_row = 0
           source_col = 0
           drop_phase = True
           b = copy.deepcopy(board)
           for i in range(5):
               for j in range(5):
                   if b[i][j] == self.my_piece:
                       counter = counter + 1
           if counter < 4:
               drop_phase = True
           else:
               drop_phase = False
                
           if drop_phase:     
               valid_locations = get_valid_locations(b)
               #print(valid_locations)
               if depth == 0:
                   return (None, None, heuristic_game_value(b), False)
               elif (self.game_value(b)) == 1 or (self.game_value(b) == -1):
                   if self.game_value(b) == 1 or self.game_value(b) == -1:
                       if heuristic_game_value(b) == 1:
                           return (None, None, 1, False)
                       elif heuristic_game_value(b) == -1:
                           return (None, None, -1, False)
               if max_player:
                   value = -1
                   row,col = random.choice(valid_locations)[0],[1]
                   #print("row" + str(row))
                   #print("col" + str(col))
                   r = 0
                   c = 0
                   for i in range(5):
                       for j in range(5):
                           if b[i][j] == ' ':
                               r = i
                               c = j
                               b_copy = copy.deepcopy(b)
                               move = [(r, c)]
                               b_copy = test_place(b, move, self.my_piece)
                               temp = minimax(b_copy, depth-1, alpha, beta, False)
                               new_score = temp[2]
                               if new_score >= value:
                                   value = new_score
                                   #print(value)
                                   row = r
                                   col = c
                               alpha = max(alpha, value)
                               if alpha >= beta:
                                   break
                   return row, col, value, drop_phase
               
               else: #Min Player
                   value = 1
                   row,col = random.choice(valid_locations)[0],[1]
                   r = 0
                   c = 0
                   for i in range(5):
                       for j in range(5):
                           if b[i][j] == ' ':
                               r = i
                               c = j
                               b_copy = copy.deepcopy(b)
                               move = [(r, c)]
                               b_copy = test_place(b, move, self.opp)
                               temp = minimax(b_copy, depth-1, alpha, beta, True)
                               new_score = temp[2]
                               if new_score <= value:
                                   value = new_score
                                   row = r
                                   col = c
                               beta = min(beta, value)
                               if alpha >= beta:
                                   break
                   return row, col, value, drop_phase

           if not drop_phase:
            # choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            #is valid location board[row][col] == 0
                valid_locations = get_valid_locations(b)
                if depth == 0:
                   return (None, None, heuristic_game_value(b), False)
                elif (self.game_value(b)) == 1 or (self.game_value(b) == -1):
                   if self.game_value(b) == 1 or self.game_value(b) == -1:
                       if heuristic_game_value(b) == 1:
                           return (None, None, 1, False)
                       elif heuristic_game_value(b) == -1:
                           return (None, None, -1, False)
                if max_player:
                    value = -1
                    row,col = random.choice(valid_locations)[0],[1]
                    for i in range(5):
                       for j in range(5):
                           if b[i][j] == ' ':
                                r = i
                                c = j
                                b_copy = copy.deepcopy(b)
                                for i in range(5):
                                    for j in range(5):
                                        if b[i][j] == self.my_piece:
                                            source_row = i
                                            source_col = j
                                            break
                                        break
                                move = [(r, c), (source_row, source_col)]
                                b_copy = test_place(b, move, self.my_piece)
                                temp = minimax(b_copy, depth-1, alpha, beta, False)
                                new_score = temp[2]
                                if new_score >= value:
                                    value = new_score
                                    row = r
                                    col = c
                                alpha = max(alpha, value)
                                if alpha >= beta:
                                    break
                    return row, col, value, drop_phase, source_row, source_col
               
                else: #Min Player
                    value = 1
                    row,col = random.choice(valid_locations)[0],[1]
                    for i in range(5):
                       for j in range(5):
                           if b[i][j] == ' ':
                               r = i
                               c = j
                               b_copy = copy.deepcopy(b)
                               for i in range(5):
                                   for j in range(5):
                                       if b[i][j] == self.opp:
                                           source_row = i
                                           source_col = j
                                           break
                                       break
                               move = [(r, c), (source_row, source_col)]
                               b_copy = test_place(b, move, self.opp)
                               temp = minimax(b_copy, depth-1, alpha, beta, True)
                               new_score = temp[2]
                               if new_score <= value:
                                   value = new_score
                                   row = r
                                   col = c
                               beta = min(beta, value)
                               if alpha >= beta:
                                   break
                    return row, col, value, drop_phase, source_row, source_col
        
        move = []             
        if (minimax(state, 3, 1, -1, True)[3]):
             result = minimax(state, 3, 1, -1, True)
             row = result[0]
             col = result[1]
             move.insert(0, (row,col))
        else:
            source_row = minimax(state, 3, 1, -1, True)[4]
            source_col = minimax(state, 3, 1, -1, True)[5]
            row = minimax(state, 3, 1, -1, True)[0]
            col = minimax(state, 3, 1, -1, True)[1]
            move.insert(0, (row,col))
            move.insert(1, (source_row, source_col))

            '''
            move = []
        (row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        return move
            '''
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
  
    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        #check \ diagonal wins
        #Case 1
        i = 1
        j = 0
        if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
            return 1 if state[i][j]==self.my_piece else -1
        #Case 2
        i = 0
        j = 0
        if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
            return 1 if state[i][j]==self.my_piece else -1
        #Case 3
        i = 1
        j = 1
        if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
            return 1 if state[i][j]==self.my_piece else -1
        #Case 4
        i = 0
        j = 1
        if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
            return 1 if state[i][j]==self.my_piece else -1
        #check / diagonal wins
        i = 0
        j = 3
        if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
            return 1 if state[i][j]==self.my_piece else -1
        i = 0
        j = 4
        if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
            return 1 if state[i][j]==self.my_piece else -1
        i = 1
        j = 3
        if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
            return 1 if state[i][j]==self.my_piece else -1
        i = 1
        j = 4
        if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
            return 1 if state[i][j]==self.my_piece else -1
        #check 2x2 box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row + 1][col] == state[row][col + 1] == state [row + 1][col + 1]:
                    return 1 if state[row][col]==self.my_piece else -1
        
        return 0 # no winner yet

    def evaluate_block(self, block, block1, piece):
        score = 0
        opp_piece = self.my_piece
        if piece == self.my_piece:
            opp_piece == self.opp
        if len(block1) == 0:    
            if block.count(piece) == 4:
                score += 100
            elif block.count(piece) == 3 and block.count(None) == 1:
                score += 85
            elif block.count(piece) == 2 and block.count(None) == 2:
                score += 30
            if block.count(opp_piece) == 3 and block.count(None) == 1:
                score -= 90
    
        else:
            if block.count(piece) + block1.count(piece) == 3:
                score += 50
            elif block.count(self.opp) + block1.count(self.opp) == 3:
                score -= 50
        return score
        

    def score_board(self, state, piece):
        score = 0
        block = []
        block1 = []
        ##Prefer center position
        #center_array = [int(i) for i in list(state[:][2])]
        center_array = []
        for i in range(5):
            center_array.append(state[i][2])
        center_count = center_array.count(piece)
        score += center_count * 100
            
        #Score Horizontal
        block = []
        row_array = []
        for r in range(5):
            for i in range(5):
                row_array.append(state[r][i])
            #row_array = [int(i) for i in list(state[r,:])]
            for c in range(2):
                block.append(row_array[c])
                block.append(row_array[c+1])
                block.append(row_array[c+2])
                block.append(row_array[c+3])
                score += self.evaluate_block(block, block1, piece)
        
        #Score Vertical
        block = []
        col_array = []
        for c in range(5):
            for i in range(5):
                col_array.append(state[i][c])
            for r in range(2):
                block.append(col_array[r])
                block.append(col_array[r+1])
                block.append(col_array[r+2])
                block.append(col_array[r+3])
                score += self.evaluate_block(block, block1, piece)
            
        #Score / diagonal
        block = []
        for r in range(2):
            for c in range(2):
                block = [state[r+i][c+i] for i in range (4)]
                score += self.evaluate_block(block, block1, piece)
        
        #Score \ diagonal
        block = []
        for r in range(2):
            for c in range(2):
                block = [state[r+3-i][c+i] for i in range (4)]
                score += self.evaluate_block(block, block1, piece)
        
        #Score 2x2 box
        row_array1 = []
        col_array1 = []
        block = []
        block1 = []
        for r in range(5):
            for i in range(2):
                row_array1.append(state[r][i])
            for c in range(5):
                for i in range(2):
                    col_array1.append(state[i][c])
                block.append(row_array1[r])
                block.append(row_array1[r+1])
                block1.append(col_array1[c])
                block1.append(col_array1[c+1])
                score += self.evaluate_block(block, block1, piece)
                
        return score/1000
        

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
        print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                 (int(move_from[1]), ord(move_from[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")
