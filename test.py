import sys
print("Platform: {0.platform}\nPython version: {0.version}".format(sys))

s0 = ['word', 11, 57, 44]
s = "{0} - {1} - {2}".format(*s0)
print(s)

print("Model - {model:.^10}, Auto - {auto:.^10}".format(model="X5", auto="BMW"))
print("{0:,d}".format(10000000).replace(",", " "))

x = 2.34567843256
print("x = {0:.2f}".format(x))

x = ["word1", "word2", "word3", "word4", "word5"]
# x = [1, 2, 3, 4, 5]
try:
    print(" + ".join(x))
except TypeError:
    print("x - not a String")
