import json
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

def analysis(file, user_id):
	try:
		file = pd.read_json('user_study.json')
	except FileNotFoundError:
         exit(0)
	minutes = file[file['user_id'] == user_id]['minutes'].sum()
	times = file[file['user_id'] == user_id]['minutes'].count()
	return times, minutes