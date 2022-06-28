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

        return Board(l,mx)

    def columns(self):
        res = [[0 for i in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                res[j][i] = self.data[i][j]
        return res

    def countAdjacent(self, i, j):
        vertical_values = self.adjacent_vertical_numbers(i, j)
        horizontal_values = self.adjacent_horizontal_numbers(i, j)
        count = [0, 0]
        for i in range(len(vertical_values)):
            if vertical_values[i] == 0 or horizontal_values[i] == 0:
                count[0] += 1
            elif vertical_values[i] == 1 or horizontal_values[i] == 1:
                count[1] += 1
        return count

    def equalArray(self, array):
        res = []
        for i in range(self.size):
            currentMissing = 2
            for j in range(self.size):
                if (array[j] != 2 and array[j] != self.data[i][j]) or self.data[i][j] == 2:
                    break
                elif array[j] == 2:
                    currentMissing = self.data[i][j]
                elif j == self.size - 1:
                    res.append((True, currentMissing))
        return res
    
    def check_column_and_row(self, row, col):
        columns = self.columns()     
        rowCount = countArray(self.data[row])
        columnCount = countArray(columns[col])
        half_cond = self.size / 2
        if self.size % 2 != 0:
            half_cond += 1
        if rowCount[0] == half_cond or columnCount[0] == half_cond:
            return 1
        elif rowCount[1] == half_cond or columnCount[1] == half_cond:
            return 0
        return None

    def check_row_adjacency(self, i, j):
        if self.get_number(i, j - 1) == self.get_number(i, j + 1) == 0 or \
            self.get_number(i, j - 2) == self.get_number(i, j - 1) == 0 or \
                self.get_number(i, j + 1) == self.get_number(i, j + 2) == 0 :
            return 1
        elif self.get_number(i, j - 1) == self.get_number(i, j + 1) == 1 or \
            self.get_number(i, j - 2) == self.get_number(i, j - 1) == 1 or \
                self.get_number(i, j + 1) == self.get_number(i, j + 2) == 1 :
            return 0
        return None

    def check_complete_row_adjacency(self, i, j):
        if self.get_number(i, j - 1) == self.get_number(i, j) == self.get_number(i, j + 1) == 0 or \
            self.get_number(i, j - 2) == self.get_number(i, j - 1) == self.get_number(i, j) == 0 or \
                self.get_number(i, j) == self.get_number(i, j + 1) == self.get_number(i, j + 2) == 0 :
            return 1
        elif self.get_number(i, j - 1) == self.get_number(i, j) == self.get_number(i, j + 1) == 1 or \
            self.get_number(i, j - 2) == self.get_number(i, j - 1) == self.get_number(i, j) == 1 or \
                self.get_number(i, j) == self.get_number(i, j + 1) == self.get_number(i, j + 2) == 1 :
            return 0
        return None

    def check_column_adjacency(self, i, j):
        if self.get_number(i - 1, j) == self.get_number(i, j) == self.get_number(i + 1, j) == 0 or \
            self.get_number(i - 2, j) == self.get_number(i - 1, j) == self.get_number(i, j) == 0 or \
                self.get_number(i, j) == self.get_number(i + 1, j) == self.get_number(i + 2, j) == 0 :
            return 1
        elif self.get_number(i - 1, j) == self.get_number(i, j) == self.get_number(i + 1, j) == 1 or \
            self.get_number(i - 2, j) == self.get_number(i - 1, j) == self.get_number(i, j) == 1 or \
                self.get_number(i, j) == self.get_number(i + 1, j) == self.get_number(i + 2, j) == 1 :
            return 0
        return None

    def check_complete_column_adjacency(self, i, j):
        if self.get_number(i - 1, j) == self.get_number(i, j) == self.get_number(i + 1, j) == 0 or \
            self.get_number(i - 2, j) == self.get_number(i - 1, j) == self.get_number(i, j) == 0 or \
                self.get_number(i, j) == self.get_number(i + 1, j) == self.get_number(i + 2, j) == 0 :
            return 1
        elif self.get_number(i - 1, j) == self.get_number(i, j) == self.get_number(i + 1, j) == 1 or \
            self.get_number(i - 2, j) == self.get_number(i - 1, j) == self.get_number(i, j) == 1 or \
                self.get_number(i, j) == self.get_number(i + 1, j) == self.get_number(i + 2, j) == 1 :
            return 0
        return None

    def equalCompleteRowArray(self, array, index):
        for i in range(self.size):
            for j in range(self.size):
                if self.get_number(i, j) != array[j]:
                    break
                elif j == self.size - 1 and self.get_number(i, j) == array[j] and i != index:
                    return True
        return False

    def equalCompleteColumnArray(self, array, index):
        columns = self.columns()
        for i in range(self.size):
            for j in range(self.size):
                if columns[i][j] != array[j]:
                    break
                elif j == self.size - 1 and columns[i][j] == array[j] and i != index:
                    return True
        return False
    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(TakuzuState(board))
        pass
    
    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        for i in range(state.board.size):
            for j in range(state.board.size):
                if state.board.get_number(i, j) == 2:
                    half_cond = state.board.check_column_and_row(i, j)
                    if half_cond != None:
                        # actions.append((i, j, half_cond))
                        return [(i, j, half_cond)]
                        # continue
                    row_adjacency = state.board.check_row_adjacency(i, j)
                    if row_adjacency != None:
                        return [(i, j, row_adjacency)]
                        # actions.append((i, j, row_adjacency))
                        # continue
                    column_adjacency = state.board.check_column_adjacency(i, j)
                    if column_adjacency != None:
                        return [(i, j, column_adjacency)]
                        # actions.append((i, j, column_adjacency))
                        # continue
                    # if countArray(state.board.data[i])[2] == 1:
                    #     equalRow = state.board.equalArray(state.board.data[i])
                    #     if (True, 0) in equalRow:
                    #         # actions.append((i, j, 1))
                    #         return [(i, j, 1)]
                    #         # continue
                    #     if (True, 1) in equalRow:
                    #         # actions.append((i, j, 0))
                    #         return [(i, j, 0)]
                    #         # continue
                    # elif countArray(state.board.columns()[j])[2] == 1:
                    #     equalCollumn = state.board.equalArray(state.board.columns()[j])
                    #     if (True, 0) in equalCollumn:
                    #         return [(i, j, 1)]
                    #         # actions.append((i, j, 0))
                    #         # continue
                    #     if (True, 1) in equalCollumn:
                    #         return [(i, j, 0)]
                    #         # actions.append((i, j, 1))
                    #         # continue                  
                    actions.append((i, j, 0))
                    actions.append((i, j, 1))
        return actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        actions = self.actions(state)
        if action in actions:
            state.board.data[action[0]][action[1]] = action[2]
        return state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        for i in range(state.board.size):
            for j in range(state.board.size):
                half_cond = state.board.check_column_and_row(i, j)
                row_adjacency = state.board.check_complete_row_adjacency(i, j)
                column_adjacency = state.board.check_complete_column_adjacency(i, j)
                if half_cond == None:
                    return False
                if row_adjacency != None:
                    return False
                if column_adjacency != None:
                    return False
                if state.board.get_number(i, j) == 2:
                    return False
                if state.board.equalCompleteRowArray(state.board.data[i], i):
                    return False
                if state.board.equalCompleteColumnArray(state.board.columns()[i], i):
                    return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return len(self.actions(node.state))

    # TODO: outros metodos da classe

def countArray(array):
    count = [0, 0, 0]
    for i in range(len(array)):
        if array[i] == 0:
            count[0] += 1
        elif array[i] == 1:
            count[1] += 1
        else:
            count[2] += 1
    return count

if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    #goal_node = astar_search(problem)
    goal_node = depth_first_tree_search(problem)
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass