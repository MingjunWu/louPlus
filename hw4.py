#!/usr/bin/env python3
from multiprocessing import Process, Queue
import sys
import csv

INCOME_TAX_LOOKUP_TABLE = [
    (80000,0.45,13505),
    (55000, 0.35,5505),
    (35000, 0.30, 2755),
    (9000,0.25,1005),
    (4500,0.2,555),
    (1500, 0.1,105),
    (0,0.03,0)
]

queue1 = Queue()
queue2 = Queue()

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
    def file_after_option(self, option):
        try:
            index = self.args.index(option)
            return self.args[index+1]
        except (ValueError,IndexError):
            print("Parameter Error")
            exit()

    @property
    def config_path(self):
        return self.file_after_option('-c')
    @property
    def userdata_path(self):
        return self.file_after_option('-d')
    @property
    def export_path(self):
        return self.file_after_option('-o')

args = Args()

class Config(object):
    def __init__(self):
        self.config = self.read_config()
    def read_config(self):
        config_path = args.config_path
        config = {}
        with open(config_path) as file:
            for line in file.readlines():
                key,value = line.strip().split(' = ')
                try:
                    config[key] = float(value)
                except ValueError:
                    print("Parameter Error")
                    exit()
        return config

    def get_config(self, key):
        try:
            return self.config[key]
        except KeyError:
            print("Config Error")
            exit()
    @property
    def low_value(self):
        return self.get_config('JiShuL')
    @property
    def high_value(self):
        return self.get_config('JiShuH')
    @property
    def total(self):
        return sum([
            self.get_config('YangLao'),
            self.get_config('YiLiao'),
            self.get_config('ShiYe'),
            self.get_config('GongShang'),
            self.get_config('ShengYu'),
            self.get_config('GongJiJin')
        ])

config = Config()

class UserData(object):
    def __init__(self):
        self.user_data = self.read_user_data() 
        Process(target=self.read_user_data()).start()
    def read_user_data(self):
        user_data_path = args.userdata_path
        user_data = []
        with open(user_data_path) as file:
            for line in file.readlines():
                id, wage = line.strip().split(',')
                try:
                    wage = int(wage)
                except ValueError:
                    print("Parameter Error")
                    exit()
                user_data.append((id,wage))
        queue1.put(user_data)
        return user_data
    def __iter__(self):
        return iter(self.user_data)

class Calculator(object):
    def __init__(self,userdata):
        self.userdata = userdata
    @staticmethod
    def social_insurance_money(income):
        if income < config.low_value:
            return config.low_value * config.total
        if income > config.high_value:
            return config.high_value * config.total
        return income * config.total
    @classmethod
    def tax_and_remain(cls, income):
        social_insurance_money = cls.social_insurance_money(income)
        real_wage = income - social_insurance_money
        taxable = real_wage - 3500
        if taxable <=0:
            return '0.00','{:.2f}'.format(real_wage)
        for item in INCOME_TAX_LOOKUP_TABLE:
            if taxable > item[0]:
                tax = taxable * item[1] - item[2]
                return '{:.2f}'.format(tax),'{:.2f}'.format(real_wage - tax)
    def cal_for_all_user(self):
        result = []
        for id, income in queue1.get():
            data = [id, income]
            social_insurance = '{:.2f}'.format(self.social_insurance_money(income))
            tax, remain = self.tax_and_remain(income)
            data+=[social_insurance, tax, remain]
            result.append(data)
        queue2.put(result)
        return result

    def export(self, default = 'csv'):
        Process(target=self.cal_for_all_user()).start()
        result = queue2.get()
        with open(args.export_path,'w',newline = '') as file:
            writer = csv.writer(file)
            writer.writerows(result)

if __name__ == '__main__':
    calculator = Calculator(UserData())
    Process(target=calculator.export()).start()        
    
