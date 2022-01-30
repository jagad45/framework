def convert_hashrate(value):
    lst = ["K", "M", "G"]
    output = ""
    for x in lst:
        current_value = int(value / 1024)
        if current_value < 1024: 
            output = f"{current_value}{x}"
            break
        else: continue
    return output