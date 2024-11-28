import csv

def importDefects(filepath):
    with open(filepath, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)                                            # Skip first row (header)
        data = [[float(row[0]), row[1]] for row in csv_reader]      # Parse data
        sorted_data = sorted(data, key=lambda x: x[0])              # Sort data (Not needed, may be removed but nice feature) 

    return sorted_data

def build_roll(data, length):    
    # Initialize an empty array with 'o' for each interval
    result = [['o'] for _ in range(length+1)]
    
    # Populate the result array based on the intervals
    for value, label in data:
        index = int(value)  # Determine which interval the value belongs to
        if result[index] == ['o']:  # Replace 'o' if it's still the default
            result[index] = [label]
        else:
            if label not in result[index]:  # Avoid duplicate letters
                result[index].append(label)
    
    return result