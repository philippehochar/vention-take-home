from message import Message
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

d0c2 = messages[3][28]
plt.plot([m.timestamp for m in d0c2], [m.data[0] for m in d0c2], label="Expected")
plt.plot([m.timestamp for m in d0c2], [m.data[1] for m in d0c2], label="Actual")
plt.legend()
plt.show()
