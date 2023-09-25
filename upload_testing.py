# Python code for the purposes of testing the upload methods.
# Created due to having to upload the specific text file manually through the form for every testing scenario which
# caused a tedious way to work with the methods.
# Danny Kim 25/09/2023
import csv

url = ""
ALLOWED_EXTENSIONS = {"txt"}


def url_check(uploaded_file):
    first_line_dict = {}
    subsequent_line_dict = {}
    split_url = url.split(".")  # Adjusted code to main due to using a hardcoded url
    # print(uploaded_file)

    if split_url[-1].lower() in ALLOWED_EXTENSIONS:  # Split code between header and subsequent data lines
        data_split = uploaded_file.splitlines()
        first_line = data_split[0].replace(" ", "")
        subsequent_line = data_split[1:]
        # first_line = uploaded_file.readline().decode('utf-8').replace(" ", "")  # Remove all white spaces inbetween
        # # each character in the heading
        # subsequent_line = uploaded_file.read().decode('utf-8').replace(" ", "").splitlines()  # Remove all white
        # # spaces inbetween each character in the heading

        first_key = 0
        for char in first_line.strip():  # Removes hidden newline characters from being inputted into the
            # dictionary keys
            first_line_dict[char] = first_key
            first_key += 1

        line_number = 0
        for line in subsequent_line:
            line_dict = {}
            subsequent_key = 0
            for char in line.replace(" ", ""):  # Remove hidden inputs from the dictionary
                line_dict[subsequent_key] = char
                subsequent_key += 1
            subsequent_line_dict[line_number] = line_dict
            line_number += 1

        # for row in subsequent_line_dict:
        #     print(subsequent_line_dict[row].values())

    return first_line_dict, subsequent_line_dict  # Return both variables using tuple returns.


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

for i, row in enumerate(line_list):  # Iterate through the whole grid, giving them an index to allow for comparisons
    # in the length of each row by counting the difference in the counts 2d array.
    highest_point = len(row)
    counts.append(highest_point)

    if row != 0:
        if counts[i] > counts[i - 1]:
            col_diff = counts[i] - counts[i - 1]
            if col_diff > 1:
                print(f"Error at row {i + 1}! There is a column difference of {col_diff} extra columns.")
            else:
                print(f"Error at row {i + 1}! There is a column difference of {col_diff} less columns.")


# with open('output.csv', 'w', newline='') as csvfile:
#     fieldnames = first_line_dict.keys()
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for row in subsequent_line_dict:
#         writer.writerow(subsequent_line_dict[row])

    # with open('output.csv', 'w', newline='') as csvfile:
    #     fieldnames = first_line_dict.keys()
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for row in subsequent_line_dict:
    #         writer.writerow(subsequent_line_dict[row])