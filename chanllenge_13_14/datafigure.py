import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import Series, DataFrame

def show_data():
    try:
        data = pd.read_json('user_study.json')
    except FileNotFoundError:
           exit(0)
    fig = plt.figure()

    result = data.groupby('user_id')['minutes'].sum()
    result.plot(title = "studyData", )
    plt.xlabel("User ID")
    plt.ylabel("Study Time")
    plt.show()




if __name__ == '__main__':
    show_data()