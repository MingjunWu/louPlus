import pandas as pd
from pandas import Series, DataFrame

def quarter_volume():
	try:
		data = pd.read_csv('apple.csv',header=0)
	except FileNotFoundError:
		exit(0)
	volume = data.Volume
	volume.index = pd.to_datetime(data.Date)
	result = volume.resample('Q').sum().sort_values()[-2]
	return result



if __name__ == '__main__':
	quarter_volume()