from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class charNForm(FlaskForm):
    races = [('Androids','Androids'),('Humans', 'Humans'),('Kasathas', 'Kasathas'),('Lashuntas', 'Lashuntas'), ('Shirrens', 'Shirrens'),('Vesk', 'Vesk'), ('Ysoki', 'Ysoki')]
    gender = [('Male', 'Male'), ('Female', 'Female')]
    charN = StringField('Character Name', validators=[DataRequired()])
    race = SelectField('Race', choices=races)
    gender = SelectField('Gender', choices=gender)
    submit = SubmitField('Next Step')

class charThemeForm(FlaskForm):
    themes = [('Ace Pilot', 'Ace Pilot'), ('Priest', 'Priest'), ('Bounty Hunter', 'Bounty Hunter'), ('Scholar', 'Scholar'), ('Icon', 'Icon'), ('Spacefarer', 'Spacefarer'), ('Mercenary', 'Mercenary'), ('Xenoseeker', 'Xenoseeker'), ('Outlaw', 'Outlaw'), ('Themeless', 'Themeless')]
    theme = SelectField('Themes', choices=themes)
    submit = SubmitField('Next Step')

class charClassForm(FlaskForm):
    classes = [('Envoy', 'Envoy'), ('Solarian', 'Solarian'), ('Mechanic', 'Mechanic'), ('Soldier', 'Soldier'),
               ('Mystic', 'Mystic'), ('Technomancer', 'Technomancer'), ('Operative', 'Operative')]
    charCls = SelectField('Classes', choices=classes)
    submit = SubmitField('Roll Attributes')