from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, number_range


class InterpolSearchForm(FlaskForm):
    forename = StringField('Имя:')
    name = StringField('Фамилия:', validators=[DataRequired(message='Поле не может быть пустым')])
    nationality = SelectField('Гражданство:', choices=[('RU', 'Russia'), ('US', 'United States')])
    sexId = SelectField('Пол:', choices=[('M', 'Male'), ('F', 'Female')])
    ageMin = IntegerField('Возраст от (мин. 20):', validators=[DataRequired(message='Поле не может быть пустым'),
                                                               number_range(min=20, max=120)])
    ageMax = IntegerField('Возраст до (макс. 120):', validators=[DataRequired(message='Поле не может быть пустым'),
                                                                 number_range(min=20, max=120)])
    submit = SubmitField('Искать!')
