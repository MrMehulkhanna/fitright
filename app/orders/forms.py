from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL']


class OrderForm(FlaskForm):
    """Place an order form."""
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    size = SelectField(
        'Size',
        choices=[(s, s) for s in SIZES],
        validators=[DataRequired()]
    )
    submit = SubmitField('Place Order')


class ReturnForm(FlaskForm):
    """Submit a return request."""
    reason = SelectField(
        'Reason',
        choices=[
            ('too_small', 'Too Small'),
            ('too_large', 'Too Large'),
            ('quality', 'Quality Issue'),
            ('other', 'Other'),
        ],
        validators=[DataRequired()]
    )
    note = TextAreaField(
        'Additional Notes',
        validators=[Optional(), Length(max=500)]
    )
    submit = SubmitField('Submit Return')
