# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 53:
# 99096 Jose Maria Cardoso
# 99233 Gustavo Diogo

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import numpy as np


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self,data,size):
        self.data = data
        self.size = size

    def __str__(self):
        res = ""
        for i in range(self.size):
            for j in range(self.size - 1):
                 res += str(self.data[i][j]) + "\t"
            res += str(self.data[i][self.size - 1]) + "\n"
        return res

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return None
        return self.data[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return (self.get_number(row + 1, col), self.get_number(row - 1, col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_number(row, col - 1), self.get_number(row, col + 1))

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        l = []
        m = []
        f = sys.stdin.readlines()
        mx = int(f[0])
        for i in range(1, mx+1):
            line = f[i].rstrip('\n')
            for j in range(0,len(line)):
                if line[j] != '\t':
                    m = m + [int(line[j])]
        for k in range(0, len(m), mx):
            l.append(m[k:k + mx])

        return Board(np.array(l),mx)

    def columns(self):
        return np.transpose(self.data)

    def check_filled_slots(self, row, column):
        half = 0
        columns = self.columns()
        one = False
        zero = False
        if self.size % 2 == 0:
            half += int(self.size / 2)
        else:
            half += int((self.size + 1) / 2)
        if np.count_nonzero(self.data[row] == 0) >= half or np.count_nonzero(columns[column] == 0) >= half:
            zero = True
        if np.count_nonzero(self.data[row] == 1) >= half or np.count_nonzero(columns[column] == 1) >= half:
            one = True
        if one and zero:
            return []
        elif one:
            return [(row, column, 0)]
        elif zero:
            return [(row, column, 1)]
        return None

    def check_adjacency(self, row, column):
        res = []
        if (self.get_number(row, column + 1) == self.get_number(row, column + 2) or \
            self.get_number(row, column + 1) == self.get_number(row, column - 1)) and \
            self.get_number(row, column + 1) not in (2, None):
            res.append(self.get_number(row, column + 1))
        if self.get_number(row, column - 1) == self.get_number(row, column - 2) and \
            self.get_number(row, column - 1) not in (2, None):
            res.append(self.get_number(row, column - 1))
        if (self.get_number(row + 1, column) == self.get_number(row + 2, column) or \
            self.get_number(row + 1, column) == self.get_number(row - 1, column)) and \
            self.get_number(row + 1, column) not in (2, None):
            res.append(self.get_number(row + 1, column))
        if self.get_number(row - 1, column) == self.get_number(row - 2, column) and \
            self.get_number(row - 1, column) not in (2, None):
            res.append(self.get_number(row - 1, column))
        if 0 in res and 1 in res:
            return []
        elif len(res) != 0:
            return [(row, column, int(abs(res[0] - 1)))]
        return None

class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(TakuzuState(board))
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        res = []
        for i in range(state.board.size - 1, -1, -1):
            for j in range(state.board.size - 1, - 1, - 1):
                if state.board.data[i][j] == 2:
                    slots_filled = state.board.check_filled_slots(i, j)
                    if slots_filled != None:
                        return slots_filled
                    adjacency_check = state.board.check_adjacency(i, j)
                    if adjacency_check != None:
                        return adjacency_check              
                    res.append((i, j, 0))
                    res.append((i, j, 1))
        if res != []:
            return [res[0], res[1]]
        return res

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        newBoard = Board(np.copy(state.board.data), state.board.size)
        newBoard.data[action[0]][action[1]] = action[2]
        return TakuzuState(newBoard)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        if np.count_nonzero(state.board.data == 2) > 0 or \
            np.unique(state.board.data, axis = 0).size != state.board.size ** 2 or \
            np.unique(state.board.columns(), axis = 0).size != state.board.size ** 2 :
            return False
        for i in range(state.board.size - 1, -1, -1):
            for j in range(state.board.size - 1, -1, -1):
                if (state.board.get_number(i, j) == state.board.get_number(i, j - 1) == state.board.get_number(i, j - 2) and \
                    state.board.get_number(i, j) != None) or\
                    (state.board.get_number(i, j) == state.board.get_number(i - 1, j) == state.board.get_number(i - 2, j) and \
                    state.board.get_number(i, j) != None):
                    return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return np.count_nonzero(node.state.board.data == 2)

if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board, end="")
    pass