log_file = open("./logs/unloaded.log", "r")

for line in log_file.readlines():
    print(line)