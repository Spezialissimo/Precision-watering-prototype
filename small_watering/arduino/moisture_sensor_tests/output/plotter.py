from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random
import pandas as pd

# initial data
df = pd.read_csv("moisture_values.csv")

# creating the first plot and frame
fig, ax = plt.subplots()
plt.ylim(0,100)

graph = ax.plot(df["timestamp"], df["sx_moisture_value"])[0]
graph2 = ax.plot(df["timestamp"], df["dx_moisture_value"])[0]

xticks = ax.get_xticks()
ax.set_xticks(xticks[::3])

# updates the data and graph
def update(frame):
    global graph
    global graph2

    # updating the data
    df = pd.read_csv("moisture_values.csv")
    # creating a new graph or updating the graph
    graph.set_xdata(df["timestamp"])
    graph.set_ydata(df["sx_moisture_value"])

    graph2.set_xdata(df["timestamp"])
    graph2.set_ydata(df["dx_moisture_value"])
    xticks = ax.get_xticks()
    ax.set_xticks(xticks[::3])
    plt.xlim(min(df["timestamp"]), max(df["timestamp"]))


anim = FuncAnimation(fig, update, frames=None)
plt.show()
