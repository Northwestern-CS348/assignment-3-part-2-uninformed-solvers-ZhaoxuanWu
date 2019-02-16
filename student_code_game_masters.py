from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # student code goes here
        disk_map = {}
        result = []
        for peg_num in range(1, 4):
            list_of_bindings = self.kb.kb_ask(parse_input('fact: (on ?disk peg' + str(peg_num) + ')'))
            temp = []
            if list_of_bindings:
                for bindings in list_of_bindings:
                    if bindings['?disk'] not in disk_map:
                        disk_map[bindings['?disk']] = int(bindings['?disk'][-1])
                    temp.append(disk_map[bindings['?disk']])
            temp.sort()
            result.append(tuple(temp))
        return tuple(result)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        game_state = self.getGameState()
        disk =  str(movable_statement.terms[0].term)
        init_peg = str(movable_statement.terms[1].term)
        init_peg_num = int(init_peg[-1])
        target_peg = str(movable_statement.terms[2].term)
        target_peg_num = int(target_peg[-1])

        if len(game_state[target_peg_num - 1]) > 0:
            # Some disk on the target peg initially
            # print("RETRACTING", parse_input('fact: (top disk' + str(game_state[target_peg_num - 1][0]) + ' ' + target_peg + ')'))
            self.kb.kb_retract(parse_input('fact: (top disk' + str(game_state[target_peg_num - 1][0]) + ' ' + target_peg + ')'))
        else:
            # There is no disk on the target peg initially
            # print("RETRACTING", parse_input('fact: (empty ' + target_peg + ')'))
            self.kb.kb_retract(parse_input('fact: (empty ' + target_peg + ')'))

        # Out of the initial peg
        # print("RETRACTING", parse_input('fact: (on ' + disk + ' ' + init_peg + ')'))
        self.kb.kb_retract(parse_input('fact: (on ' + disk + ' ' + init_peg + ')'))
        # No longer top the initial peg
        # print("RETRACTING", parse_input('fact: (top ' + disk + ' ' + init_peg + ')'))
        self.kb.kb_retract(parse_input('fact: (top ' + disk + ' ' + init_peg + ')'))
        # Now on the target peg
        # print("ADDING", parse_input('fact: (on ' + disk + ' ' + target_peg + ')'))
        self.kb.kb_add(parse_input('fact: (on ' + disk + ' ' + target_peg + ')'))
        # Now top the target peg
        # print("ADDING", parse_input('fact: (top ' + disk + ' ' + target_peg + ')'))
        self.kb.kb_add(parse_input('fact: (top ' + disk + ' ' + target_peg + ')'))
        if len(game_state[init_peg_num - 1]) > 1:
            # Some disk under the one moved
            # New top on the initial peg
            # print("ADDING", parse_input('fact: (top ' + 'disk' + str(game_state[init_peg_num - 1][1]) + ' ' + init_peg + ')'))
            self.kb.kb_add(
                parse_input('fact: (top disk' + str(game_state[init_peg_num - 1][1]) + ' ' + init_peg + ')'))
        else:
            # No disk under the one moved
            # print("ADDING", parse_input('fact: (empty ' + init_peg + ')'))
            self.kb.kb_add(parse_input('fact: (empty ' + init_peg + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        tile_map = {}
        result = []
        for y_coord in range(1, 4):
            temp = []
            for x_coord in range(1, 4):
                list_of_bindings = self.kb.kb_ask(parse_input('fact: (coord ?tile pos' + str(x_coord) + ' pos' + str(y_coord) +')'))
                if list_of_bindings:
                    for bindings in list_of_bindings:
                        if bindings['?tile'] not in tile_map:
                            if bindings['?tile'] == 'empty':
                                tile_map[bindings['?tile']] = -1
                            else:
                                tile_map[bindings['?tile']] = int(bindings['?tile'][-1])
                        temp.append(tile_map[bindings['?tile']])
            result.append(tuple(temp))
        return tuple(result)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        # print(self.getGameState())

        tile = str(movable_statement.terms[0].term)
        init_x = str(movable_statement.terms[1].term)
        init_y =  str(movable_statement.terms[2].term)
        target_x =  str(movable_statement.terms[3].term)
        target_y =  str(movable_statement.terms[4].term)

        # Retracting old coordinates
        # print('RETRACTING', parse_input('fact: (coord ' + tile + ' ' + init_x + ' ' + init_y + ')'))
        self.kb.kb_retract(parse_input('fact: (coord ' + tile + ' ' + init_x + ' ' + init_y + ')'))
        # print('RETRACTING', parse_input('fact: (coord empty ' + target_x + ' ' + target_y + ')'))
        self.kb.kb_retract(parse_input('fact: (coord empty ' + target_x + ' ' + target_y + ')'))

        # Adding new coordinates
        # print('ADDING', parse_input('fact: (coord empty ' + init_x + ' ' + init_y + ')'))
        self.kb.kb_add(parse_input('fact: (coord empty ' + init_x + ' ' + init_y + ')'))
        # print('ADDING', parse_input('fact: (coord ' + tile + ' ' + target_x + ' ' + target_y + ')'))
        self.kb.kb_add(parse_input('fact: (coord ' + tile + ' ' + target_x + ' ' + target_y + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
