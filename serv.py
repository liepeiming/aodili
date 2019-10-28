#!/usr/bin/env python3
import sys
import os
import queue
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model

basedir = os.path.realpath(os.path.dirname(__file__))
prefix = "sqlite:///" if sys.platform.startswith("win") else "sqlite:////"
print(prefix + os.path.join(basedir, "data.db"))

app = Flask(__name__)
app.config["SECRET_KEY"] = "devvv"
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(basedir, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False, index=True, nullable=False)

    CalendarType = db.Column(db.String(8), index=True, nullable=False)
    CalendarId = db.Column(db.String(7), index=True, nullable=False)
    StartTime = db.Column(db.String(255), nullable=False)
    Firstname = db.Column(db.String(32), nullable=False)
    Lastname = db.Column(db.String(32), nullable=False)
    DateOfBirth = db.Column(db.String(10), nullable=False)
    TraveldocumentNumber = db.Column(db.String(9), index=True, nullable=False)
    Sex = db.Column(db.String(1), nullable=False)
    Street = db.Column(db.String(255), nullable=False)
    Postcode = db.Column(db.String(10), nullable=False)
    City = db.Column(db.String(10), nullable=False)
    Country = db.Column(db.String(255), nullable=False)
    Telephone = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    LastnameAtBirth = db.Column(db.String(255), nullable=False)
    NationalityAtBirth = db.Column(db.String(255), nullable=False)
    CountryOfBirth = db.Column(db.String(255), nullable=False)
    PlaceOfBirth = db.Column(db.String(255), nullable=False)
    NationalityForApplication = db.Column(db.String(255), nullable=False)
    TraveldocumentDateOfIssue = db.Column(db.String(255), nullable=False)
    TraveldocumentValidUntil = db.Column(db.String(255), nullable=False)
    TraveldocumentIssuingAuthority = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Client {self.TraveldocumentNumber}>"

    def to_dict(self):
        return {
            "CalendarType": self.CalendarType,
            "CalendarId": self.CalendarId,
            "StartTime": self.StartTime,
            "Firstname": self.Firstname,
            "Lastname": self.Lastname,
            "DateOfBirth": self.DateOfBirth,
            "TraveldocumentNumber": self.TraveldocumentNumber,
            "Sex": self.Sex,
            "Street": self.Street,
            "Postcode": self.Postcode,
            "City": self.City,
            "Country": self.Country,
            "Telephone": self.Telephone,
            "Email": self.Email,
            "LastnameAtBirth": self.LastnameAtBirth,
            "NationalityAtBirth": self.NationalityAtBirth,
            "CountryOfBirth": self.CountryOfBirth,
            "PlaceOfBirth": self.PlaceOfBirth,
            "NationalityForApplication": self.NationalityForApplication,
            "TraveldocumentDateOfIssue": self.TraveldocumentDateOfIssue,
            "TraveldocumentValidUntil": self.TraveldocumentValidUntil,
            "TraveldocumentIssuingAuthority": self.TraveldocumentIssuingAuthority,
        }


class BaiduOCRClient(db.Model):
    __tablename__ = "baidu_ocr_client"

    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False, index=True, nullable=False)

    APP_ID = db.Column(db.String(8), unique=True, nullable=False)
    API_KEY = db.Column(db.String(24), index=True, nullable=False)
    SECRET_KEY = db.Column(db.String(32), index=True, nullable=False)

    def __repr__(self):
        return f"<BaiduOCRClient {self.APP_ID} {self.API_KEY} {self.SECRET_KEY}>"

    def to_dict(self):
        return {
            "APP_ID": self.APP_ID,
            "API_KEY": self.API_KEY,
            "SECRET_KEY": self.SECRET_KEY,
        }


db.create_all()


class ClientForm(FlaskForm):
    # 北京 / 上海 使领馆
    CalendarId = SelectField(
        label="使领馆",
        validators=[DataRequired("请选择使领馆")],
        render_kw={"class": "form-control"},
        choices=[
            ("7226345", "PEKING"),
            ("SHANGHAI", "SHANGHAI"),
            ("1213873", "PEKING(演示)"),
            ("950653", "SHANGHAI(演示)"),
            #         ('ABUJA', 'ABUJA'), ('ADDIS-ABEBA', 'ADDIS-ABEBA'), ('ALGIER', 'ALGIER'), ('AMMAN', 'AMMAN'),
            #         ('ANKARA', 'ANKARA'), ('ASTANA', 'ASTANA'), ('BAKU', 'BAKU'), ('BANGKOK', 'BANGKOK'),
            #         ('BEIRUT', 'BEIRUT'), ('BRUESSEL', 'BRUESSEL'), ('BUENOS-AIRES', 'BUENOS-AIRES'), ('DAKAR', 'DAKAR'),
            #         ('DAMASKUS', 'DAMASKUS'), ('DEN-HAAG', 'DEN-HAAG'), ('DSCHIBUTI', 'DSCHIBUTI'), ('DUBLIN', 'DUBLIN'),
            #         ('HANOI', 'HANOI'), ('HONGKONG', 'HONGKONG'), ('ISLAMABAD', 'ISLAMABAD'), ('ISTANBUL', 'ISTANBUL'),
            #         ('JAKARTA', 'JAKARTA'), ('KAIRO', 'KAIRO'), ('KIEW', 'KIEW'), ('KOPENHAGEN', 'KOPENHAGEN'),
            #         ('KUALA-LUMPUR', 'KUALA-LUMPUR'), ('KUWAIT', 'KUWAIT'), ('LONDON', 'LONDON'),
            #         ('LOS-ANGELES', 'LOS-ANGELES'), ('MANILA', 'MANILA'), ('MEXIKO', 'MEXIKO'), ('MOSKAU', 'MOSKAU'),
            #         ('MUENCHEN', 'MUENCHEN'), ('NAIROBI', 'NAIROBI'), ('NEW-DELHI', 'NEW-DELHI'), ('NEW-YORK', 'NEW-YORK'),
            #         ('OTTAWA', 'OTTAWA'), ('PARIS', 'PARIS'), ('PRESSBURG', 'PRESSBURG'),
            #         ('PRETORIA', 'PRETORIA'), ('PRISTINA', 'PRISTINA'), ('RABAT', 'RABAT'), ('RIYADH', 'RIYADH'),
            #         ('SEOUL', 'SEOUL'), ('SKOPJE', 'SKOPJE'),
            #         ('STOCKHOLM', 'STOCKHOLM'), ('TEHERAN', 'TEHERAN'), ('TEL-AVIV', 'TEL-AVIV'), ('TOKIO', 'TOKIO'),
            #         ('TRIPOLIS', 'TRIPOLIS'), ('TUNIS', 'TUNIS'), ('WASHINGTON', 'WASHINGTON'),
        ],
        default="PEKING(演示)",
        coerce=str,
    )
    # 抢预约的时间
    # Times = SelectMultipleField(
    #     label='请选择预约时间(按住 Ctrl (windows) / Command (Mac) 按钮来选择多个选项)',
    #     validators=[DataRequired('请选择您要预约的时间')],
    #     coerce=str,
    #     choices=[('11/11/2019 10:00', '11/11/2019 10:00'), ('11/11/2019 10:20', '11/11/2019 10:20'),
    #              ('11/11/2019 10:40', '11/11/2019 10:40'), ('11/11/2019 11:00', '11/11/2019 11:00')],
    #     description='预约的时间',
    #     render_kw={'class': 'form-control', 'size': 4},
    # )
    StartTime = StringField(
        label='起始时间[可填写多个,用逗号+空格", "隔开] (如 8/10/201910:20, 8/10/2019 10:40, 8/10/2019 11:00)'
    )

    Firstname = StringField(label="姓", validators=[DataRequired()])
    Lastname = StringField(label="名", validators=[DataRequired()])
    # DateOfBirth = DateField(label='DateOfBirth', validators=[DataRequired()])
    DateOfBirth = StringField(
        label="出生日期 tt.mm.jjjj按此格式填写日期(如 15/3/2016)", validators=[DataRequired()]
    )
    TraveldocumentNumber = StringField(label="护照号码", validators=[DataRequired()])
    Sex = SelectField(
        label="性别",
        validators=[DataRequired()],
        choices=[
            ("1", "Male"),
            ("2", "Female"),
            ("4", "Not Applicable"),
            ("3", "Unknown"),
        ],
        render_kw={"class": "form-control"},
        default="1",
        coerce=str,
    )
    Street = StringField(label="地址", validators=[DataRequired()])
    Postcode = StringField(label="邮编", validators=[DataRequired()])
    City = StringField(label="城市", validators=[DataRequired()])
    Country = StringField(label="国家", validators=[DataRequired()], default="46")
    Telephone = StringField(label="电话号码", validators=[DataRequired()])
    Email = StringField(label="电子邮箱", validators=[DataRequired()])
    LastnameAtBirth = StringField(label="出生时的姓氏", validators=[DataRequired()])
    NationalityAtBirth = StringField(
        label="出生时的国籍", validators=[DataRequired()], default="49"
    )
    CountryOfBirth = StringField(
        label="出生所在国", validators=[DataRequired()], default="49"
    )
    PlaceOfBirth = StringField(label="出生地点", validators=[DataRequired()])
    NationalityForApplication = StringField(
        label="现在的国籍", validators=[DataRequired()], default="49"
    )
    TraveldocumentDateOfIssue = StringField(
        label="护照签发时间 tt.mm.jjjj按此格式填写日期(如 15/3/2016)", validators=[DataRequired()]
    )
    TraveldocumentValidUntil = StringField(
        label="护照有效期 tt.mm.jjjj按此格式填写日期(如 15/3/2016)", validators=[DataRequired()]
    )
    TraveldocumentIssuingAuthority = SelectField(
        label="护照签发机关",
        validators=[DataRequired()],
        choices=[("49", "CHINA")],
        default="49",
        coerce=str,
    )


@app.route("/", methods=["GET", "POST", "DELETE"])
def index():
    form = ClientForm()
    method = request.method
    if method == "POST":
        CalendarId = form.CalendarId.data
        StartTime = form.StartTime.data
        Firstname = form.Firstname.data
        Lastname = form.Lastname.data
        DateOfBirth = form.DateOfBirth.data
        TraveldocumentNumber = form.TraveldocumentNumber.data
        Sex = form.Sex.data
        Street = form.Street.data
        Postcode = form.Postcode.data
        City = form.City.data
        Country = form.Country.data
        Telephone = form.Telephone.data
        Email = form.Email.data
        LastnameAtBirth = form.LastnameAtBirth.data
        NationalityAtBirth = form.NationalityAtBirth.data
        CountryOfBirth = form.CountryOfBirth.data
        PlaceOfBirth = form.PlaceOfBirth.data
        NationalityForApplication = form.NationalityForApplication.data
        TraveldocumentDateOfIssue = form.TraveldocumentDateOfIssue.data
        TraveldocumentValidUntil = form.TraveldocumentValidUntil.data
        TraveldocumentIssuingAuthority = form.TraveldocumentIssuingAuthority.data
        if form.validate():
            client = Client.query.filter_by(
                TraveldocumentNumber=TraveldocumentNumber
            ).first()
            if client:
                client.CalendarId = CalendarId
                client.CalendarType = 'PEKING' if CalendarId == '1213873' or CalendarId == '1213936' or CalendarId == '7226345' else 'SHANGHAI'
                client.StartTime = StartTime
                client.Firstname = Firstname
                client.Lastname = Lastname
                client.DateOfBirth = DateOfBirth
                # client.TraveldocumentNumber = TraveldocumentNumber
                client.Sex = Sex
                client.Street = Street
                client.Postcode = Postcode
                client.City = City
                client.Country = Country
                client.Telephone = Telephone
                client.Email = Email
                client.LastnameAtBirth = LastnameAtBirth
                client.NationalityAtBirth = NationalityAtBirth
                client.CountryOfBirth = CountryOfBirth
                client.PlaceOfBirth = PlaceOfBirth
                client.NationalityForApplication = NationalityForApplication
                client.TraveldocumentDateOfIssue = TraveldocumentDateOfIssue
                client.TraveldocumentValidUntil = TraveldocumentValidUntil
                client.TraveldocumentIssuingAuthority = TraveldocumentIssuingAuthority
            else:
                db.session.add(
                    Client(
                        CalendarId=CalendarId,
                        CalendarType='PEKING' if CalendarId == '1213873' or CalendarId == '1213936' or CalendarId == '7226345' else 'SHANGHAI',
                        StartTime=StartTime,
                        Firstname=Firstname,
                        Lastname=Lastname,
                        DateOfBirth=DateOfBirth,
                        TraveldocumentNumber=TraveldocumentNumber,
                        Sex=Sex,
                        Street=Street,
                        Postcode=Postcode,
                        City=City,
                        Country=Country,
                        Telephone=Telephone,
                        Email=Email,
                        LastnameAtBirth=LastnameAtBirth,
                        NationalityAtBirth=NationalityAtBirth,
                        CountryOfBirth=CountryOfBirth,
                        PlaceOfBirth=PlaceOfBirth,
                        NationalityForApplication=NationalityForApplication,
                        TraveldocumentDateOfIssue=TraveldocumentDateOfIssue,
                        TraveldocumentValidUntil=TraveldocumentValidUntil,
                        TraveldocumentIssuingAuthority=TraveldocumentIssuingAuthority,
                    )
                )
            db.session.commit()
            return redirect(url_for("index"))
        else:
            flash("表单信息不正确,请认真检查", "warning")
            form.CalendarId.data = CalendarId
            form.StartTime.data = StartTime
            form.Firstname.data = Firstname
            form.Lastname.data = Lastname
            form.DateOfBirth.data = DateOfBirth
            form.TraveldocumentNumber.data = TraveldocumentNumber
            form.Sex.data = Sex
            form.Street.data = Street
            form.Postcode.data = Postcode
            form.City.data = City
            form.Country.data = Country
            form.Telephone.data = Telephone
            form.Email.data = Email
            form.LastnameAtBirth.data = LastnameAtBirth
            form.NationalityAtBirth.data = NationalityAtBirth
            form.CountryOfBirth.data = CountryOfBirth
            form.PlaceOfBirth.data = PlaceOfBirth
            form.NationalityForApplication.data = NationalityForApplication
            form.TraveldocumentDateOfIssue.data = TraveldocumentDateOfIssue
            form.TraveldocumentValidUntil.data = TraveldocumentValidUntil
            form.TraveldocumentIssuingAuthority = TraveldocumentIssuingAuthority

    elif method == "DELETE":
        TraveldocumentNumber = (
            request.json.get("TraveldocumentNumber", None)
            if request.json
            else request.args.get("TraveldocumentNumber", None)
            if request.args
            else request.form.get("TraveldocumentNumber", None)
            if request.form
            else None
        )
        if TraveldocumentNumber:
            client = Client.query.filter_by(
                TraveldocumentNumber=TraveldocumentNumber, deleted=False
            ).first()
            if client:
                client.deleted = True
                db.session.commit()
                return jsonify({"status": "ok"})
            else:
                return jsonify({"status": "err", "msg": "护照号码不正确"})
        else:
            return jsonify({"status": "err", "msg": "没收到您的护照号码"})

    return render_template("index.html", form=form)


@app.route("/clients", methods=["GET"])
def clients():
    clientGroup = Client.query.filter_by(deleted=False).all()
    return jsonify({
        "status": "ok",
        "data": {
            "PEKING": [client.to_dict() for client in clientGroup if client.CalendarType == 'PEKING'],
            "SHANGHAI": [client.to_dict() for client in clientGroup if client.CalendarType == 'SHANGHAI'],
        },
    })


@app.route("/baiduClients", methods=["GET", "POST"])
@app.route("/baiduClients/<int:number>")
@app.route("/baiduClients/<int:start>/<int:number>")
def baiduClients(start=0, number=5):
    if request.method == "POST":
        APP_ID = (
            request.json.get("APP_ID", None)
            if request.json
            else request.args.get("APP_ID", None)
            if request.args
            else request.form.get("APP_ID", None)
            if request.form
            else None
        )
        API_KEY = (
            request.json.get("API_KEY", None)
            if request.json
            else request.args.get("API_KEY", None)
            if request.args
            else request.form.get("API_KEY", None)
            if request.form
            else None
        )
        SECRET_KEY = (
            request.json.get("SECRET_KEY", None)
            if request.json
            else request.args.get("SECRET_KEY", None)
            if request.args
            else request.form.get("SECRET_KEY", None)
            if request.form
            else None
        )
        baidu_ocr_client = BaiduOCRClient.query.filter_by(APP_ID=APP_ID).first()
        if baidu_ocr_client:  # 存在则修改
            baidu_ocr_client.APP_ID = APP_ID
            baidu_ocr_client.API_KEY = API_KEY
            baidu_ocr_client.SECRET_KEY = SECRET_KEY
        else:  # 不存在则创建
            db.session.add(
                BaiduOCRClient(APP_ID=APP_ID, API_KEY=API_KEY, SECRET_KEY=SECRET_KEY)
            )
        db.session.commit()
        return jsonify({'status': 'ok'})
    else:
        baidu_ocr_clients = BaiduOCRClient.query.filter_by(deleted=False).all()
        len_baidu_ocr_clients = len(baidu_ocr_clients)
        if start > len_baidu_ocr_clients - 1 or number > len_baidu_ocr_clients:
            return jsonify({"status": "err"})
        return jsonify(
            {
                "status": "ok",
                "data": [
                    client.to_dict() for client in baidu_ocr_clients[start: start + number]
                ],
            }
        )


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
    pass
