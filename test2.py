import time

s = "String"
for i in s:
    print(i, end='')

s = "Long String"
a = "Long+"
if a in s:
    print("\nOk")
else:
    print("\nNot OK")

s = "str"
print(s.center(15, '-'))


for i in range(0, 101):
    print("Progress: {0}%".format(i), end='')
    time.sleep(.05)
    print("\r", end='')
