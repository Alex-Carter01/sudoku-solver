import math

def isSquare(n):
    ## Trivial checks
    if type(n) != int:  ## integer
        return False
    if n < 0:      ## positivity
        return False
    if n == 0:      ## 0 pass
        return True

    ## Reduction by powers of 4 with bit-logic
    while n&3 == 0:    
        n=n>>2

    ## Simple bit-logic test. All perfect squares, in binary,
    ## end in 001, when powers of 4 are factored out.
    if n&7 != 1:
        return False

    if n==1:
        return True  ## is power of 4, or even power of 2


    ## Simple modulo equivalency test
    c = n%10
    if c in {3, 7}:
        return False  ## Not 1,4,5,6,9 in mod 10
    if n % 7 in {3, 5, 6}:
        return False  ## Not 1,2,4 mod 7
    if n % 9 in {2,3,5,6,8}:
        return False  
    if n % 13 in {2,5,6,7,8,11}:
        return False  

    ## Other patterns
    if c == 5:  ## if it ends in a 5
        if (n//10)%10 != 2:
            return False    ## then it must end in 25
        if (n//100)%10 not in {0,2,6}: 
            return False    ## and in 025, 225, or 625
        if (n//100)%10 == 6:
            if (n//1000)%10 not in {0,5}:
                return False    ## that is, 0625 or 5625
    else:
        if (n//10)%4 != 0:
            return False    ## (4k)*10 + (1,9)


    ## Babylonian Algorithm. Finding the integer square root.
    ## Root extraction.
    s = (len(str(n))-1) // 2
    x = (10**s) * 4

    A = {x, n}
    while x * x != n:
        x = (x + (n // x)) >> 1
        if x in A:
            return False
        A.add(x)
    return True

#backtracking
#DFS

class Sudoko:
	def __init__(self, board):
		self.solved = False
		self.n = len(board)
		
		if not isSquare(self.n):
			print("Invalid Board")

		for row in board:
			if self.n != len(row):
				print("Invalid Board")
		
		self.secsize = math.sqrt(self.n)
		self.board = board
		self.rowset = [set() for i in range(self.n)]
		self.colset = [set() for i in range(self.n)]
		self.secset = [set() for i in range(self.n)]

		# initialize rowset, colset, section set
		for row in range(self.n):
			for col in range(self.n):
				val = self.board[row][col]
				if val != 0:
					self.colset[col].add(val)
					self.rowset[row].add(val)
					self.secset[self.getSectionNum(row, col)].add(val)

		self.printStuff()	

	def getSectionNum(self, row, col):
		return int(int(row/self.secsize) * self.secsize + int(col/self.secsize))

	def printStuff(self):
		print("Board:")
		for row in self.board:
			print(row)
		"""
		print("Rows:")
		for r in self.rowset:
			print(r)
		print("Columns:")
		for c in self.colset:
			print(c)
		print("Sections:")
		for s in self.secset:
			print(s)
		"""
		

	def isPromising(self, row, col, val):
		if self.board[row][col] != 0: # maybe unnecissary
			return False

		if val in self.rowset[row]:
			return False

		if val in self.colset[col]:
			return False

		if val in self.secset[self.getSectionNum(row, col)]:
			return False

		return True

	def isSolution(self):
		if self.solved:
			return True

		for row in self.rowset:
			if len(row) != self.n:
				return False

		for col in self.colset:
			if len(col) != self.n:
				return False

		print("solution found!")
		self.printStuff()
		self.solved = True
		return True

	def nextLoc(self, row, col):
		if col == self.n -1:
			if row == self.n - 1:
				return -1, -1
			return row + 1, 0
		return row, col + 1

	def checkNode(self, row, col):
		if self.isSolution():
			return

		if row and col == -1:
			print("no possible solution")
			return

		for guess in range(1, self.n + 1): # 9
			if self.board[row][col] != 0:
				next_row, next_col = self.nextLoc(row, col)

				# make recursive call
				self.checkNode(next_row, next_col)

			elif self.isPromising(row, col, guess):
				# make guess
				self.board[row][col] = guess
				self.rowset[row].add(guess)
				self.colset[col].add(guess)

				# make recursive call
				next_row, next_col = self.nextLoc(row, col)
				self.checkNode(next_row, next_col)

				# undo this guess
				self.board[row][col] = 0
				self.rowset[row].remove(guess)
				self.colset[col].remove(guess)

	def solve(self):
		self.checkNode(0,0)

graph = [
 [0,0,0,2,6,0,7,0,1],
 [6,8,0,0,7,0,0,9,0],
 [1,9,0,0,0,4,5,0,0],
 [8,2,0,1,0,0,0,4,0],
 [0,0,4,6,0,2,9,0,0],
 [0,5,0,0,0,3,0,2,8],
 [0,0,9,3,0,0,0,7,4],
 [0,4,0,0,5,0,0,3,6],
 [7,0,3,0,1,8,0,0,0]]

s = Sudoko(graph)
s.solve()

#----

#stochastic - annealing, genteic, tabu

#constraint problem

#constraint + backtracking

#exact cover
#knuth algX or gauss elimnation

#allow n to be scale-able