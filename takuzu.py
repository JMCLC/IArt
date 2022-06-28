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
import time


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self,data,size):
        # self.data = data
        self.list = data
        self.size = size

    def __str__(self):
        res = ""
        for i in range(self.size):
            for j in range(self.size - 1):
            #     res += str(self.data[i][j]) + "\t"
            # res += str(self.data[i][self.size - 1]) + "\n"
                res += str(self.list[i][j]) + "\t"
            res += str(self.list[i][self.size - 1]) + "\n"
        return res

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return None
        return self.data[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if self.size == row + 1 :
            return (None, self.data[row - 1][col])
        elif row == 0:
            return (self.data[row + 1][col], None)
        else:
            return (self.data[row + 1][col],self.data[row - 1][col])

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if self.size == col + 1:
            return (self.data[row][col - 1],None)
        elif col == 0:
            return (None,self.data[row][col + 1])
        else:
            return (self.data[row][col - 1],self.data[row][col + 1])

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
        for i in range(1,mx+1):
            line = f[i].rstrip('\n')
            for j in range(0,len(line)):
                if line[j] == '\t':
                    pass
                else:
                    m = m + [int(line[j])]
        for k in range(0,len(m),mx):
            l.append(m[k:k + mx])

        return Board(np.array(l),mx)

    def columns(self):
        res = np.zeros_like(self.list)
        for i in range(self.size):
            for j in range(self.size):
                res[j][i] = self.list[i][j]
        return res


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(TakuzuState(board))
        pass
    
    def ammount_in_line_column(self, state: TakuzuState, line: int, column: int):
        num = state.board.size // 2
        num += state.board.size % num
        res = []
        if np.count_nonzero(state.board.list == 0, axis=1)[line] >= num:
            res.append(0)
        if np.count_nonzero(state.board.list == 1, axis=1)[line] >= num:
            res.append(1)
        if np.count_nonzero(state.board.list == 0, axis=0)[column] >= num:
            res.append(0)
        if np.count_nonzero(state.board.list == 1, axis=0)[column] >= num:
            res.append(1)
        res_set = set(res)
        if len(res_set) == 1:
            return res[0]
        elif len(res_set) == 2:
            return -1
        else:
            return 2

    def adjacents_in_line_column(self, state: TakuzuState, line: int, column: int):
        res = []
        if column < state.board.size - 2:
            if state.board.list[line][column + 1] == state.board.list[line][column + 2] and \
                    state.board.list[line][column + 1] != 2:
                res.append(state.board.list[line][column + 1])
        if 0 < column < state.board.size - 1:
            if state.board.list[line][column - 1] == state.board.list[line][column + 1] and \
                    state.board.list[line][column + 1] != 2:
                res.append(state.board.list[line][column + 1])
        if column > 1:
            if state.board.list[line][column - 1] == state.board.list[line][column - 2] and \
                    state.board.list[line][column - 1] != 2:
                res.append(state.board.list[line][column - 1])
        if line < state.board.size - 2:
            if state.board.list[line + 1][column] == state.board.list[line + 2][column] and \
                    state.board.list[line + 1][column] != 2:
                res.append(state.board.list[line + 1][column])
        if 0 < line < state.board.size - 1:
            if state.board.list[line - 1][column] == state.board.list[line + 1][column] and \
                    state.board.list[line + 1][column] != 2:
                res.append(state.board.list[line + 1][column])
        if line > 1:
            if state.board.list[line - 1][column] == state.board.list[line - 2][column] and \
                    state.board.list[line - 1][column] != 2:
                res.append(state.board.list[line - 1][column])
        res_set = set(res)
        if len(res_set) == 1:
            return res[0]
        elif len(res_set) == 2:
            return -1
        else:
            return 2
    
    def check_for_repeated_rows(self, state, line, column):
        for i in range(state.board.size - 1, -1, -1):
            if line != i:
                if np.sum(state.board.list[i] == state.board.list[line]) == state.board.size - np.count_nonzero(state.board.list[line] == 2):
                    if state.board.list[i][column] == 0:
                        return (line,column,1)
                    else:
                        return (line,column,0)
        return None

    def check_for_repeated_columns(self, state, line, column):
        columns = state.board.columns()
        for i in range(state.board.size - 1, -1, -1):
            if line != i:
                if np.sum(columns[i] == columns[line]) == state.board.size - np.count_nonzero(columns[line] == 2):
                    if columns[i][line] == 0:
                        return (line,column,1)
                    else:
                        return (line,column,0)
        return None

    def actions(self, state: TakuzuState):
        """Retorna uma lista de aÃ§Ãµes que podem ser executadas a
        partir do estado passado como argumento."""
        action_list = []
        for i in range(state.board.size - 1, -1, -1):
            for j in range(state.board.size - 1, -1, -1):
                if state.board.list[i][j] == 2:
                    x = self.ammount_in_line_column(state, i, j)
                    if x == -1:
                        return []
                    if x == 2:
                        y = self.adjacents_in_line_column(state, i, j)
                        if y == -1:
                            return []
                        if y == 2:
                            repetetion_r = self.check_for_repeated_rows(state, i, j)
                            repetetion_c = self.check_for_repeated_columns(state, i, j)
                            if repetetion_r != None:
                                action_list.append(repetetion_r)
                            elif repetetion_c != None:
                                action_list.append(repetetion_c)
                            else:
                                action_list.append((i, j, 0))
                                action_list.append((i, j, 1))
                        elif y == 1:
                            return [(i, j, 0)]
                        elif y == 0:
                            return [(i, j, 1)]
                    elif x == 1:
                        return [(i, j, 0)]
                    elif x == 0:
                        return [(i, j, 1)]
        if len(action_list) == 0:
            return []
        return [action_list[0], action_list[1]]

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        actions = self.actions(state)
        if action in actions:
            # state.board.data[action[0]][action[1]] = action[2]
            state.board.list[action[0]][action[1]] = action[2]
        return state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return False

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return np.count_nonzero(node.state.board.list == 2)

if __name__ == "__main__":
    start = time.time()
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)  
    if goal_node != None:
        print(goal_node.state.board, sep="")
    else:
        print(board, sep="")
    f = open("readme.txt", "w")
    f.write(board.__str__())
    f.close()
    end = time.time()
    print(end-start)
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass