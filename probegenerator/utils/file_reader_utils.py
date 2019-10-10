import csv

def read_delimited_file_as_dict_list(path, delimiter=','):
    with open(path) as read_file:
        reader = csv.DictReader(read_file, delimiter=delimiter)
        return [row for row in reader]

def read_file_as_list_of_lines(path, strip_new_lines=False):
    with open(path) as read_file:
        lines = read_file.readlines()
        if strip_new_lines:
            return [line.strip('\n') for line in lines]
        return lines