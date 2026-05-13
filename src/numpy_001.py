
import numpy as np
print('numpy version: ', np.__version__)

import matplotlib
print("Current backend:", matplotlib.get_backend())


# arrays!
mylist = [1,2,3]
# print(mylist)
# print(type(mylist))

my_array = np.array(mylist)
# print(type(my_array))

a = np.arange(0,10,2)
# print(a)

b = np.zeros(shape=(5,5))
# print(b)
b = np.ones(shape=(5,2))
b*10
# print(b)

np.random.seed(101)
r1 = np.random.randint(0,100,10)
# print(r1)
# print(type(r1))
r2 = np.random.randint(0,100,10)
print(r2)
#
# print('max value', r2.max())
# print('max value location in array', r2.argmax())
# print('min value', r2.min())
# print('min value location in array', r2.argmin())
# print('average value', r2.mean())
# print('shape of array', r2.shape)
# print('reshape the array in the same box', r2.reshape(5,2))

print('----indexing----')

mat = np.arange(0,100).reshape(10,10)
print(mat)
print(mat.shape)
print(mat.dtype)
print('to select one element from that array I use index')
row=2
col=5
print('i 25 ? : ', mat[row,col])

print('---slicing vertically')
print(mat[:,1])
print(mat[:,1].reshape(10,1))
print(mat[:,1].reshape(1,10))

print('---slicing horizontally')
print(mat[2,:])

print('---slicing horizontally and vertically some part of the array')
print(mat[0:3,0:4])
my_new_mat = mat.copy()
my_new_mat[0:3,0:4]=0
print(my_new_mat)
my_new_mat[0:6,:]=333
print(my_new_mat)