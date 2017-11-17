#! /usr/bin/env python3
import sys
def wage_after_tax(wage):
    wage_should_be_taxed = wage - wage * 0.165 - 3500
    income_lookup_table = [
        (80000, 0.45,13505),
        (55000, 0.35,5505),
        (35000, 0.30,2755),
        (9000, 0.25,1005),
        (4500, 0.20, 555),
        (1500, 0.10, 105),
        (0, 0.03, 0)
    ]
    if wage_should_be_taxed < 0:
        wage_should_be_taxed = 0
    tax = 0
    for item in income_lookup_table:
        if wage_should_be_taxed > item[0]:
           tax = wage_should_be_taxed * item[1] - item[2]
           break
    return format(wage - wage * 0.165 - tax, ".2f")
if __name__ == '__main__':
    final = {}
    if(len(sys.argv[1:]) == 0):
        print("Parameter Error")
        exit()
    for arg in sys.argv[1:]:
        result = arg.split(':')
        if len(result)!=2:
            print("Parameter Error")
            break
            exit()
        try:
            wage = int(result[1])
            print("{}:{}".format(result[0],wage_after_tax(wage)))
        except ValueError:
            print("Parameter Error")
            exit()



