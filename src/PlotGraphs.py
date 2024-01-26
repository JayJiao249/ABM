# PlotGraph.py
"""
This testing class is used to verify the functionality of plotting functions for generic agents, including line
graphs and scatter plots."""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import PredatorPreyModel
import ECAgent.Tags as Tags
import threading
import matplotlib

matplotlib.use('QtAGG')

csv_lock = threading.Lock()

# None reference for model
model = None

# List of agents in the model
agents = []

# Creates population array to store population of each iteration, appends at each iteration.
agent_population = []

# X-axis values (iteration count) for plotting the population graph.
x_vals = []

# Creates location array to store population of each iteration, refreshes at each iteration.
agent_locations = []

# Create line graph:
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()


def write_data_to_csv(iteration: int):
    global agent_locations, agent_population, x_vals
    for i in model.run(iteration):
        line = []
        for agent_name in agents:
            line.append(len(model.environment.get_agents(tag=Tags.__getattr__(agent_name.upper()))))
        with csv_lock:
            for population in agent_population:
                population[1].append(len(model.environment.get_agents(tag=Tags.__getattr__(population[0].upper()))))
            x_vals.append(len(agent_population[0][1]))

            agent_locations = []  # Reset agent locations
            for agent_name in agents:
                agent_locations.append([agent_name, [], []])
            for location in agent_locations:
                for agent in model.environment.get_agents(tag=Tags.__getattr__(location[0].upper())):
                    location[1].append(agent[PredatorPreyModel.PositionComponent].x)
                    location[2].append(agent[PredatorPreyModel.PositionComponent].y)


def animate(i):
    global agent_population, x_vals
    with plt.style.context('fivethirtyeight'):
        ax1.clear()
        for population in agent_population:
            ax1.plot(x_vals, population[1], label=population[0])
    ax1.legend()
    ax1.set_title(f'Population of agents at iteration :{model.iteration}')


def animate2(i):
    global agent_locations, agent_population
    ax2.clear()
    x_intervals = [-0.5 + i for i in range(int(51))]
    y_intervals = [-0.5 + i for i in range(int(51))]

    for x in x_intervals:
        ax2.axvline(x, color='gray', linestyle='--', linewidth=0.5)

    for y in y_intervals:
        ax2.axhline(y, color='gray', linestyle='--', linewidth=0.5)

    for location in agent_locations:
        ax2.scatter(location[1], location[2], marker='s', s=15)


'''
if __name__ == "__main__":

    model = PredatorPreyModel.PredatorPreyModel(50,100,50,30,4,0.04,25,0.06)

    # User needs to define the size for x and y limits
    ax2.set_xlim(0, size)
    ax2.set_ylim(0, size)

    # Gets a list of agents that are in the model.
    for agent in model.agent_last_id:
        agents.append(agent[0])
    for agent_name in agents:
        agent_population.append([agent_name, []])

    # User can define own iteration, args=(iteration)
    iteration = 1000
    thread_function1 = threading.Thread(target=write_data_to_csv, args=(iteration,))

    thread_function1.start()

    ani1 = FuncAnimation(fig1, animate, frames=1000, interval=5, cache_frame_data=False)
    ani2 = FuncAnimation(fig2, animate2, frames=1000, interval=5, cache_frame_data=False)

    plt.show()

    thread_function1.join()
'''
