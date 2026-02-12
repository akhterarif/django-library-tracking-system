import random
rand_list = [random.randint(1, 20) for _ in range(10)]

print(rand_list)

# showing result using comprehension
list_comprehension_below_10 = [ i for i in rand_list if i < 10 ]

print(list_comprehension_below_10)


#  showing results using filter
def less_than_10(num):
    if num < 10:
        return num
    else:
        False
        
list_comprehension_below_10_filter = filter(less_than_10, rand_list)

result_list = [i for i in list_comprehension_below_10_filter]
print(result_list)