import numpy as np



filename='D:/pythoncode/test\\clmforc.0.1x0.1.prec-2010-01.nc'
if '-04' in filename or '-06'  in filename or'-09' in filename or '-11' in filename:
	print ("yes")
else:
	print ("no")

Bin='as'
a=[Bin,'c']
print(a)




def test2():
	print("Testing 2 dimensions")


def test():
	print("Testing")
	test2()

test()
a=np.ones((12,14,15))
b=np.zeros((12,14,15))
d=["a","b","c","d"]
c=[]
c.append(a)
c.append(b)
c[0][0][0][0]=56
print(c[0])
print("--------------------------------------")
for i in c:
	print(i)
	print("+++++++++++++++++++++++++++++++")
print("--------------------------------------")
for i,j in zip(a,b):
	print(i)
	print(j)
	print("+++")