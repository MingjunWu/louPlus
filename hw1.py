#! /usr/bin/env python3
import sys

if __name__ == '__main__':
 try:
    if(len(sys.argv)!=2):
      exit()

    wage = int(sys.argv[1])
    initial_tax_wage = 3500
    wage_tax = wage - initial_tax_wage
    if(wage_tax <= 0):
      wage_tax = 0
    tax = 0
    if wage_tax > 80000:
        tax = wage_tax * 0.45 - 13505
    elif wage_tax > 55000:
        tax = wage_tax * 0.35 - 5505
    elif wage_tax > 35000:
        tax = wage_tax * 0.3 - 2755
    elif wage_tax > 9000:
        tax = wage_tax * 0.25 - 1005
    elif wage_tax > 4500:
        tax = wage_tax * 0.2 - 555
    elif wage_tax > 1500:
        tax = wage_tax * 0.1 - 105
    else:
        tax = wage_tax * 0.03  - 0
    print(format(tax,".2f"))
 except:
    print("Parameter Error")
