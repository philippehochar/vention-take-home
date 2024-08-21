from message import Message
from animator import animate
import matplotlib.pyplot as plt

log_file = open("./logs/loaded.log", "r")

messages: dict[int, dict[int, list[Message]]] = {}
drives: dict[int, list[int]] = {}

for line in log_file.readlines():
    message = Message(line)
    if message.drive not in messages.keys(): messages[message.drive] = {}
    if message.channel not in messages[message.drive].keys(): messages[message.drive][message.channel] = []
    messages[message.drive][message.channel].append(message)
    if message.drive not in drives.keys(): drives[message.drive] = []
    if not message.channel in drives[message.drive]: drives[message.drive].append(message.channel)


print(drives)


def plot_pos(ax: plt.Axes, ms: list[Message]):
    ax.plot([m.timestamp for m in ms], [m.data[0] for m in ms], color='g', linestyle="--", label="Position (expected)")
    ax.plot([m.timestamp for m in ms], [m.data[1] for m in ms], color='g', linestyle='-', label="Position (actual)")
    ax.legend()


def plot_spd(ax: plt.Axes, ms: list[Message]):
    ax.plot([m.timestamp for m in ms], [m.data[0] for m in ms], color='r', linestyle="--", label="Speed (expected)")
    ax.plot([m.timestamp for m in ms], [m.data[1] for m in ms], color='r', linestyle="-", label="Speed (actual)")
    ax.legend()


def plot_trq(ax: plt.Axes, ms: list[Message]):
    ax.plot([m.timestamp for m in ms], [m.data[1] for m in ms], color='b', label="Torque (Actual)")
    ax2= ax.twinx()
    ax2.plot([m.timestamp for m in ms], [m.data[2] for m in ms], color='c', label="Control Effort")
    ax2.legend(loc='upper right')
    ax.legend(loc='lower right')


def plot_sw(ax: plt.Axes, ms: list[Message]):
    ax.plot([m.timestamp for m in ms], [m.data[0] for m in ms], label="sw")
    ax.legend()


def plot_driver(driver: int):
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True)
    fig.suptitle(f"Driver {driver} Data")
    ax1.title.set_text("Position")
    plot_pos(ax1, messages[driver][28])
    ax2.title.set_text("Speed")
    plot_spd(ax2, messages[driver][38])
    ax3.title.set_text("Torque / Control Effort")
    plot_trq(ax3, messages[driver][18])
    ax4.title.set_text("Status Word")
    plot_sw(ax4, messages[driver][18])
    plt.legend()
    plt.show()


def plot_pos_comparison(driver1: int, driver2: int):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.suptitle("Driver Position Comparison")
    ax1.title.set_text(f"Driver {driver1} Position")
    plot_pos(ax1, messages[driver1][28])
    ax2.title.set_text(f"Driver {driver2} Position")
    plot_pos(ax2, messages[driver2][28])

    for i in range(1, len(messages[driver1][18])):
        if messages[driver1][18][i - 1].data[0] > messages[driver1][18][i].data[0] and messages[driver1][18][i].data[0] < 36000:
            ax1.axvline(x=messages[driver1][18][i].timestamp, color='gray')
            ax2.axvline(x=messages[driver1][18][i].timestamp, color='gray')
    for i in range(1, len(messages[driver2][18])):
        if messages[driver2][18][i - 1].data[0] > messages[driver2][18][i].data[0] and messages[driver2][18][i].data[0] < 36000:
            ax1.axvline(x=messages[driver2][18][i].timestamp, color='gray')
            ax2.axvline(x=messages[driver2][18][i].timestamp, color='gray')

    plt.legend()
    plt.show()


plot_driver(1)
plot_driver(2)
plot_driver(3)

plot_pos_comparison(1, 3)

animate(messages[1][28][:4192:2], messages[3][28][:4192:2])
