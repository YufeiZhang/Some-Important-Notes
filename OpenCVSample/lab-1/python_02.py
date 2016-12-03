import numpy as np

ones = np.ones(100)
rand = np.random.rand(100,1)*10
for x in range(0,len(rand)):
	print " %f" % rand[x]