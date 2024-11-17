from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search
import sys
import argparse
import time

start_time = time.time()
def print_solution(s, size):
  s_ = {}

  verbose = False
  for var, val in s:
    s_[int(var.name())] = val
    if verbose:
      print("Var n: {}, Value: {}".format(var.name(), val))

  for i in range(size):
    for j in range(size):
      cur = s_[(i*size+j)]
      if cur == 1:
        left, right, top, bot = 0, 0, 0, 0
        if j != 0:
          left = s_[(i*size+j-1)]
        if j != size-1:
          right = s_[(i*size+j+1)]
        if i != 0:
          top = s_[((i-1)*size+j)]  
        if i != size-1:
          bot = s_[((i+1)*size+j)]
        if verbose:
          print(f"({i},{j}): {left} {right} {top} {bot}")
        if (left  and right == 1) or (top and bot == 1):
          print('M',end="")
        elif (left == 1 and right == 0): 
          print('>',end="") 
        elif (left == 0 and right == 1): 
          print('<',end="") 
        elif (top == 0 and bot == 1): 
          print('^',end="") 
        elif (bot == 0 and top == 1): 
          print('v',end="") 
        else: 
          print('S',end="")
      elif cur == 0:
        print('.',end="")
      else: 
        print("UNEXPECTED CHARACTER")
    print('')

#parse board and ships info
#file = open(sys.argv[1], 'r')
#b = file.read()
parser = argparse.ArgumentParser()
parser.add_argument(
  "--inputfile",
  type=str,
  required=True,
  help="The input file that contains the puzzles."
)
parser.add_argument(
  "--outputfile",
  type=str,
  required=True,
  help="The output file that contains the solution."
)
args = parser.parse_args()
file = open(args.inputfile, 'r')
b = file.read()
b2 = b.split()
size = len(b2[4])
board = b2[3:] 
rows = b.split()[0]
cols = b.split()[1]

varlist = []
varn = {}
conslist = []

#1/0 variables
for i in range(0,size):
  for j in range(0, size):
    v = None

    # v = Variable(f"|r:{i} c:{j}|", [0,1])
    v = Variable(str((i*size+j)), [0,1])
    varlist.append(v)
    varn[str(i*size+j)] = v



#make 1/0 variables match board info
board = [list(row) for row in b2[3:]]

for i in range(size):
  for j in range(size):
    var = varn[str(i*size+j)]
    # TODO: reduce domains (preprocessing) 
    if board[i][j] != '0' and board[i][j] != '.':
      var.resetDomain([1])
    if board[i][j] == '.':
      var.resetDomain([0])

for i in range(size):
  if rows[i] == 0:
    for j in range(size):
      var = varn[str(i*size+j)]
      var.resetDomain([0])
  if cols[i] == 0:
    for j in range(size):
      var = varn[str(j*size+i)]
      var.resetDomain([0])


i = 0
for row in range(size):
  conslist.append(NValuesConstraint(f'row{i}', [varn[str(row*size+col)] for col in range(size)], [1], int(rows[row]), int(rows[row])))
  i += 1


i = 0
for col in range(size):
  conslist.append(NValuesConstraint(f'col{i}', [varn[str(col+row*size)] for row in range(size)], [1], int(cols[col]), int(cols[col])))
  i += 1

#diagonal constraints on 1/0 variables
for i in range(1, size-1):
    for j in range(1, size-1):
      conslist.append(NValuesConstraint('diag', [varn[str(i*size+j)], varn[str((i-1)*size+(j-1))]], [1], 0, 1))
      conslist.append(NValuesConstraint('diag', [varn[str(i*size+j)], varn[str((i-1)*size+(j+1))]], [1], 0, 1))

#./S/</>/v/^/M variables
#these would be added to the csp as well, before searching,
#along with other constraints
#for i in range(0, size):
#  for j in range(0, size):
#    v = Variable(str(i*size+j), ['.', 'S', '<', '^', 'v', 'M', '>'])
#    varlist.append(v)
#    varn[str(str(i*size+j))] = v
#connect 1/0 variables to W/S/L/R/B/T/M variables
#    conslist.append(TableConstraint('connect', [varn[str(-1-(i*size+j))], varn[str(i*size+j)]], [[0,'.'],[1,'S'],[1,'<'],[1,'^'],[1,'v'],[1,'M'],[1,'>']]))




#find all solutions and check which one has right ship #'s
csp = CSP('battleship', varlist, conslist)
print("CSP Name:", csp.name())
for var in csp.variables():
  print(f"  {var.name()}: Domain = {var.curDomain()}")
# print("Constraints:")
# for cons in csp.constraints():
#   print(f"  {cons.name()}: Scope = {[v.name() for v in cons.scope()]}")

solutions, num_nodes = bt_search('FC', csp, 'mrv', True, False)

sys.stdout = open(args.outputfile, 'w')
print_solution(solutions, size)
print("--------------")

sys.stdout = sys.__stdout__
print(f"Time elapsed: {time.time() - start_time} seconds")