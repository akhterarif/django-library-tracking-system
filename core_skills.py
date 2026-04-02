import random
rand_list = [random.randint(1, 20) for i in range(20)]
print(rand_list)
list_comprehension_below_10 = [i for i in rand_list if i < 10]

print(list_comprehension_below_10)

def below_10(num):
    if num< 10:
        return num

filt_list_comprehension_below_10 = filter(below_10, rand_list)
list_comprehension_below_10 = [i for i in filt_list_comprehension_below_10]

print(list_comprehension_below_10)