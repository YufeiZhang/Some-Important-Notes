import sys
import re
from copy import deepcopy as dc


try:
  #test=open(input( "Which data file do you want to use?"),'r')
  test = open("triangle_2.txt")
  testP=test.read()
  numbers=[]
  l=[]
except:
  print('Incorrect input, please check.')
  sys.exit()


test.seek(0)
testF=test.readlines()


L=[]
for line in testF:
  cols=line.split()
  numbers=list(map(int,cols))
  L.insert(0,numbers)
n=len(L)
m=n
x=0
lnew=[]
while m>0:
  lnew.append([0,[],1])
  m=m-1


for i in range(n-x):
  lnew[i][1].insert(0,L[0][i])
  lnew[i][0]=lnew[i][0]+L[0][i]

for p in range(1,n):                            # 这里因为要从倒数第二行开始，所以range是len(L)-1
  ln=[]                                         # 每一行的时候，ln都要变成一个空list

  for i in range(len(L[p])):                    # 这里是为了查每一行的各个数据，进行更新
    current = []                                # 这个是要放在 ln 里面的

    if lnew[i][0] > lnew[i+1][0]:               # 左边的比右边的大，选择走左边
      current.append(L[p][i] + lnew[i][0])
      path = dc(lnew[i][1])
      path.insert(0, L[p][i])
      current.append(path)
      current.append(lnew[i][2])


    elif lnew[i][0] < lnew[i+1][0]:              # 因为右边比左边的大，选择走右边
      current.append(L[p][i] + lnew[i+1][0])     # 这里更新 largest sum
      path = dc(lnew[i+1][1])                    # 这三行跟新最左路径
      path.insert(0, L[p][i])
      current.append(path)
      current.append(lnew[i+1][2])               # 这一行更新路径总数


    else:
      current.append(L[p][i] + lnew[i][0])
      path = dc(lnew[i][1])
      path.insert(0, L[p][i])
      current.append(path)
      current.append(lnew[i][2] + lnew[i+1][2])   # 路径总数只在 左右相等的时候要做计算

    ln.append(current)                            # 最后将 current append到ln上
  lnew = ln 


print('The largest sum is:', lnew[0][0])
print('The number of paths yielding this sum is:', lnew[0][2])
print('The leftmost path yielding this sum is:', lnew[0][1])
