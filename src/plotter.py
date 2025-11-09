from matplotlib import pyplot as plt
import pandas as pd

data = pd.read_csv(str(input("Enter the path to the CSV file: ")))
data.plot(x='time', y=['proportional', 'derivative', 'integral', 'output'])