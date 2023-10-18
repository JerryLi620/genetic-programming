import csv

def load_dataset(filename):
    dataset = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            x1, x2, x3, fx = float(row[0]), float(
                row[1]), float(row[2]), float(row[3])
            dataset.append(((x1, x2, x3), fx))
    return dataset
