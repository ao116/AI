import timeit
class CustomKakuroSolver:
    def __init__(self, puzzle):
        self.board = puzzle
        self.score_board = puzzle
    
    def imroved_find_empty_cell(self):
        max=self.find_max_constraint()
        if(max[3]=="row"):
            row , col = self.east_constraint_cell(max[1],max[2])
            for j in range(max[2]+1,col):
                if(self.is_empty_cell(row,j)):
                    return row, j

        if(max[3]=="col"):
            row , col = self.south_constraint_cell(max[1],max[2])
            for j in range(max[1]+1,row):
                if(self.is_empty_cell(j,col)):
                    return j, col
        return None, None        
    
    def find_max_constraint(self):
        max=[0,0,0," "]
        for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if(self.is_constraint_cell(i,j)):
                        if(self.board[i][j][0]>max[0] and not self.is_full_col(i+1,j)):
                            max[0]=self.board[i][j][0]
                            max[1]=i
                            max[2]=j
                            max[3]="col"
                        if(self.board[i][j][1]>max[0] and not self.is_full_row(i,j+1)):
                            max[0]=self.board[i][j][1]
                            max[1]=i
                            max[2]=j
                            max[3]="row"   
        return max                     




    



    def is_obstacle(self, row, col):
        return self.board[row][col] == "o"

    def is_empty_cell(self, row, col):
        return self.board[row][col] == "-"

    def is_constraint_cell(self, row, col):
        if (isinstance(self.board[row][col],list)):
            return True
        return False

    def find_empty_cell(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.is_empty_cell(row, col):
                    return row, col
        return None, None

    def west_constraint_cell(self, row, col):
        for i in range(col, -1, -1):
            if self.is_constraint_cell(row, i):
                return row, i
        #return None, None

    def east_constraint_cell(self, row, col):
        i, j = self.west_constraint_cell(row, col)
        for k in range(j + 1, len(self.board)):
            if self.is_constraint_cell(row, k):
                return row, k
        return row, len(self.board[row])

    def north_constraint_cell(self, row, col):
        for i in range(row, -1, -1):
            if self.is_constraint_cell(i, col):
                return i, col
        return None, None

    def south_constraint_cell(self, row, col):
        i, j = self.north_constraint_cell(row, col)
        for k in range(i + 1, len(self.board)):
            if self.is_constraint_cell(k, col):
                return k, col
        return len(self.board), col

    def used_in_row(self, row, col, num):
        i, j = self.west_constraint_cell(row, col)
        ii, jj = self.east_constraint_cell(row, col)
        for c in range(j + 1, jj):
            if self.board[row][c] == num:
                return True
        return False

    def used_in_col(self, row, col, num):
        i, j = self.north_constraint_cell(row, col)
        ii, jj = self.south_constraint_cell(row, col)
        for r in range(i + 1, ii):
            if self.board[r][col] == num:
                return True
        return False

    def sum_of_row(self, row, col):
        total_sum = 0
        i, j = self.west_constraint_cell(row, col)
        ii, jj = self.east_constraint_cell(row, col)
        for c in range(j + 1, jj):
            if isinstance(self.board[row][c], int):
                total_sum += int(self.board[row][c])
        return total_sum

    def sum_of_col(self, row, col):
        total_sum = 0
        i, j = self.north_constraint_cell(row, col)
        ii, jj = self.south_constraint_cell(row, col)
        for r in range(i + 1, ii):
            if isinstance(self.board[r][col], int):
                total_sum += int(self.board[r][col])
        return total_sum

    def num_of_row(self, row, col):
        i, j = self.west_constraint_cell(row, col)
        context = self.board[i][j]
        last_two_chars = context[1]#int(context[-2:])
        return last_two_chars

    def num_of_col(self, row, col):
        i, j = self.north_constraint_cell(row, col)
        context = self.board[i][j]
        first_two_chars = context[0]#int(context[:2])
        return first_two_chars

    def is_full_row(self, row, col):
        i, j = self.west_constraint_cell(row, col)
        ii, jj = self.east_constraint_cell(row, col)
        for c in range(j + 1, jj):
            if self.is_empty_cell(row, c):
                return False
        return True

    def is_full_col(self, row, col):
        i, j = self.north_constraint_cell(row, col)
        ii, jj = self.south_constraint_cell(row, col)
        for r in range(i + 1, ii):
            if self.is_empty_cell(r, col):
                return False
        return True

    def is_safe(self, row, col, num):
        self.board[row][col] = num
        if (self.is_full_row(row, col) and self.num_of_row(row, col) != self.sum_of_row(row, col)):
            self.board[row][col] = "-"
            return False
        if (self.is_full_col(row, col) and self.num_of_col(row, col) != self.sum_of_col(row, col)):
            self.board[row][col] = "-"
            return False
        self.board[row][col] = "-"
        if (self.used_in_row(row, col, num) or self.used_in_col(row, col, num)):
            return False
        return True

    def solve_puzzle(self):
        row, col = self.find_empty_cell()
        #row, col = self.imroved_find_empty_cell()
        if row is None:
            return True
        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                if self.solve_puzzle():
                    return True
                self.board[row][col] = "-"
        return False
    
    def improve_solve_puzzle(self):
        #row, col = self.find_empty_cell()
        check=0
        if(check==0):
            row, col = self.imroved_find_empty_cell()
        check=1
        row, col = self.find_empty_cell()


        if row is None:
            return True
        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                if self.solve_puzzle():
                    return True
                self.board[row][col] = "-"
        return False

    def print_solution(self):
        if (self.solve_puzzle()):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    text=str(self.board[i][j])
                    print(f"{text:<8}" , end=" ")
                print()
        else:
            print("No solution exists")
    def improved_print_solution(self):
        if (self.improve_solve_puzzle()):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    text=str(self.board[i][j])
                    print(f"{text:<8}" , end=" ")
                print()
        else:
            print("No solution exists")        


    #def improved_finder(self):

    
#chosing sample from link below
#https://www.puzzles-to-print.com/number-puzzles/PDFs/easy-kakuro.pdf
sample = [["o"    ,"o"    ,[30,-1],[4,-1],[24,-1],"o"     ,[4,-1] ,[16,-1]],
                ["o"    ,[16,19],"-"    ,"-"    ,"-"    ,[9,10] ,"-"    ,"-"    ],
                [[-1,39],"-"    ,"-"    ,"-"    ,"-"    ,"-"    ,"-"    ,"-"    ],
                [[-1,15],"-"    ,"-"    ,[23,10],"-"    ,"-"    ,[10,-1],"o"    ],
                ["o"    ,[-1,16],"-"    ,"-"    ,[6,4]  ,"-"    ,"-"    ,[16,-1]],
                ["o"    ,[14,-1],[16,9] ,"-"    ,"-"    ,[4,12] ,"-"    ,"-"    ],
                [[-1,35],"-"    ,"-"    ,"-"    ,"-"    ,"-"    ,"-"    ,"-"    ],
                [[-1,16],"-"    ,"-"    ,[-1,7] ,"-"    ,"-"    ,"-"    ,"o"    ],
                ]

#SamplePuzze
test = CustomKakuroSolver(sample)

start = timeit.default_timer()
test.print_solution()
stop = timeit.default_timer()
print("simple :" ,stop - start)


test2 = CustomKakuroSolver(sample)

start = timeit.default_timer()
test2.improved_print_solution()
stop = timeit.default_timer()
print("advanced :" ,stop - start)
