from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm


class UploadForm(FlaskForm):
    file = FileField("Upload your file!")
    submit = SubmitField("Submit")