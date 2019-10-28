#!/usr/bin/env python3
from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

G_CustomerInformation_List = []

app = Flask(__name__)
app.config["SECRET_KEY"] = "devvv"
bootstrap = Bootstrap(app)


class CustomerInformationForm(FlaskForm):
    Firstname = StringField(label='Firstname', validators=[DataRequired()])
    Lastname = StringField(label='Lastname', validators=[DataRequired()])
    # DateOfBirth = DateField(label='DateOfBirth', validators=[DataRequired()])
    DateOfBirth = StringField(label='DateOfBirth', validators=[DataRequired()])
    TraveldocumentNumber = StringField(label='TraveldocumentNumber', validators=[DataRequired()])
    # Sex = SelectField(label='Sex', validators=[DataRequired()], choices=[(1, '男'), (2, '女')], default=2, coerce=int)
    Sex = StringField(label='Sex', validators=[DataRequired()], default='2')
    Street = StringField(label='Street', validators=[DataRequired()])
    Postcode = StringField(label='Postcode', validators=[DataRequired()])
    City = StringField(label='City', validators=[DataRequired()])
    Country = StringField(label='Country', validators=[DataRequired()], default='46')
    Telephone = StringField(label='Telephone', validators=[DataRequired()])
    Email = StringField(label='Email', validators=[DataRequired()])
    LastnameAtBirth = StringField(label='LastnameAtBirth', validators=[DataRequired()])
    NationalityAtBirth = StringField(label='NationalityAtBirth', validators=[DataRequired()], default='49')
    CountryOfBirth = StringField(label='CountryOfBirth', validators=[DataRequired()], default='49')
    PlaceOfBirth = StringField(label='PlaceOfBirth', validators=[DataRequired()])
    NationalityForApplication = StringField(label='NationalityForApplication', validators=[DataRequired()],
                                            default='49')
    TraveldocumentDateOfIssue = StringField(label='TraveldocumentDateOfIssue', validators=[DataRequired()])
    TraveldocumentValidUntil = StringField(label='TraveldocumentValidUntil', validators=[DataRequired()])
    TraveldocumentIssuingAuthority = StringField(label='TraveldocumentIssuingAuthority', validators=[DataRequired()],
                                                 default='49')

    submit = SubmitField('submit', validators=[DataRequired()])


@app.route('/clear')
def clear():
    global G_CustomerInformation_List
    G_CustomerInformation_List = []


@app.route('/baidu_ocr_client')
def baidu_ocr_client():
    return 'None'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CustomerInformationForm()
    if form.validate_on_submit():
        global G_CustomerInformation_List
        p = {
            'Firstname': form.Firstname.data,
            'Lastname': form.Lastname.data,
            'DateOfBirth': form.DateOfBirth.data,
            'TraveldocumentNumber': form.TraveldocumentNumber.data,
            'Sex': form.Sex.data,
            'Street': form.Street.data,
            'Postcode': form.Postcode.data,
            'City': form.City.data,
            'Country': form.Country.data,
            'Telephone': form.Telephone.data,
            'Email': form.Email.data,
            'LastnameAtBirth': form.LastnameAtBirth.data,
            'NationalityAtBirth': form.NationalityAtBirth.data,
            'CountryOfBirth': form.CountryOfBirth.data,
            'PlaceOfBirth': form.PlaceOfBirth.data,
            'NationalityForApplication': form.NationalityForApplication.data,
            'TraveldocumentDateOfIssue': form.TraveldocumentDateOfIssue.data,
            'TraveldocumentValidUntil': form.TraveldocumentValidUntil.data,
            'TraveldocumentIssuingAuthority': form.TraveldocumentIssuingAuthority.data,
        }
        G_CustomerInformation_List.append(p)
        return 'success'
    else:
        return render_template('index.html', form=form)


@app.route('/customer_information')
def customer_information():
    return jsonify(G_CustomerInformation_List)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)
    pass
