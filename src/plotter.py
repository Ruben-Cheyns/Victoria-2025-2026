import os
import sys
from matplotlib import pyplot as plt
import pandas as pd

path = input("Enter the path to the CSV file: ").strip().strip('"').strip("'")

if not os.path.isfile(path):
    print("File not found:", path)
    sys.exit(1)

df = pd.read_csv(path)

if df is None:
    print("Failed to read CSV. Try opening it in a text editor to check delimiter/encoding.")
    sys.exit(1)

print("Loaded file:", path)
print("Columns:", list(df.columns))
print(df.head(5))
# Plotting
angleCols = ['desiredValue', 'angle']
constantCols =['proportional', 'derivative', 'integral', 'output']
xcol = 'time'

print("Plotting x =", xcol, "y =", constantCols)
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 12), sharex=True)
ax[0,0] = df.plot(x=xcol, y=angleCols, grid=True, figsize=(10,6))
ax[1,0] = df.plot(x=xcol, y=constantCols, grid=True, figsize=(10,6))

ax[0,0].set_xlabel(xcol)
ax[0,0].set_ylabel("angle")
ax[1,0].set_xlabel(xcol)
ax[1,0].set_ylabel("% motor speed")
plt.legend()
plt.tight_layout()
plt.show()