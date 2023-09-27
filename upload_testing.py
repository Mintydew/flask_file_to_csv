# Python code for the purposes of testing the upload methods.
# Created due to having to upload the specific text file manually through the form for every testing scenario which
# caused a tedious way to work with the methods.
# Danny Kim 25/09/2023
import csv

url = ""  # Hidden for privacy purposes
ALLOWED_EXTENSIONS = {"txt"}


def url_check(uploaded_file):
    first_line_dict = {}
    subsequent_line_dict = {}
    split_url = url.split(".")  # Adjusted code to main due to using a hardcoded url
    # print(uploaded_file)

    if split_url[-1].lower() in ALLOWED_EXTENSIONS:  # Split code between header and subsequent data lines
        data_split = uploaded_file.splitlines()
        # first_line = data_split[0].replace(" ", ",")
        first_line = data_split[0].split(" ")
        subsequent_line = data_split[1:]
        # first_line = uploaded_file.readline().decode('utf-8').replace(" ", "")  # Remove all white spaces inbetween
        # # each character in the heading
        # subsequent_line = uploaded_file.read().decode('utf-8').replace(" ", "").splitlines()  # Remove all white
        # # spaces inbetween each character in the heading
        # print(subsequent_line)

        first_key = 0
        for list_item in first_line:  # Removes hidden newline characters from being inputted into the
            # print(list_item)
            # dictionary keys
            first_line_dict[list_item] = first_key
            first_key += 1

        line_number = 0
        for line in subsequent_line:
            # print(line.split(" "))
            line_dict = {}
            subsequent_key = 0
            # print(line)
            # for char in line.replace(" ", ""):  # Remove hidden inputs from the dictionary
            for list_item in line.strip().split():
                # print(list_item)
                line_dict[subsequent_key] = list_item
                subsequent_key += 1
            subsequent_line_dict[line_number] = line_dict
            line_number += 1

        # print(subsequent_line_dict)

        # for row in subsequent_line_dict:
        #     print(subsequent_line_dict[row].values())

    return first_line_dict, subsequent_line_dict  # Return both variables using tuple returns.

def check_grid(first_line_dict, subsequent_line_dict):
    first_line = list(first_line_dict)
    line_list = []
    for row in subsequent_line_dict:
        value = list(subsequent_line_dict[row].values())
        line_list.append(value)

    line_list.insert(0, first_line)  # Insert the header row at index 0 of the data grid as list form.
    counts = []

    for i, row in enumerate(line_list):  # Iterate through the whole grid, giving them an index to allow for comparisons
        # in the length of each row by counting the difference in the counts 2d array.
        highest_point = len(row)
        counts.append(highest_point)

        if row != 0:
            if counts[i] > counts[i - 1]:
                col_diff = counts[i] - counts[i - 1]
                if col_diff > 1:
                    return f"Error at row {i + 1}! There is a column difference of {col_diff} extra columns.", False
                else:
                    return f"Error at row {i + 1}! There is a column difference of {col_diff} less columns.", False

    return "True result pass", True

# If the grid is a valid grid (e.g. equal in columns per row) we parse through each subsequent line dict as a dict
# using the header as its key to successfully write the data into our csv file using write.writerow
def save_to_csv(first_line, subsequent_line):
    temp = {}

    dict_key_number = 0
    for item in subsequent_line.items():
        key = 0
        new_dict = {}
        for length in first_line:
            new_dict[length] = subsequent_line[item[0]][key]
            key += 1
        temp[dict_key_number] = new_dict
        dict_key_number += 1

    try:
        with open('output.csv', 'w', newline='') as csvfile:
            fieldnames = first_line.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in temp.items():
                writer.writerow(value)
            print("Save successful!")
            return
    except Exception as e:
        print(f"Error saving file! Error: {e}")

# These steps are necessary as we are not parsing through a filename class file like main.py using wtforms.
# We manually read the file and save its output as a list under line_list for testing purposes.
try:
    file = open(url, 'r')
    data = file.read()
except FileNotFoundError as e:
    print(e)

first_line_dict, subsequent_line_dict = url_check(data)

file = list(first_line_dict)
line_list = []
for row in subsequent_line_dict:
    value = list(subsequent_line_dict[row].values())
    line_list.append(value)

line_list.insert(0, file)  # Insert the header row at index 0 of the data grid as list form.

counts = []

# print(check_grid(first_line_dict, subsequent_line_dict))
string_return_result, grid_validation_result = check_grid(first_line_dict, subsequent_line_dict)


if grid_validation_result:
    save_to_csv(first_line_dict, subsequent_line_dict)
else:
    print('error')


# print(first_line_dict)
# print(subsequent_line_dict)







# with open('output.csv', 'w', newline='') as csvfile:
#     fieldnames = first_line_dict.keys()
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for row in subsequent_line_dict:
#         writer.writerow(subsequent_line_dict[row])
