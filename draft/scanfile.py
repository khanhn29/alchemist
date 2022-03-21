import os
for file in os.listdir("data"):
    if file.endswith(".csv"):
        print(os.path.join("data", file))
        cur_file = open(os.path.join("data", file))
        