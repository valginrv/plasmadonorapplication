from flask import Flask,request, render_template, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from base64 import b64encode, b64decode
import jinja2
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" +os.path.join(basedir,'plasmadonor.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Register(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email =db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.Integer, nullable = False, unique = True)
    date_joined = db.Column(db.Date,default = datetime.utcnow)

    def __repr__(self):
        return f"<User : {self.email}>"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    password = db.Column(db.Integer, nullable = False, unique = True)

    def __repr__(self):
        return f"<User : {self.name}>"
class Donor_Registrations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    age = db.Column(db.Integer, nullable=False)
    bloodgroup = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    contactnumber = db.Column(db.Integer, nullable=False)
    alternativenumber = db.Column(db.Integer, nullable=False)
    whatsappnumber = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    location = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(50), nullable=False)
    covidstatus= db.Column(db.String(50), nullable=False)
    covidvaccinationstatus = db.Column(db.String(50), nullable=False)
    covidvaccinationdose = db.Column(db.String(50), nullable=False)
    druguser = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.String(150), nullable=False)
    verified = db.Column(db.String(50),nullable=False)


    def __repr__(self):
        return f"<User : {self.email}>"

with app.app_context():

    db.create_all()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/donorregistration')
def donorregister():
    return render_template('registration.html')


@app.route('/admin.html')
def admin_page():
    query = Donor_Registrations.query.order_by(Donor_Registrations.name).all()
    print(query)
    return render_template("admin.html", posts=query)

   #return render_template("admin.html")

@app.route('/register_login',methods = ['GET','POST'])
def register_login():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']


        query = Register(name = name, email = email, password = password)
        db.session.add(query)
        db.session.commit()
        return render_template('index.html')

@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        login = Register.query.filter_by(email=email, password = password).first()
        #query = Admin(email='admin@gmail.com',password= "admin")
        #db.session.add(query)
        # db.session.commit()
        if login  is not None:
            return render_template('index.html', login_data= email)
        elif Admin is not None:
            return redirect('admin.html')
            #pass
        else:
            return render_template('login.html', login_data="make sure u enter the coorrect pasword")

@app.route('/donor',methods=['GET','POST'])
def donor():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        bloodgroup = request.form['bloodgroup']
        gender =request.form['gender']
        contactnumber =request.form['contactnumber']
        alternativenumber =request.form['alternativenumber']
        whatsappnumber =request.form['whatsappnumber']
        email=request.form['email']
        location =request.form['location']
        address =request.form['address']
        state = request.form['state']
        city =request.form['city']
        occupation = request.form['occupation']
        covidstatus = request.form['covidstatus']
        covidvaccinationstatus = request.form['covidvaccinationstatus']
        covidvaccinationdose = request.form['covidvaccinationdose']
        druguser = request.form['druguser']
        comments = request.form['comments']
        verified = "notverified"
        query = Donor_Registrations(name=name,  age=age, bloodgroup=bloodgroup, gender=gender, contactnumber=contactnumber, alternativenumber=alternativenumber, whatsappnumber=whatsappnumber, email=email, location=location, address= address,
                         state=state, city=city, occupation=occupation, covidstatus=covidstatus, covidvaccinationstatus=covidvaccinationstatus, covidvaccinationdose=covidvaccinationdose, druguser=druguser, comments=comments, verified=verified)
        db.session.add(query)
        db.session.commit()
        return render_template('index.html', res = "succesfully")

@app.route('/searchbar', methods=['GET','POST'])
def searchbar():
    return render_template("search.html")

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search1 = request.form.get('bloodgroup')
        search2 = request.form.get('city')
        #query = Donor_Registration.query.filter(Donor_Registration.bloodgroup, city.like("%" + search1 + "%", "%" + search2 + "%")).all()
        query =Donor_Registrations.query.filter(Donor_Registrations.bloodgroup.like(search1),Donor_Registrations.city.like(search2))
        return render_template('search.html', posts=query)

@app.route('/deleteform',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        deleted = Donor_Registrations.query.get(id)
        db.session.delete(deleted)
        db.session.commit()
        return redirect('/admin.html')

@app.route('/updateform',methods = ['GET','POST'])
def updatedata():
    if request.method == 'POST':
        id = request.form['id']
        Donor_Registrations.query.filter_by(id = id).update(dict(verified="verified"))
        db.session.commit()
        return redirect('/admin.html')


if __name__ == '__main__':
    app.run(debug=True)