def multi_table(x, y):
    sp = len(str(x*y))+1
    nsign = ""
    if x*y < 0:
        nsign = "-"
    x = abs(x)
    y = abs(y)
    for i in range(1, y+1):
        for a in range(1, x+1):
            res = nsign + str(i*a)
            print(res.rjust(sp), end='')
        print("\n")


def safe_input(n):
    num = 0
    while True:
        try:
            num = int(input(str(n) + " число - "))
            if num == 0:
                print("Умножение на ноль не имеет смысла. Введите другое число.")
                continue
            break
        except ValueError:
            print("Ошибка ввода. Введите целое число.")
            continue
    return num


num1 = safe_input(1)
num2 = safe_input(2)
multi_table(num1, num2)
