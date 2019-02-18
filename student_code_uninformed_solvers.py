
from solver import *
import queue

# THIS VERSION IS TOO SLOW
# -----------------------------------------------------------------------------
# class SolverDFS(UninformedSolver):
#     def __init__(self, gameMaster, victoryCondition):
#         super().__init__(gameMaster, victoryCondition)
#         self.stack = []
#
#     def solveOneStep(self):
#         """
#         Go to the next state that has not been explored. If a
#         game state leads to more than one unexplored game states,
#         explore in the order implied by the GameMaster.getMovables()
#         function.
#         If all game states reachable from a parent state has been explored,
#         the next explored state should conform to the specifications of
#         the Depth-First Search algorithm.
#
#         Returns:
#             True if the desired solution state is reached, False otherwise
#         """
#
#         print("CURRENNNTTSTATE", self.gm.getGameState())
#
#         if self.currentState not in self.visited:
#             # This is only trigger on the first step of the whole solver
#             self.visited[self.currentState] = True
#
#         while True:
#             movables = self.gm.getMovables()
#             print('movvvables', movables)
#             # Arrive at a state, first add the possible branches to queue
#             if movables and not self.currentState.children:
#                 # New GameState reached, create GameStates
#                 for move in reversed(movables):
#                     self.gm.makeMove(move)
#                     new_state_tuple = self.gm.getGameState()
#                     if self.currentState.parent and new_state_tuple == self.currentState.parent.state:
#                         # This particular move is reversing a move
#                         # print("SKIPPP")
#                         self.gm.reverseMove(move)
#                         continue
#                     else:
#                         # This particular move result in new states, append it to currentState's children
#                         new_game_state = GameState(new_state_tuple, self.currentState.depth + 1, move)
#                         new_game_state.parent = self.currentState
#                         self.currentState.children.append(new_game_state)
#                         self.stack.append(new_game_state)
#                         self.gm.reverseMove(move)
#
#             # Get the next state to reach
#             # print('SIZEEEEEEE', self.queue.qsize())
#             next_state = self.stack.pop()
#             # print(next_state.state)
#
#             if next_state in self.visited:
#                 # This state already visited
#                 # print(new_game_state.state, "VISTIEDDDDDDDDDDDDDDDDDDDDD")
#                 continue
#
#             steps_to_new_state_from_root = []
#             while self.currentState.requiredMovable:
#                 # Reverse till the root
#                 print("Reveresinggg", self.currentState.requiredMovable)
#                 self.gm.reverseMove(self.currentState.requiredMovable)
#                 self.currentState = self.currentState.parent
#             while next_state.requiredMovable:
#                 steps_to_new_state_from_root.append(next_state.requiredMovable)
#                 next_state = next_state.parent
#             while steps_to_new_state_from_root:
#                 move = steps_to_new_state_from_root.pop()
#                 print('making_move', move)
#                 self.gm.makeMove(move)
#                 new_state_tuple = self.gm.getGameState()
#                 for child in self.currentState.children:
#                     if child.state == new_state_tuple:
#                         self.currentState = child
#                         self.visited[self.currentState] = True
#                         break
#             break
#
#         if self.currentState.state == self.victoryCondition:
#             return True
#         print("WRONGGGGGGGGGG", self.currentState.state, self.victoryCondition)
#         return False
# -----------------------------------------------------------------------------


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True

        # print("CURRENNNTTSTATE", self.gm.getGameState())
        movables = self.gm.getMovables()
        # print('movvvables', movables)

        if movables and not self.currentState.children:
            # New GameState reached, create GameStates
            for move in movables:
                self.gm.makeMove(move)
                new_state_tuple = self.gm.getGameState()
                if self.currentState.parent and new_state_tuple == self.currentState.parent.state:
                    # print("SKIP")
                    # This particular move is reversing a move
                    self.gm.reverseMove(move)
                    continue
                else:
                    # This particular move result in new states, append it to currentState's children
                    new_game_state = GameState(new_state_tuple, self.currentState.depth + 1, move)
                    new_game_state.parent = self.currentState
                    self.currentState.children.append(new_game_state)
                    # print('before reverse', self.gm.getGameState())
                    self.gm.reverseMove(move)
                    # print('after reverse', self.gm.getGameState())

        if movables and self.currentState.children:
            # Previously added GameState reached, follow DFS
            flag = True
            while flag:
                if not self.currentState.parent and self.currentState.nextChildToVisit == len(self.currentState.children):
                    # Searched all
                    flag = False
                if self.currentState.nextChildToVisit < len(self.currentState.children):
                    # Still left children unvisited
                    if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                        # Such GameState never encountered before, make the move
                        self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
                        self.currentState.parent.nextChildToVisit = self.currentState.parent.nextChildToVisit + 1
                        self.visited[self.currentState] = True
                        print("Inserting", self.currentState.state)
                        print("MAKE_MOVE")
                        self.gm.makeMove(self.currentState.requiredMovable)
                        flag = False
                    else:
                        # For some GameState already encountered, do not go into infinite loops
                        self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
                        continue
                else:
                    # All children visited, reverse one depth up
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent
                    continue

        print("WRONGGGGGGGGGG", self.currentState.state, self.victoryCondition)
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = queue.Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.currentState.state == self.victoryCondition:
            return True

        print("CURRENNNTTSTATE", self.gm.getGameState())

        if self.currentState not in self.visited:
            # This is only trigger on the first step of the whole solver
            self.visited[self.currentState] = True

        while True:
            movables = self.gm.getMovables()
            # print('movvvables', movables)
            # Arrive at a state, first add the possible branches to queue
            if movables and not self.currentState.children:
                # New GameState reached, create GameStates
                for move in movables:
                    self.gm.makeMove(move)
                    new_state_tuple = self.gm.getGameState()
                    if self.currentState.parent and new_state_tuple == self.currentState.parent.state:
                        # This particular move is reversing a move
                        # print("SKIPPP")
                        self.gm.reverseMove(move)
                        continue
                    else:
                        # This particular move result in new states, append it to currentState's children
                        new_game_state = GameState(new_state_tuple, self.currentState.depth + 1, move)
                        new_game_state.parent = self.currentState
                        self.currentState.children.append(new_game_state)
                        self.queue.put(new_game_state)
                        self.gm.reverseMove(move)

            # Get the next state to reach
            # print('SIZEEEEEEE', self.queue.qsize())
            next_state = self.queue.get()
            # print(next_state.state)

            if next_state in self.visited:
                # This state already visited
                # print(new_game_state.state, "VISTIEDDDDDDDDDDDDDDDDDDDDD")
                continue

            steps_to_new_state_from_root = []
            while self.currentState.requiredMovable:
                # Reverse till the root
                # print("Reveresinggg", self.currentState.requiredMovable)
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
            while next_state.requiredMovable:
                steps_to_new_state_from_root.append(next_state.requiredMovable)
                next_state = next_state.parent
            while steps_to_new_state_from_root:
                move = steps_to_new_state_from_root.pop()
                # print('making_move', move)
                self.gm.makeMove(move)
                new_state_tuple = self.gm.getGameState()
                for child in self.currentState.children:
                    if child.state == new_state_tuple:
                        self.currentState = child
                        self.visited[self.currentState] = True
                        break
            break

        print("WRONGGGGGGGGGG", self.currentState.state, self.victoryCondition)
        return False
