from flask import Flask, render_template, send_file
from forms import UploadForm
from io import BytesIO
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'
# Include the extensions that are allowed to be processed by the code. Currently only at txt
ALLOWED_EXTENSIONS = {'txt'}


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
            # Prepare the data as a CSV using a BytesIO buffer, then send the file for download using Flask send_file.
            save_to_csv(first_line_dict, subsequent_line_dict)

    return render_template("index.html", form_template=form)

# def export_file():
#     folder = request.files['folderInput']


def url_check(uploaded_file):
    first_line_dict = {}
    subsequent_line_dict = {}
    split_url = uploaded_file.filename.split(".")

    if split_url[-1].lower() in ALLOWED_EXTENSIONS:
        # Remove all white spaces inbetween each character in the heading
        first_line = uploaded_file.readline().decode('utf-8').split(" ")
        # Remove all white spaces inbetween each character in the heading
        subsequent_line = uploaded_file.read().decode('utf-8').splitlines()

        first_key = 0
        for value in first_line:
            # Removes hidden newline characters from being inputted into the
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

    # Return both variables using tuple returns.
    return first_line_dict, subsequent_line_dict


def check_grid(first_line_dict, subsequent_line_dict):
    first_line = list(first_line_dict)
    line_list = []
    for row in subsequent_line_dict:
        value = list(subsequent_line_dict[row].values())
        line_list.append(value)

    # Insert the header row at index 0 of the data grid as list form.
    line_list.insert(0, first_line)

    counts = []

    # Iterate through the whole grid, giving them an index to allow for comparisons
    # in the length of each row by counting the difference in the counts 2d array.
    for i, row in enumerate(line_list):
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



    # try:
        # Create BytesIO buffer to maintain data in memory.
        buffer = BytesIO()
        # Get the keys of the first row dictionary from prior methods.
        fieldnames = first_line.keys()

        # Use the BytesIO buffer via the context manager to write the file to.
        # try:
        with buffer as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # for key, value in temp.items():
            #     encoded_value = value.encode('utf-8')
            #     writer.writerow(encoded_value)
            for key, value in temp.items():
                # Encode the entire row as bytes and write it to the CSV file.
                encoded_row = {k: v.encode('utf-8') for k, v in value.items()}
                writer.writerow(encoded_row)
        # except Exception as e:
        #     print(f"ERRRORRRRR {e}")

        # File buffer has been moved after writing our file. Therefore, we need to point the buffer back to the
        # beginning to ensure that we send the whole file.
        buffer.seek(0)

        # send_file is a Flask function that sends a file as response to a client (e.g. user's browser)
        return send_file(
            buffer,
            as_attachment=True, # For the user to download the file rather than on a browser window.
            download_name="output.csv", # Name of the download.
            mimetype="text/csv" # MIME type to indicate it will be a text as its primary type and csv as its secondary
        )
    # except Exception as e:
    #     print(f"Error saving file! Error: {e}")


if __name__ == "__main__":
    app.run(debug=True)