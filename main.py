from flask import Flask, render_template, request
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

        first_line_dict, subsequent_line_dict = url_check(uploaded_file)  # Return the information for the header row
        # and its subsequent rows using tuple returns.


        result = check_grid(first_line_dict, subsequent_line_dict)

        if not result:
            return None

        with open('output.csv', 'w', newline='') as csvfile:
            fieldnames = first_line_dict.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in subsequent_line_dict:
                writer.writerow(subsequent_line_dict[row])

    return render_template("index.html", form_template=form)

# def export_file():
#     folder = request.files['folderInput']


def url_check(uploaded_file):
    first_line_dict = {}
    subsequent_line_dict = {}
    split_url = uploaded_file.filename.split(".")

    if split_url[-1].lower() in ALLOWED_EXTENSIONS:
        first_line = uploaded_file.readline().decode('utf-8').replace(" ", "")  # Remove all white spaces inbetween
        # each character in the heading
        subsequent_line = uploaded_file.read().decode('utf-8').replace(" ", "").splitlines()  # Remove all white
        # spaces inbetween each character in the heading

        first_key = 0
        for char in first_line.strip():  # Removes hidden newline characters from being inputted into the
            # dictionary keys
            first_line_dict[char] = first_key
            first_key += 1

        line_number = 0
        for line in subsequent_line:
            line_dict = {}
            subsequent_key = 0
            for char in line.strip():
                line_dict[subsequent_key] = char
                subsequent_key += 1
            subsequent_line_dict[line_number] = line_dict
            line_number += 1

        for row in subsequent_line_dict:
            print(subsequent_line_dict[row].values())

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
                    print(f"Error at row {i + 1}! There is a column difference of {col_diff} extra columns.")
                    return False
                else:
                    print(f"Error at row {i + 1}! There is a column difference of {col_diff} less columns.")
                    return False

    print("Data grid is OK")
    return True


if __name__ == "__main__":
    app.run(debug=True)