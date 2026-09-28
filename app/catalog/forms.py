from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import Optional, NumberRange, DataRequired

CATEGORY_CHOICES = [
    ("", "All Categories"),
    ("tops", "Tops"),
    ("jeans", "Jeans"),
    ("dresses", "Dresses"),
    ("jackets", "Jackets"),
    ("shorts", "Shorts"),
]


class SearchForm(FlaskForm):
    """Product search and filter form."""

    q = StringField("Search", validators=[Optional()])
    category = SelectField(
        "Category", choices=CATEGORY_CHOICES, validators=[Optional()]
    )
    submit = SubmitField("Search")

    class Meta:
        csrf = False  # safe GET form


class MeasurementForm(FlaskForm):
    """User body measurement input form (all values in cm)."""

    chest = FloatField(
        "Chest (cm)",
        validators=[
            DataRequired(),
            NumberRange(min=60, max=160, message="Enter a value between 60-160 cm."),
        ],
    )
    waist = FloatField(
        "Waist (cm)",
        validators=[
            DataRequired(),
            NumberRange(min=50, max=140, message="Enter a value between 50-140 cm."),
        ],
    )
    hip = FloatField(
        "Hip (cm)",
        validators=[
            DataRequired(),
            NumberRange(min=70, max=170, message="Enter a value between 70-170 cm."),
        ],
    )
    submit = SubmitField("Save Measurements")
