import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from matplotlib import animation 
from matplotlib import colormaps
import numpy as np

# Iteration 1
it1_sitters = []

it1_tappers = []

# Iteration #2
it2_sitters = []

it2_tappers = []

# Iteration #3
it3_sitters = []

it3_tappers = []

# Iteration #4
it4_sitters = []

it4_tappers = []

# Iteration #5
it5_sitters = []

it5_tappers = []

# Iteration #6
it6_sitters = []

it6_tappers = []

# Iteration #7
it7_sitters = []

it7_tappers = []

# Iteration #8
it8_sitters = []

it8_tappers = []

# Iteration #9
it9_sitters = []

it9_tappers = []

# Iteration #10
it10_sitters = []

it10_tappers = []

# Iteration 11
it11_sitters = []

it11_tappers = []

# Iteration 12
it12_sitters = []

it12_tappers = []

# Iteration 13
it13_sitters = []

it13_tappers = []

# Iteration 14
it14_sitters = []

it14_tappers = []

# Iteration 15
it15_sitters = []

it15_tappers = []

# Iteration 16
it16_sitters = []

it16_tappers = []

# Iteration 17
it17_sitters = []

it17_tappers = []

# Iteration 18
it18_sitters = []
it18_tappers = []

# Iteration 19
it19_sitters = []
it19_tappers = []

# Iteration 20
it20_sitters = []

it20_tappers = []

"""
# Visualization #1 - Starting Escapability vs Tapability
# Get initial tapability and escapability values
start_tap = [sublist[4] for sublist in it1_tappers]
start_escape = [sublist[3] for sublist in it1_sitters]
data = [start_tap, start_escape]
labels = ['Starting Tapability', 'Starting Escapability']

# Create the plot
fig, ax = plt.subplots(figsize=(8, 4))
for i, d in enumerate(data):
    # avoid overlapping points
    jittered_y = np.random.normal(i + 1, 0.05, size=len(d))
    ax.scatter(d, jittered_y, alpha=0.8)

# Set axis labels
ax.set_xlim(1, 10) 
ax.set_yticks(range(1, len(data) + 1))
ax.set_yticklabels(labels)
ax.set_xlabel('Values')
ax.set_title('Starting Tapability and Escapability')

# Show plot
plt.tight_layout()
plt.show() 
"""

"""
# Visualization 2 - Fun Over Time
# Get fun values for each iteration
fun1 = [sublist[6] for sublist in it1_sitters]
fun2 = [sublist[6] for sublist in it2_sitters]
fun3 = [sublist[6] for sublist in it3_sitters]
fun4 = [sublist[6] for sublist in it4_sitters]
fun5 = [sublist[6] for sublist in it5_sitters]
fun6 = [sublist[6] for sublist in it6_sitters]
fun7 = [sublist[6] for sublist in it7_sitters]
fun8 = [sublist[6] for sublist in it8_sitters]
fun9 = [sublist[6] for sublist in it9_sitters]
fun10 = [sublist[6] for sublist in it10_sitters]
fun11 = [sublist[6] for sublist in it11_sitters]
fun12 = [sublist[6] for sublist in it12_sitters]
fun13 = [sublist[6] for sublist in it13_sitters]
fun14 = [sublist[6] for sublist in it14_sitters]
fun15 = [sublist[6] for sublist in it15_sitters]
fun16 = [sublist[6] for sublist in it16_sitters]
fun17 = [sublist[6] for sublist in it17_sitters]
fun18 = [sublist[6] for sublist in it18_sitters]
fun19 = [sublist[6] for sublist in it19_sitters]
fun20 = [sublist[6] for sublist in it10_sitters]

# Set data labels and categories
iterations = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
categories = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
values = [
    fun1, fun2, fun3, fun4, fun5, fun6, fun7, fun8, fun9, fun10, fun11, fun12, fun13, fun14, fun15, fun16, fun17, fun18, fun19, fun20
]

# Set up figure structure
fig, ax = plt.subplots()
bars = ax.bar(categories, values[0])
ax.set_ylim(-20, max(max(values)) + 5)
ax.set_title("Category Values Over Time")
ax.set_ylabel("Value")
ax.set_xlabel("Sitter")

# Update figure for each iteration
def update(frame):
    for bar, val in zip(bars, values[frame]):
        bar.set_height(val)
    ax.set_title(f"Fun Values in Iteration: {iterations[frame]}")

# Animate figures together
ani = FuncAnimation(fig, update, frames=len(iterations), repeat=True, interval=700)
ani.save("Trial3Visual2.mp4", writer=animation.FFMpegWriter(fps=5)) 
"""
"""
# Visulization #3 - Who is Winked At

# Set number of sitters
n_people = 10

# Generate circular coordinates to place dots at
angles = np.linspace(0, 2 * np.pi, n_people, endpoint=False)
radius = 1 
x_coords = radius * np.cos(angles)
y_coords = radius * np.sin(angles)
heat_values = np.zeros(n_people)

# People Chosen (from output file information)
update_sequence = [5, 9, 6, 9, 10, 2, 1, 9, 1, 3, 7, 1, 1, 10, 7, 9, 8, 9, 8, 1]   # Sitters chosen in order throughout game

# Set up the figure 
fig, ax = plt.subplots(figsize=(6, 6))
cmap = plt.cm.Blues  # Define colormap
norm = Normalize(vmin=0, vmax=1)  # Normalize heat values to the range [0, 1]
scatter = ax.scatter(
    x_coords, y_coords,
    c=cmap(norm(heat_values)),  # Initial color values
    s=200, edgecolor='black'
)

# Add labels for each dot and add offset to avoid overlap with dots
label_offset = 0.05
for i, (x, y) in enumerate(zip(x_coords, y_coords)):
    ax.annotate(
        str(i + 1),
        (x + label_offset, y + label_offset),
        color='black',
        fontsize=10,
        ha='center',
        va='center',
        zorder=3,
    )

# Add title to figure
ax.set_title("Chosen Sitters Throughout Game Progression")
ax.axis('off')

# Function to increment heat value when chosen
def update_heat_values(person_index):
    heat_values[person_index] += 0.2  # Increment heat for the specified dot
    heat_values[person_index] = min(heat_values[person_index], 1) 

# Update function to create additional frames
def update(frame):
    if frame == 0:
        # Initial frame: do not update heat values
        scatter.set_facecolor(cmap(norm(heat_values)))
    else:
        person_to_update = update_sequence[frame - 1]  # Subtract 1 for zero-based indexing
        update_heat_values(person_to_update - 1)
        scatter.set_facecolor(cmap(norm(heat_values)))
    return scatter,

# Create the animation
ani = FuncAnimation(
    fig, update, frames=len(update_sequence) + 1, interval=1100, blit=False
)
ani.save("Trial3Visual3.mp4", writer=animation.FFMpegWriter(fps=2))
"""
"""
# Visualization #4 and #5 - Escape Rate vs Tap Rate
# Set up figure for Sitters
num_escape_sit = [sublist [1] for sublist in it20_sitters]
num_tap_sit = [sublist[2] for sublist in it20_sitters]
indices = np.arange(len(num_escape_sit))
bar_width = 0.35
plt.bar(indices, num_escape_sit, bar_width, label='Number of Times Escaped', color='b')
plt.bar(indices + bar_width, num_tap_sit, bar_width, label='Number of Times Tapped', color='g')

# Add labels and title to figure
plt.xlabel('Sitter')
plt.ylabel('Values')
plt.title('Number of Times Tapped and Escaped')
plt.xticks(indices + bar_width / 2, indices + 1) 
plt.legend()

# Show the plot
plt.tight_layout()
plt.show() 
"""
"""
# Set up figure for Tappers
num_escape_tap = [sublist [3] for sublist in it20_tappers]
num_tap_tap = [sublist[2] for sublist in it20_tappers]
indices = np.arange(len(num_escape_tap))
bar_width = 0.35
plt.bar(indices, num_escape_tap, bar_width, label='Number of Times Escaped', color='b')
plt.bar(indices + bar_width, num_tap_tap, bar_width, label='Number of Times Tapped', color='g')

# Add labels and title to figure
plt.xlabel('Tapper')
plt.ylabel('Values')
plt.title('Number of Times Tapped and Escaped')
plt.xticks(indices + bar_width / 2, indices + 1) 
plt.legend()

# Show the plot
plt.tight_layout()
plt.show() 
"""

# Visualization #6 - Animation of Sitter Chosen
numbers = [5, 9, 6, 9, 10, 2, 1, 9, 1, 3, 7, 1, 1, 10, 7, 9, 8, 9, 8, 1]
count = [0] * 10

# Create the figure and set labels
fig, ax = plt.subplots()
bars = ax.bar(np.arange(1, 11), count, color='skyblue')
ax.set_ylim(0, 10)
ax.set_xlabel('Sitter')
ax.set_ylabel('Times Winked At')
ax.set_title('Sitters Winked At')
ax.set_xticks(np.arange(1, 11))

# Update figure for each iteration
def update(frame):
    number = numbers[frame]
    count[number - 1] += 1
    for i, bar in enumerate(bars):
        bar.set_height(count[i])
    ax.set_title(f'Sitters winked At: Iteration {frame + 1}/{len(numbers)}')

# Create the animation
def init():
    for bar in bars:
        bar.set_height(0)
    ax.set_title('Sitters Winked At')
    return bars

# Save Animation
ani = FuncAnimation(fig, update, frames=len(numbers), init_func=init, interval=1100, repeat=False)
ani.save("Trial3Visual6.mp4", writer=animation.FFMpegWriter(fps=2))
