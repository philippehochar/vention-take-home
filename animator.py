from message import Message

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(dr1: list[Message], dr2: list[Message]):
    # Extract x and y values for both lines
    expected_x = [m.data[0] for m in dr1]
    expected_y = [m.data[0] for m in dr2]

    actual_x = [m.data[1] for m in dr1]
    actual_y = [m.data[1] for m in dr2]

    # Set up the figure and axis
    fig, ax = plt.subplots()
    ax.set_xlim(min(min(expected_x), min(actual_x)), max(max(expected_x), max(actual_x)))
    ax.set_ylim(min(min(expected_y), min(actual_y)), max(max(expected_y), max(actual_y)))

    # Create line objects, which will be updated during the animation
    line1, = ax.plot([], [], lw=2, label='Expected')
    line2, = ax.plot([], [], lw=2, label='Actual')

    # Initialization function: plot the background of each frame
    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        return line1, line2

    # Animation function: this is called sequentially
    def animate(i):
        # Update the lines with the new data up to index i
        line1.set_data(expected_x[max(0, i-30):i+1], expected_y[max(0, i-30):i+1])
        line2.set_data(actual_x[max(0, i-30):i+1], actual_y[max(0, i-30):i+1])
        return line1, line2

    # Call the animator
    anim = FuncAnimation(fig, animate, init_func=init, frames=len(expected_x), interval=10, blit=True)

    # Add a legend to distinguish the lines
    ax.legend()

    # Save the animation as a video file
    # anim.save('two_lines_trace.mp4', fps=60, extra_args=['-vcodec', 'libx264'])

    # Display the plot (optional)
    plt.show()
