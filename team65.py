import sys
import random
import signal
import copy
import time
import pdb
import simulator

class Player65():
	def __init__(self):
		self.win_pos = [
        (0,1,2,3),(4,5,6,7),(8,9,10,11),(12,13,14,15),
        (0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15),
        (0,5,10,15),(3,6,9,12)
        ]
		# pdb.set_trace()
	        self.max_depth = 4
	        self.heur_val = []
	        for i in range(4):
			    new = []
			    for j in range(4):
				    new.append(0)
			    self.heur_val.append(new)
		#print self.heur_val[2][2]
		#print type(self.heur_val[0])

	def move(self, board, old_move, flag):
	    if old_move == (-1,-1):
			self.heur_val[1][1] = 0.3
			return (4,4)
            #print 'poiii'
	    temp_block = copy.deepcopy(board.block_status)
            temp_board = copy.deepcopy(board.board_status)
	    x = old_move[0]/4
	    y = old_move[1]/4
	    bl = x*4+y
	    # print bl
	    self.heur_val[x][y] = self.heuristic(temp_board, bl, flag)/1000.00
  	    #print 'vegeta'

	    cell = self.balphabeta(temp_board, temp_block, flag, flag, 0, -100000, 100000, old_move)
	    #print 'goku'
	    #print cell, flag
	    return cell

	def eval_board(self):
		overall_sum = 0
		#horizontal
		#print type(self.heur_val[0])
		lsum = 0
		for i in range(3):
			rowsum = 0
			for j in range(3):
				rowsum+=self.heur_val[i][j]
			x = 1
			flag = 0
			if rowsum < 0:
				flag = 1
				rowsum = -rowsum
			while rowsum>0:
				if rowsum>=1:
					lsum+=1*(x-(x/10))
				else:
					lsum+=rowsum*(x-(x/10))
				x*=10
				rowsum-=1
			if flag == 1:
				lsum = -lsum
			overall_sum += lsum

		#vertical
		lsum = 0
		for i in range(3):
			colsum = 0
			for j in range(3):
				colsum+=self.heur_val[j][i]
			x = 1
			flag = 0
			if colsum < 0:
				flag = 1
				colsum = -colsum
			while colsum>0:
				if colsum>=1:
					lsum+=1*(x-(x/10))
				else:
					lsum+=colsum*(x-(x/10))
				x*=10
				colsum-=1
			if flag == 1:
				lsum = -lsum
			overall_sum += lsum

		#diagonal
		diasum=0
		diasum += self.heur_val[0][0]
		diasum += self.heur_val[1][1]
		diasum += self.heur_val[2][2]
		x = 1
		flag = 0
		if diasum < 0:
			flag = 1
			diasum = -diasum
		lsum = 0
		while diasum>0:
			if diasum>=1:
				lsum+=1*(x-(x/10))
			else:
				lsum+=diasum*(x-(x/10))
			x*=10
			diasum-=1
		if flag == 1:
			lsum = -lsum
		overall_sum += lsum



		diasum=0
		diasum += self.heur_val[2][0]
		diasum += self.heur_val[1][1]
		diasum += self.heur_val[0][2]
		x = 1
		flag = 0
		if diasum < 0:
			flag = 1
			diasum = -diasum
		lsum = 0
		while diasum>0:
			if diasum>=1:
				lsum+=1*(x-(x/10))
			else:
				lsum+=diasum*(x-(x/10))
			x*=10
			diasum-=1
		if flag == 1:
			lsum = -lsum
		overall_sum += lsum

		# for i in range(3):
		# 	for j in range(3):
		# 		print self.heur_val[i][j],
		# 	print
		# print overall_sum

		return overall_sum

	def balphabeta(self, board, block, flag, turn, depth, a, b, old_move):
		if depth == 4:
			return self.eval_board()
			#return random.randrange(200) - 100

		if turn == 'x':
			oturn = 'o'
		else:
			oturn = 'x'
		blk_stat = []
		for i in range(0,4):
	   	    for j in range(0,4):
			blk_stat.append(block[i][j])
	        #print 'kl'
		valid_blocks = self.blocks_allowed(old_move, blk_stat)
	        #print 'asds'
		#print valid_blocks
		#print 'valid'
		tboard = [row[:] for row in board]
		tblock = block[:]
		free = False
		#print 'false'
		#pdb.set_trace()
		if len(valid_blocks) == 0:
			#print 'dlksakds'
			#print 'len'
			#pdb.set_trace()
			free = True
			for i in range(16):
				if blk_stat[i] == '-':
					valid_blocks.append(i)
			#print valid_blocks
		#print 'loop'
		if free == True:
			j = 0
			for j in range(2):
				minb = -1000
				for bl in valid_blocks:
					mvs = self.alphabeta(tboard, bl, turn, turn, 0, -100000, 100000)
					#print 'mvs value'
					#print mvs
					maxh = -100000
					if len(mvs) > 1:
						for mv in mvs:
							h = self.findh(mv, block, board, flag, bl)
							if h > maxh:
								maxh = h
								bmove = mv
						mv = bmove
					else:
						mv = mvs[0]

					tboard[mv[0]][mv[1]] = turn
					x = bl/4
					y = bl%4
					a = self.heur_val[x][y]
					hb = self.heuristic(tboard, bl, flag)/100.00
					#hb = self.eval_board()
					if hb >	 minb:
						minb = hb
						move = mv
					self.heur_val[x][y] = a
					tboard[mv[0]][mv[1]] = '-'
				if j == 0:
					pval = minb
					pmove = move
					turn = oturn
					flag = oturn
				elif j == 1:
					if minb > pval:
						return move
					else:
						return pmove

		minb = -100000
		for bl in valid_blocks:
			mvs = self.alphabeta(tboard, bl, turn, turn, 0, -100000, 100000)
			maxh = -100000
			if len(mvs) > 1:
				for mv in mvs:
					h = self.findh(mv, block, board, flag, bl)
					if h > maxh:
						maxh = h
						bmove = mv
				mv = bmove
			else:
				mv = mvs[0]

			tboard[mv[0]][mv[1]] = turn
			x = bl/4
			y = bl%4
			a = self.heur_val[x][y]
			self.heur_val[x][y] = self.heuristic(tboard, bl, flag)/1000.00
			hb = self.eval_board()
			if hb >= minb:
				minb = hb
				move = mv
			self.heur_val[x][y] = a
			tboard[mv[0]][mv[1]] = '-'
		return move



	def findh(self, move, block, board, flag, blck):
		blk_stat = []
		for i in range(0,4):
	   	    for j in range(0,4):
			blk_stat.append(block[i][j])
		valid_blocks = self.blocks_allowed(move, blk_stat)
		tboard = [row[:] for row in board]
		tboard[move[0]][move[1]] = flag
		tblock = block[:]

		h = self.heuristic(board, blck, flag)
		#print 'h value'
		#print h
		if h == 1000:
			tblock[blck] = flag
		if len(valid_blocks) == 0:
			#print 'findh'
			#pdb.set_trace()
			for i in range(16):
				if blk_stat[i] == '-':
					valid_blocks.append(i)

		minh = 100000
		for bl in valid_blocks:
			h = self.heuristic(board, bl, flag)
			if h < minh:
				minh = h

		return minh




	def heuristic(self, board,block_number,player):
		x_start = (block_number/4)*4
		y_start = (block_number%4)*4
		heuristic_value = 0
		# for i in range(3):
		# 	for j in range(3):
		# 		board[x_start+i][y_start+j]=raw_input()

		# for i in range(3):
		# 	for j in range(3):
		# 		print board[x_start+i][y_start+j],
		# 	print "\n"

		#horizontal check
		#print 'emter'
		for i in range(4):
			x = x_start + i
			y = y_start
			count_of_empty_cells = 0
			for j in range(4):
				y = y_start + j
				if board[x][y]=='-':
					count_of_empty_cells+=1
			x = x_start + i
			y = y_start
			if count_of_empty_cells==0:
				if board[x][y]==player and (board[x][y]==board[x][y+1] and board[x][y+2]==board[x][y+1]) and board[x][y+3]==board[x][y+2]:
					return 1000
				elif board[x][y]!=player and (board[x][y]==board[x][y+1] and board[x][y+2]==board[x][y+1])and board[x][y+3]==board[x][y+2]:
					return -1000
			elif count_of_empty_cells==1:
				if (board[x][y]==board[x][y+1] and board[x][y]==player and board[x][y+1]==board[x][y+2]) or (board[x][y+1]==board[x][y+2] and board[x][y+1]==player and board[x][y+3]==board[x][y+2]) or (board[x][y]==board[x][y+2] and board[x][y]==player and board[x][y+2]==board[x][y+3] ) or (board[x][y]==board[x][y+1] and board[x][y]==player and board[x][y+1]==board[x][y+3] ):
					heuristic_value+=100
				elif (board[x][y]==board[x][y+1] and board[x][y]!=player and board[x][y+1]==board[x][y+2]) or (board[x][y+1]==board[x][y+2] and board[x][y+1]!=player and board[x][y+3]==board[x][y+2]) or (board[x][y]==board[x][y+2] and board[x][y]!=player and board[x][y+2]==board[x][y+3] ) or (board[x][y]==board[x][y+1] and board[x][y]!=player and board[x][y+1]==board[x][y+3] ):
					heuristic_value-=100
			elif count_of_empty_cells==2:
				if (board[x][y]==player and board[x][y]==board[x][y+1]) or (board[x][y]==player and board[x][y]==board[x][y+2]) or (board[x][y]==player and board[x][y]==board[x][y+3]) or (board[x][y+1]==player and board[x][y+1]==board[x][y+2]) or (board[x][y+1]==player and board[x][y+1]==board[x][y+3]) or (board[x][y+2]==player and board[x][y+2]==board[x][y+3]):
					heuristic_value += 10
				elif (board[x][y]==player and board[x][y]==board[x][y+1]) or (board[x][y]==player and board[x][y]==board[x][y+2]) or (board[x][y]==player and board[x][y]==board[x][y+3]) or (board[x][y+1]==player and board[x][y+1]==board[x][y+2]) or (board[x][y+1]==player and board[x][y+1]==board[x][y+3]) or (board[x][y+2]==player and board[x][y+2]==board[x][y+3]):
					heuristic_value -= 10
			elif count_of_empty_cells==3:
				if board[x][y]==player or board[x][y+1]==player or board[x][y+2]==player or board[x][y+3]==player:
					heuristic_value+=1
				else:
					heuristic_value-=1
		#print heuristic_value,"horizontal"
		#vertical check
		for i in range(4):
			x = x_start
			y = y_start + i
			count_of_empty_cells = 0
			for j in range(4):
				x = x_start + j
				if board[x][y]=='-':
					count_of_empty_cells+=1
			x = x_start
			y = y_start + i
			if count_of_empty_cells==0:
				if board[x][y]==player and (board[x][y]==board[x+1][y] and board[x+2][y]==board[x+1][y]) and board[x+3][y]==board[x+2][y]:
					return 1000
				elif board[x][y]!=player and (board[x][y]==board[x+1][y] and board[x+2][y]==board[x+1][y])and board[x+3][y]==board[x+2][y]:
					return -1000
			elif count_of_empty_cells==1:
				if (board[x][y]==board[x+1][y] and board[x][y]==player and board[x+1][y]==board[x+2][y]) or (board[x+1][y]==board[x+2][y] and board[x+1][y]==player and board[x+3][y]==board[x+2][y]) or (board[x][y]==board[x+2][y] and board[x][y]==player and board[x+2][y]==board[x+3][y] ) or (board[x][y]==board[x+1][y] and board[x][y]==player and board[x+1][y]==board[x+3][y] ):
					heuristic_value+=100
				elif (board[x][y]==board[x+1][y] and board[x][y]!=player and board[x+1][y]==board[x+2][y]) or (board[x+1][y]==board[x+2][y] and board[x+1][y]!=player and board[x+3][y]==board[x+2][y]) or (board[x][y]==board[x+2][y] and board[x][y]!=player and board[x+2][y]==board[x+3][y] ) or (board[x][y]==board[x+1][y] and board[x][y]!=player and board[x+1][y]==board[x+3][y] ):
					heuristic_value-=100
			elif count_of_empty_cells==2:
				if (board[x][y]==player and board[x][y]==board[x+1][y]) or (board[x][y]==player and board[x][y]==board[x+2][y]) or (board[x][y]==player and board[x][y]==board[x+3][y]) or (board[x+1][y]==player and board[x+1][y]==board[x+2][y]) or (board[x+1][y]==player and board[x+1][y]==board[x+3][y]) or (board[x+2][y]==player and board[x+2][y]==board[x+3][y]):
					heuristic_value += 10
				elif (board[x][y]!=player and board[x][y]==board[x+1][y]) or (board[x][y]!=player and board[x][y]==board[x+2][y]) or (board[x][y]!=player and board[x][y]==board[x+3][y]) or (board[x+1][y]!=player and board[x+1][y]==board[x+2][y]) or (board[x+1][y]!=player and board[x+1][y]==board[x+3][y]) or (board[x+2][y]!=player and board[x+2][y]==board[x+3][y]):
					heuristic_value -= 10
			elif count_of_empty_cells==3:
				if board[x][y]==player or board[x+1][y]==player or board[x+2][y]==player or board[x+3][y]==player:
					heuristic_value+=1
				else:
					heuristic_value-=1
		#print heuristic_value,"vertical"
		#diagonal check 1
		flag = 0
		count_of_empty_cells = 0
		x = x_start
		y = y_start
		if board[x_start][y_start]=='-':
			count_of_empty_cells+=1
		if board[x_start+1][y_start+1]=='-':
			count_of_empty_cells+=1
		if board[x_start+2][y_start+2]=='-':
			count_of_empty_cells+=1
		if board[x_start+3][y_start+3]=='-':
			count_of_empty_cells+=1
		if count_of_empty_cells==0:
			if board[x][y]==player and (board[x][y]==board[x+1][y+1] and board[x+2][y+2]==board[x+1][y+1] and board[x+3][y+3]==board[x+2][y+2]):
				return 1000
			elif board[x][y]!=player and (board[x][y]==board[x+1][y+1] and board[x+2][y+2]==board[x+1][y+1] and board[x+3][y+3]==board[x+2][y+2]):
				return -1000
		elif count_of_empty_cells==1:
			if (board[x][y]==board[x+1][y+1] and board[x][y]==player and board[x+1][y+1]==board[x+2][y+2]) or (board[x+1][y+1]==board[x+2][y+2] and board[x+1][y]==player and board[x+3][y+3]==board[x+2][y+2]) or (board[x][y]==board[x+2][y+2] and board[x][y]==player and board[x+2][y+2]==board[x+3][y+3] ) or (board[x][y]==board[x+1][y+1] and board[x][y]==player and board[x+1][y+1]==board[x+3][y+3] ):
				heuristic_value+=100
			elif (board[x][y]==board[x+1][y+1] and board[x][y]!=player and board[x+1][y+1]==board[x+2][y+2]) or (board[x+1][y+1]==board[x+2][y+2] and board[x+1][y]!=player and board[x+3][y+3]==board[x+2][y+2]) or (board[x][y]==board[x+2][y+2] and board[x][y]!=player and board[x+2][y+2]==board[x+3][y+3] ) or (board[x][y]==board[x+1][y+1] and board[x][y]!=player and board[x+1][y+1]==board[x+3][y+3] ):
				heuristic_value-=100
		elif count_of_empty_cells==2:
			if (board[x][y]==player and board[x][y]==board[x+1][y+1]) or (board[x][y]==player and board[x][y]==board[x+2][y+2]) or (board[x][y]==player and board[x][y]==board[x+3][y+3]) or (board[x+1][y+1]==player and board[x+1][y+1]==board[x+2][y+2]) or (board[x+1][y+1]==player and board[x+1][y+1]==board[x+3][y+3]) or (board[x+2][y+2]==player and board[x+2][y+2]==board[x+3][y+3]):
				heuristic_value += 10
			elif (board[x][y]!=player and board[x][y]==board[x+1][y+1]) or (board[x][y]!=player and board[x][y]==board[x+2][y+2]) or (board[x][y]!=player and board[x][y]==board[x+3][y+3]) or (board[x+1][y+1]!=player and board[x+1][y+1]==board[x+2][y+2]) or (board[x+1][y+1]!=player and board[x+1][y+1]==board[x+3][y+3]) or (board[x+2][y+2]!=player and board[x+2][y+2]==board[x+3][y+3]):
				heuristic_value -= 10
		elif count_of_empty_cells==3:
			if board[x_start][y_start]==player or board[x_start+1][y_start+1]==player or board[x_start+2][y_start+2]==player or board[x_start+3][y_start+3]==player :
				heuristic_value+=1
			else:
				heuristic_value-=1
			flag = 1

		#diagonal check 2
		count_of_empty_cells = 0
		x = x_start+2
		y = y_start
		if board[x][y]=='-':
			count_of_empty_cells+=1
		if board[x-1][y+1]=='-':
			count_of_empty_cells+=1
		if board[x-2][y+2]=='-':
			count_of_empty_cells+=1
		if board[x-3][y+3]=='-':
			count_of_empty_cells+=1
		if count_of_empty_cells==0:
			if board[x][y]==player and (board[x][y]==board[x-1][y+1] and board[x-2][y+2]==board[x-1][y+1] and board[x-3][y+3]==board[x-2][y+2]):
				return 1000
			elif board[x][y]!=player and (board[x][y]==board[x-1][y+1] and board[x-2][y+2]==board[x-1][y+1] and board[x-3][y+3]==board[x-2][y+2]):
				return -1000
		elif count_of_empty_cells==1:
			if (board[x][y]==board[x-1][y+1] and board[x][y]==player and board[x-1][y+1]==board[x-2][y+2]) or (board[x-1][y+1]==board[x-2][y+2] and board[x-1][y]==player and board[x-3][y+3]==board[x-2][y+2]) or (board[x][y]==board[x-2][y+2] and board[x][y]==player and board[x-2][y+2]==board[x-3][y+3] ) or (board[x][y]==board[x-1][y+1] and board[x][y]==player and board[x-1][y+1]==board[x-3][y+3] ):
				heuristic_value+=100
			elif (board[x][y]==board[x-1][y+1] and board[x][y]!=player and board[x-1][y+1]==board[x-2][y+2]) or (board[x-1][y+1]==board[x-2][y+2] and board[x-1][y]!=player and board[x-3][y+3]==board[x-2][y+2]) or (board[x][y]==board[x-2][y+2] and board[x][y]!=player and board[x-2][y+2]==board[x-3][y+3] ) or (board[x][y]==board[x-1][y+1] and board[x][y]!=player and board[x-1][y+1]==board[x-3][y+3] ):
				heuristic_value-=100
		elif count_of_empty_cells==2:
			if (board[x][y]==player and board[x][y]==board[x-1][y+1]) or (board[x][y]==player and board[x][y]==board[x-2][y+2]) or (board[x][y]==player and board[x][y]==board[x-3][y+3]) or (board[x-1][y+1]==player and board[x-1][y+1]==board[x-2][y+2]) or (board[x-1][y+1]==player and board[x-1][y+1]==board[x-3][y+3]) or (board[x-2][y+2]==player and board[x-2][y+2]==board[x-3][y+3]):
				heuristic_value += 10
			elif (board[x][y]!=player and board[x][y]==board[x-1][y+1]) or (board[x][y]!=player and board[x][y]==board[x-2][y+2]) or (board[x][y]!=player and board[x][y]==board[x-3][y+3]) or (board[x-1][y+1]!=player and board[x-1][y+1]==board[x-2][y+2]) or (board[x-1][y+1]!=player and board[x-1][y+1]==board[x-3][y+3]) or (board[x-2][y+2]!=player and board[x-2][y+2]==board[x-3][y+3]):
				heuristic_value -= 10
		elif count_of_empty_cells==2 and flag == 0:
			if board[x][y]==player or board[x-1][y+1]==player or board[x-2][y+2]==player or board[x-3][y+3]==player:
				heuristic_value+=1
			else:
				heuristic_value-=1
		#print 'leave'
	        #print heuristic_value
		#print 'heur'
		#print "value", heuristic_value
		return heuristic_value

	def alphabeta(self, tboard, bl, flag, turn, depth, a, b):
		#print 'ala'
		if depth == self.max_depth:
			return self.heuristic(tboard, bl, flag)
			#return random.randrange(200) - 100
		if turn == 'x':
			oturn = 'o'
		else:
			oturn = 'x'
		cells = []
		x = (bl/4)*4
		y = (bl%4)*4
		for i in range(4):
			p = x+i
			for j in range(4):
				q = y + j
				if tboard[p][q] == "-":
					cells.append((p,q))
				else:
					#print p, q, tboard[p][q]
					pass
		moves = []
		#print cells
		for i in range(len(cells)):
			if a > b:
				#if depth == 0:
					#print "NO!"
				return util
			tboard[cells[i][0]][cells[i][1]] = turn
			h = self.heuristic(tboard, bl, flag)
			if h > 675:
				tboard[cells[i][0]][cells[i][1]] = "-"
				if depth == 0:
					#print "okay"
					return [cells[i]]
				return (self.max_depth - depth + 1)*1000
			elif h < -675:
				tboard[cells[i][0]][cells[i][1]] = "-"
				if depth == 0:
					#print "okay1"
					return [cells[i]]
					pass
				else:
					return (self.max_depth - depth + 1)*-1000
			elif h == 0:
				x = (bl/4)*4
				y = (bl%4)*4
				count = 0
				for p in xrange(x, x+4):
					for q in xrange(y, y+4):
						if tboard[p][q] == '-':
							count += 1
				if count == 0:
					if depth == 0:
						return [cells[i]]
					else:
						return 0
			v = self.alphabeta(tboard, bl, flag, oturn, depth+1, a, b)
			tboard[cells[i][0]][cells[i][1]] = "-"
			if i == 0:
				util = v
			if turn == flag:
				if v > a:
					a = v
					if depth == 0:
						moves.insert(0,cells[i])
				# elif abs(v - a) <= 5:
				# 	moves.append(cells[i])
				if v > util:
					util = v
			else:
				if v < b:
					b = v
				if v < util:
					util = v
		if depth == 0:
			if moves == []:
				print moves, " bottom"
			return moves
		if cells == []:
			return self.heuristic(tboard, bl, flag)
		return util


	def  blocks_allowed(self, old_move,block):
            for i in range(0,4):
		#print 'ioi'
                if old_move[0]%4 == i:
                    for j in range(0,4):
                        #print 'joj',old_move[1],j
                        if old_move[1]%4 == j:
			    #print 'asdsd'
                            block_next = 4*i+j
            #pdb.set_trace()
            #print block,block_next
            if block[block_next] != '-':
            	#pdb.set_trace()
            	return []
            #print 'sad'
 	 		    #pdb.set_trace()
			#print block_next
	    return [block_next]
