from typing import Tuple

import numpy as np

from gym_neutreeko.game.common import const


class NeutreekoUtils:
    @staticmethod
    def search_sequence_numpy(arr, seq):
        """ Find sequence in an array using NumPy only.

        Parameters
        ----------
        arr    : input 1D array
        seq    : input 1D array

        Output
        ------
        Output : 1D Array of indices in the input array that satisfy the
        matching of input sequence in the input array.
        In case of no match, an empty list is returned.
        """

        # Store sizes of input array and sequence
        Na, Nseq = arr.size, seq.size

        # Range of sequence
        r_seq = np.arange(Nseq)

        # Create a 2D array of sliding indices across the entire length of input array.
        # Match up with the input sequence & get the matching starting indices.
        M = (arr[np.arange(Na-Nseq+1)[:,None] + r_seq] == seq).all(1)

        # Return true if the sequence exists
        return M.any() > 0

        # Get the range of those indices as final output
        # if M.any() > 0:
        #     return np.where(np.convolve(M, np.ones(Nseq, dtype=int)) > 0)[0]
        # else:
        #     return []         # No match found

    @staticmethod
    def find_sequence_board(board, sequence):
        """

        :param board:
        :param sequence:
        :return:
        """
        for i in range(len(board)):
            # Check in lines
            if NeutreekoUtils.search_sequence_numpy(board[i, :], sequence):
                return True
            # check in columns
            if NeutreekoUtils.search_sequence_numpy(board[:, i], sequence):
                return True

        # check victory in diagonals
        flipped_board = np.fliplr(board)
        for i in range(-2, 3):
            diagonal1 = np.diagonal(board, offset=i)
            if NeutreekoUtils.search_sequence_numpy(diagonal1, sequence):
                return True
            diagonal2 = np.diagonal(flipped_board, offset=i)
            if NeutreekoUtils.search_sequence_numpy(diagonal2, sequence):
                return True

        return False

    @staticmethod
    def value_in_board(board, coords: Tuple[int, int]):
        """
        Returns the value in the board

        :param board: A np array of size (5,5)
        :param coords: The x and y coordinates of a spot
        :return:
        """
        if (coords[0] < 0) | (coords[0] >= const.BOARD_SIZE) | (coords[1] < 0) | (coords[1] >= const.BOARD_SIZE):
            return False
        return board[coords[0], coords[1]]

    @staticmethod
    def replace_in_board(board, coords: Tuple[int, int], value: int):
        """
        Replaces a value in the board

        :param board: A np array of size (5,5)
        :param coords: The x and y coordinates of a spot
        :param value: the value to be in the board
        :return: None
        """
        if (coords[0] < 0) | (coords[0] >= const.BOARD_SIZE) | (coords[1] < 0) | (coords[1] >= const.BOARD_SIZE):
            return False
        board[coords[0], coords[1]] = value


class Reward:
    @staticmethod
    def method_1(move_type) -> int:
        CONST_REWARDS = {
            "win": 30,  # winning move
            # "2_row": 5,  # places 2 pieces together
            # "between": 2,  # gets in between 2 opponent pieces
            "default": -0.1  # makes a move (negative to not enforce unnecessary moves)
        }

        return CONST_REWARDS.get(move_type, -1)
