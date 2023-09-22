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
    first_line_dict = {}
    subsequent_line_dict = {}

    if form.validate_on_submit():
        uploaded_file = form.file.data

        if not uploaded_file:
            return "No files were uploaded"

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

                # subsequent_line_dict[subsequent_key] = line
                # subsequent_key += 1

            for row in subsequent_line_dict:
                print(subsequent_line_dict[row].values())

            with open('output.csv', 'w', newline='') as csvfile:
                fieldnames = first_line_dict.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in subsequent_line_dict:
                    writer.writerow(subsequent_line_dict[row])


    return render_template("index.html", form_template=form)

# def export_file():
#     folder = request.files['folderInput']



if __name__ == "__main__":
    app.run(debug=True)