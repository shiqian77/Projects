"""
fizzbuzz

Write a python script which prints the numbers from 1 to 100,
but for multiples of 3 print "fizz" instead of the number,
for multiples of 5 print "buzz" instead of the number,
and for multiples of both 3 and 5 print "fizzbuzz" instead of the number.
"""
for x in range(1,101):
    if x%3 == 0 and x%5 == 0:
        print('fizzbuzz')
    elif x%3 == 0:
        print('fizz')
    elif x%5 == 0:
        print('buzz')
    else:
        print(x)
        
