import os
import sys
from matplotlib import pyplot as plt
import pandas as pd
entering = True
graphNr = 0
dataframes = []
while entering:
    path = input("Enter the path to a CSV file: ").strip().strip('"').strip("'")

    if not os.path.isfile(path):
        print("File not found:", path)
        break

    df = pd.read_csv(path, sep=',')

    if df is None:
        print("Failed to read CSV. Try opening it in a text editor to check delimiter/encoding.")
        sys.exit(1)

    print("Loaded file:", path)
    print("Columns:", list(df.columns))
    print(df.head(5))

    def angleChange(x):
        out = []
        for i in x:
            i = i-360 if i > 180 else i
            out.append(i)
        return out

    dataframes.append(pd.DataFrame(df.apply(angleChange, axis=1,result_type="broadcast")))
    print(pd.DataFrame(df.apply(angleChange, axis=1,result_type="broadcast")))


# Plotting
angleCols = [5, 6]
constantCols = [1, 2, 3, 4]
xcol = 0

print("Plotting x =", xcol, "y =", constantCols)
fig, (dataframes) = plt.subplots(len(dataframes),2, sharex=True)
for i in dataframes:
    i.plot(x=xcol, y=angleCols, grid=True)

ax1.set_xlabel("time (s)")
ax1.set_ylabel("angle")
#ax2.set_xlabel("time (s)")
#ax2.set_ylabel("controller output")
plt.legend()
plt.tight_layout()
plt.show()