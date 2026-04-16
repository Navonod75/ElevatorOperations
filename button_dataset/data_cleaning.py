forbidden = {"open", "close", "alarm", "blank", "unknown", "empty", "speaker", "led", "keyhole", "blur", "up", "down", "call", "switch", "indicator", "stop"}

pics = set()

with open("valid/_annotations.csv", "r") as f:
    lines = f.readlines()
    for line in lines:
        pics.add(line.split(",")[0])

with open("valid/_clean_annotations.csv", "w") as f:
    for line in lines:
        if line.split(",")[3].isnumeric() or len(line.split(",")[3]) == 1:
            f.write(line)

print(len(pics))