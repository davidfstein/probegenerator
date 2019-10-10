import csv

def read_delimited_file_as_dict_list(path, delimiter=','):
    with open(path) as read_file:
        reader = csv.DictReader(read_file, delimiter=delimiter)
        return [row for row in reader]