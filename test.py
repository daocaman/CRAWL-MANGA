def generateName(num, l):
    result_str = "0"*l + str(num)

    return result_str[-1*l:]


for i in range(1, 100):
    print(generateName(i, 4))
