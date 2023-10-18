import csv


def read_csv(file_name):
    with open(file_name, "r+") as file:
        reader = csv.reader(file)
        next(reader)  # skip the first row
        data = [(float(row[0]), float(row[1]))
                for row in reader]  # This is for dataset_1
    return data
