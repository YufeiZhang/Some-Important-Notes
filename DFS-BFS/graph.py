from random import randint as ri

for i in range(50):
	a = ri(1,20)
	b = ri(1,20)
	if a != b:
		print("R({:d},{:d})".format(a,b))
