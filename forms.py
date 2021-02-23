from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length

"""Forms for SpeadEats"""

class UserForm(FlaskForm):
    """Form for adding or editing users"""

    email = StringField('Email',
        validators=[DataRequired()])
    password = PasswordField('Password',
        validators=[DataRequired(),
            Length(min=8,
                message='Password must be at least 8 characters long')])
    name = StringField('Name', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Form to log in a user"""
    
    email = StringField('Email',
        validators=[DataRequired()])
    password = PasswordField('Password',
        validators=[DataRequired()])

class AddMemberForm(FlaskForm):
    """Add youself to a party"""

    party_id = IntegerField("Party Id", validators=[DataRequired()])

class PartyForm(FlaskForm):
    """Create or edit a party"""

    name = StringField("Name",
                validators=[DataRequired()])
    address = StringField("Address",
                validators=[DataRequired()])
    city = StringField("City",
                validators=[DataRequired()])
    state = StringField("State",
                validators=[DataRequired()])
    zip_code = IntegerField("Zip Code",
                validators=[DataRequired()])

class VoteForm(FlaskForm):

    yay_or_nay = BooleanField("I'd Eat Here!")

class VoteAgainForm(FlaskForm):

    include_same = BooleanField("Use the winners from this round")

    add_new = IntegerField("Add __ new resturaunts", default=0)