from flask import Flask, render_template, request, flash
from forms import UploadForm
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
ALLOWED_EXTENSIONS = {'txt'}  # Include the extensions that are allowed to be processed by the code.
# Currently only at txt


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data

        if not uploaded_file:
            return "No files were uploaded"

        # Return the information for the header row and its subsequent rows using tuple returns.
        first_line_dict, subsequent_line_dict = url_check(uploaded_file)

        # Check that the grid is  valid, and return it's boolean result and its string result for later code.
        string_return_result, grid_validation_result = check_grid(first_line_dict, subsequent_line_dict)

        if not grid_validation_result:
            return None
        else:
            print(string_return_result)
            save_to_csv(first_line_dict, subsequent_line_dict)

    return render_template("index.html", form_template=form)

# def export_file():
#     folder = request.files['folderInput']


def url_check(uploaded_file):
    first_line_dict = {}
    subsequent_line_dict = {}
    split_url = uploaded_file.filename.split(".")

    if split_url[-1].lower() in ALLOWED_EXTENSIONS:
        first_line = uploaded_file.readline().decode('utf-8').split(" ")  # Remove all white spaces inbetween
        # each character in the heading
        subsequent_line = uploaded_file.read().decode('utf-8').splitlines()  # Remove all white
        # spaces inbetween each character in the heading

        first_key = 0
        for value in first_line:  # Removes hidden newline characters from being inputted into the
            # dictionary keys
            stripped_value = value.strip()
            first_line_dict[stripped_value] = first_key
            first_key += 1

        line_number = 0
        for line in subsequent_line:
            line_dict = {}
            subsequent_key = 0
            for list_item in line.strip().split():  # Remove white spaces between each String
                line_dict[subsequent_key] = list_item
                subsequent_key += 1
            subsequent_line_dict[line_number] = line_dict
            line_number += 1

        # Test to see that the code is correctly saving the subsequent list items.
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

    return "Data grid is OK", True


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


if __name__ == "__main__":
    app.run(debug=True)