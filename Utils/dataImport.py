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
    result = [['o'] for _ in range(length)]
    
    # Populate the result array based on the intervals
    for value, label in data:
        index = int(value)  # Determine which interval the value belongs to
        if index < length:
            if result[index] == ['o']:  # Replace 'o' if it's still the default
                result[index] = [label]
            else:
                if label not in result[index]:  # Avoid duplicate letters
                    result[index].append(label)
    
    return result


def split_roll(roll, num_sub_rolls):
    """
    Splits the roll into `num_sub_rolls` sub-rolls. Each sub-roll will be a contiguous segment of the main roll.
    
    Parameters:
    - roll: The main roll, represented as a list of values (e.g., defect data).
    - num_sub_rolls: The number of sub-rolls to create.
    
    Returns:
    - A list of sub-rolls, where each sub-roll is a list representing a portion of the main roll.
    """
    sub_rolls = []
    sub_roll_length = len(roll) // num_sub_rolls  # Basic division of the roll length
    
    for i in range(num_sub_rolls):
        # For the last sub-roll, include the remaining part of the roll
        start_index = i * sub_roll_length
        if i == num_sub_rolls - 1:
            sub_rolls.append(roll[start_index:])  # Add the remaining portion for the last sub-roll
        else:
            sub_rolls.append(roll[start_index:start_index + sub_roll_length])
    
    return sub_rolls

def build_back_roll(sub_rolls):
    bigRoll = []
    for roll in sub_rolls:
        for value in roll:
            bigRoll.append(value)

    return bigRoll