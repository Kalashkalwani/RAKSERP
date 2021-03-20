import os
from datetime import timedelta

from flask import Flask, render_template, request, session, flash, redirect, url_for,send_file
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from fpdf import FPDF



app = Flask(__name__)
app.secret_key = "XY123jfjeioghhgohgh@jojjfog@#$%%^15555"
params = {}
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql://RAKSERP:softwareproject@RAKSERP.mysql.pythonanywhere-services.com/RAKSERP$NEWERP"
db = SQLAlchemy(app)

UPLOAD_FOLDER = r"/home/RAKSERP/mysite/static/upload/"
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.refresh_view = "relogin"
login_manager.needs_refresh_message = (u"session timeout, please re-login")
login_manager.needs_refresh_message_category = "info"
SQLALCHEMY_POOL_RECYCLE=90



@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes = 50)
    session.modified = True





# ************************************************************************************************************************
# database initialize


class Faculty(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'Faculty'

    S_No = db.Column(db.Integer,
                     primary_key=True, autoincrement=True)

    Name = db.Column(db.String,
                     nullable=False,
                     unique=False)
    Id = db.Column(db.String,
                   nullable=False,
                   unique=True)
    Post = db.Column(db.String(40),
                     unique=True,
                     nullable=False)
    Department = db.Column(db.String(200),
                           primary_key=False,
                           unique=False,
                           nullable=False)
    email = db.Column(db.String(200),
                      primary_key=False,
                      unique=False,
                      nullable=False)
    Qualification = db.Column(db.String(200),
                              primary_key=False,
                              unique=False,
                              nullable=False)
    Mobile_No = db.Column(db.Integer,
                          unique=False)

    member = db.Column(db.Integer,
                          unique=False)


    Password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)

    def set_password(self, password):
        """Create hashed password."""
        self.Password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.Password, password)

    def __repr__(self):
        return '<User {}>'.format(self.Name)

    def get_id(self):
           return (self.S_No)







class Student(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'Student'

    S_No= db.Column(db.Integer,
                    primary_key=True, autoincrement=True)
    Enroll_No = db.Column(db.String,
                           nullable=False,
                           unique=True)
    Name = db.Column(db.String,
                     nullable=False,
                     unique=False)
    Branch = db.Column(db.String(40),
                       unique=True,
                       nullable=False)
    Specialization = db.Column(db.String(200),
                               primary_key=False,
                               unique=False,
                               nullable=False)
    email = db.Column(db.String(200),
                      primary_key=False,
                      unique=False,
                      nullable=False)
    Mobile_No = db.Column(db.Integer,
                          unique=False)

    member = db.Column(db.Integer,
                          unique=False)

    Password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)

    Father_Name = db.Column(db.String(200),
                      primary_key=False,
                      unique=False,
                      nullable=False)
    DOB = db.Column(db.Date,
                          unique=False)
    Gender = db.Column(db.String(20),
                         primary_key=False,
                         unique=False,
                         nullable=False)

    Address = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)


    def set_password(self, password):
        """Create hashed password."""
        self.Password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.Password, password)

    def __repr__(self):
        return '<User {}>'.format(self.Name)

    def get_id(self):
           return (self.S_No)


    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)









class Course(UserMixin, db.Model):
    """Model for Courses ."""

    __tablename__ = 'Course'

    S_No = db.Column(db.Integer,
                    primary_key=True)

    Course_Name = db.Column(db.String(200),
                      primary_key=False,
                      unique=False,
                      nullable=False)
    Course_Code = db.Column(db.String,
                           nullable=False,
                           unique=True)



class Attendence(UserMixin, db.Model):
    """Model for Attendence of student."""

    __tablename__ = 'Attendence'

    SS_No = db.Column(db.Integer, db.ForeignKey(Student.S_No),
                      primary_key=True)

    FS_No = db.Column(db.Integer, db.ForeignKey(Faculty.S_No),
                      primary_key=False)

    Course_No = db.Column(db.Integer, db.ForeignKey(Course.S_No),
                          primary_key=True)

    Total_Classes_Held = db.Column(db.Integer,
                      nullable=False,
                      unique=False)
    Classes_Attended = db.Column(db.Integer,
                         nullable=False,
                         unique=False)

    Till_Date = db.Column(db.Date,
                    unique=False)

    Percentage = db.Column(db.Numeric(3, 1),
                           unique=False)

    def update(self, kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)











class Grades(UserMixin, db.Model):
    """Model for  Grades of student"""

    __tablename__ = 'Grades'

    SS_No = db.Column(db.Integer,db.ForeignKey(Student.S_No),
                     primary_key=True)

    FS_No = db.Column(db.Integer,db.ForeignKey(Faculty.S_No),
                     primary_key=False)

    Course_No = db.Column(db.Integer,db.ForeignKey(Course.S_No),
                primary_key=True)

    MST_1 = db.Column(db.Numeric(2,1),
                      unique=False)
    MST_2 = db.Column(db.Numeric(2,1),
                      unique=False)
    End_Sem = db.Column(db.Numeric(2, 1),
                      unique=False)
    Percentage = db.Column(db.Numeric(3, 2),
                      unique=False)


class Fees(UserMixin, db.Model):
    """Model for  Grades of student"""

    __tablename__ = 'Fees'
    S_No = db.Column(db.Integer,db.ForeignKey(Student.S_No),
                     primary_key=True)

    Due_Amount = db.Column(db.Numeric(5,2),
                      unique=False)
    Due_Date = db.Column(db.Date,
                    unique=False)

    def update(self, kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)






# end database
# ************************************************************************************************************************
# ************************************************************************************************************************
# login start

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:

        x = Faculty.query.get(user_id)
        if x is None:
            x = Student.query.get(user_id)
            return x
        else:
            return x
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    # v.speak('You must be logged in to view that page.')
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        dict = request.form
        username = dict['username']
        userpass = dict['password']
        member = dict['membership']

            # Student_Dashboard calling
        if member == "0":
            user = Student.query.filter_by(Enroll_No=username).first()
            if user and user.check_password(password=userpass):
                login_user(user)

                next_page = request.args.get('next')
                return redirect(next_page or "/student_dashboard")

        elif member == "1":
            user = Faculty.query.filter_by(Id=username).first()
            if user and user.check_password(password=userpass):
                login_user(user)

                next_page = request.args.get('next')
                return redirect(next_page or "/faculty_dashboard")

        # except Exception as e:
        #     flash("Due to server issue we are unable to accept your request")
        #     # v.speak("Due to server issue we are unable to accept your request")
        #     return redirect("/")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        return render_template("register_note.html")
    return render_template("register.html")


@app.route("/Forget_pass", methods=["GET", "POST"])
def Forget_pass():
    if request.method == "POST":
        return render_template("forget_note.html")
    return render_template("Forget_pass.html")







# end login
# ************************************************************************************************************************
# ************************************************************************************************************************
# faculty start

@app.route("/faculty_dashboard" ,methods=["POST","GET"])
@login_required
def Faculty_Dashboard():
    """User log-out logic."""
    # if request.method == "POST":
    #     redirect("/voice")


    user = current_user
    return render_template("faculty_dashboard.html",user = user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/student_add",methods=["POST","GET"])
@login_required
def Student_add():
    if request.method == 'POST':
        dict = request.form
        EN =dict["Enrollment"]
        entry = Student(Name = dict["Name"] , Enroll_No = dict["Enrollment"],Branch =dict["Branch"],Specialization=dict["Specialization"],Father_Name=dict["Father_Name"],DOB=dict["DOB"],Gender=dict["Gender"],Address=dict["Address"],Mobile_No=dict["Mobile_No"],email=dict["email"])
        entry.set_password(dict["Password"])
        db.session.add(entry)
        db.session.commit()
        return redirect("/student_add_"+EN)

    user = current_user
    return render_template("student_add.html",user = user)

@app.route("/student_add_<string:enrollment>",methods=["POST","GET"])
@login_required
def Student_add_(enrollment):
    user = current_user
    if request.method == 'POST':
        file =request.files["image"]
        if file.filename.split(".")[0] == enrollment:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            return redirect("/student_add")
        else:
            flash("File name must be same as Enrollment No ")
            return redirect("/student_add_"+enrollment)

    user = current_user
    return render_template("student_add_2.html",user = user)

@app.route("/add_fee",methods=["POST","GET"])
@login_required
def add_fee():
    if request.method == 'POST':
        dict = request.form
        ss = Student.query.filter_by(Enroll_No=dict["enrollment"]).first()
        if ss is None:
            flash("No student Found")

        else:
            trans = Fees.query.filter_by(S_No = ss.S_No).first()
            if trans is None:
                entry = Fees(S_No = ss.S_No,Due_Amount=dict["add"],Due_Date = dict["Date"])
                db.session.add(entry)
                db.session.commit()
            else:
                trans = Fees.query.filter_by(S_No = ss.S_No).first()
                dict ={"Due_Amount":(float(dict["add"])+float(trans.Due_Amount)),"Due_Date" : dict["Date"]}
                trans.update(dict)
                db.session.commit()

    students = Student.query.all()
    user = current_user
    return render_template("add_fee.html",user = user,students=students)



def AA(data):
    try:
        trans = Attendence.query.filter(Attendence.SS_No == data["SS_No"],Attendence.Course_No == data["Course_No"]).first()
        if trans is None:
            entry = Attendence(SS_No = data["SS_No"],Course_No = data["Course_No"],Total_Classes_Held=0,Classes_Attended=0,Till_Date = data["Till_Date"])
            db.session.add(entry)
            db.session.commit()
        trans = Attendence.query.filter(Attendence.SS_No == data["SS_No"] , Attendence.Course_No == data["Course_No"]).first()
        data.update({"Total_Classes_Held":trans.Total_Classes_Held+1})
        data.update({"Classes_Attended":trans.Classes_Attended+1})

        per = (data["Classes_Attended"]/data["Total_Classes_Held"])*100

        data.update({"Percentage" : per})
        trans.update(data)
        db.session.commit()
        return True
    except Exception as e:
        flash(e)
        db.session.rollback()
        return False


@app.route("/student_attendance",methods=["POST","GET"])
@login_required
def Update_student_attendance():
    user = current_user
    if request.method == 'POST':
        dict = request.form
        date = dict["date"]
        course_no = dict["subject"]
        for key in dict.keys():
            if key == "date" or key == "subject":
                continue
            data = {"Till_Date" : date,"Course_No":course_no,"SS_No":key,"FS_No":user.S_No}
            re = AA(data)
            if re is True:
                flash("Update sucessfully")
            else:
                flash("Not Updated")




    Courses = Course.query.order_by(Course.S_No).all()
    students = Student.query.order_by(Student.Enroll_No).all()
    return render_template("update_student_attendence.html",user = user,students=students,Courses=Courses)


@app.route("/student_update",methods=["POST","GET"])
@login_required
def student_update():
    user = current_user
    if request.method == 'POST':
        dict = request.form
        return redirect(url_for(".student_update_2",dict1 = dict['subject'],dict2=dict['student']))

    students = Student.query.all()
    return render_template("student_update.html",user = user,students=students)


@app.route("/student_update_2/", methods=["POST", "GET"])
@login_required
def student_update_2():
    user = current_user

    subject = request.args['dict1']
    student = request.args['dict2']

    if request.method == 'POST':
        if subject == "Password":
            dict = request.form
            ss =Student.query.filter_by(Enroll_No=student).first()
            ss.set_password(dict["Password"])
            db.session.commit()

        elif subject == "Profile picture":
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                if file.filename.split(".")[0] == student:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    #print('upload_image filename: ' + filename)
                    flash('Image successfully uploaded and displayed')
            else:
                flash('Allowed image types are -> png')
                flash('file name same as Enrollment No')
                return redirect(request.url)

        else:
            dict = request.form
            ss =Student.query.filter_by(Enroll_No=student)
            ss.update(dict)
            db.session.commit()

        flash("update successfull")
        return redirect("/student_update")

    students = Student.query.all()
    return render_template("student_update_2.html",user = user,subject = subject,students=students)




@app.route("/student_list")
@login_required
def Student_list():
    """User log-out logic."""
    user = current_user
    students = Student.query.all()
    return render_template("student_list.html",user=user,students = students)

@app.route("/update_syllabus",methods=["POST","GET"])
@login_required
def update_syllabus():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed')
        else:
            flash('Allowed image types are -> png')
            flash('file name same as Course_Code')
            return redirect(request.url)

    user = current_user
    return render_template("update_syllabus.html",user = user)

#end faculty
# ***********************************************************************************************************************
# ************************************************************************************************************************
# Functions

def Fee_pdf(dict):
    pdf = FPDF()
    # Add a page
    pdf.add_page()
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 20)
    pdf.cell(200, 10, txt = " Fees receipt", ln = 1, align = 'C')
    #dict={'Name':'Abhas Kushwaha','Enrollmentno':'EN18IT301003','Fees Paid':49500,'Fees Left to pay':0}
    pdf.cell(200, 10, txt = "RAKS ERP FEE PENDING RECEIPT",  ln = 2, align = 'L')
    for i in dict.keys():
        # create a cell
        pdf.cell(200, 10, txt = i +" : " + str(dict[i]),  ln = 2, align = 'L')
        # save the pdf with name .pdf
    pdf.output("fee.pdf")










# End Functions
# ************************************************************************************************************************
# ************************************************************************************************************************
# student start


@app.route("/student_dashboard")
@login_required
def Student_Dashboard():
    """User log-out logic."""

    user = current_user

    return render_template("student_dashboard.html",user=user)

@app.route("/show_result")
@login_required
def Show_result():
    """User log-out logic."""
    user = current_user
    return render_template("Result.html",user=user)

@app.route("/Syllabus",methods=["POST","GET"])
@login_required
def Syllabus():
    if request.method == "POST":
        dict = request.form
        file = dict['course']+".png"

        return redirect(url_for("download_file",file=file))

    """Course syllabus logic."""
    user = current_user
    courses = Course.query.all()
    return render_template("Syllabus.html",user=user,courses=courses)

@app.route("/Timetable",methods=["POST","GET"])
@login_required
def Timetable():
    if request.method == "POST":
        file = "Timetable.PNG"
        return redirect(url_for("download_file",file=file))
    """Timetable download logic."""
    user = current_user
    return render_template("TimeTable.html",user=user)

@app.route("/Attendance")
@login_required
def Attendance():
    """User log-out logic."""
    user = current_user
    courses = Course.query.order_by(Course.S_No).all()
    cc = {}
    for c in courses:
        att = Attendence.query.filter(Attendence.SS_No == user.S_No,Attendence.Course_No == c.S_No).first()
        if att is None:
            percentage = "Abhi Class nhi laga"
        else:
            percentage = att.Percentage
        cc.update({c.Course_Code:percentage})


    return render_template("Attendance.html",user=user,courses=courses,cc=cc)


@app.route("/FeeReceipt",methods=["POST","GET"])
@login_required
def FeeReceipt():
    """User Fee receipt pdf  logic."""
    user = current_user
    if request.method == "POST":
        ff = Fees.query.filter_by(S_No = user.S_No).all()
        if ff is None:
            flash("No Fee Pending")
            return redirect("/FeeReceipt")
        for f in ff:
            dict = {"Name":user.Name,"Fathers_Name":user.Father_Name,"Enrollment_NO":user.Enroll_No,"Branch":user.Branch,"Mobile_NO":user.Mobile_No,"":"","Due_Amount":f.Due_Amount,"Due_Date":f.Due_Date}
            file= "fee.pdf"
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],file))
        except Exception:
            pass
        Fee_pdf(dict)
        path = os.path.join("/home/RAKSERP/",file)
        return send_file(path, as_attachment=True)

    return render_template("FeeReceipt.html",user=user)



# end student
# *************************************************************************************************************************

@app.route("/about_software", methods=["POST","GET"])
@login_required
def About_software():
    user = current_user
    return render_template("About_erp.html",user=user)


@app.route("/voice", methods=["POST","GET"])
@login_required
def voice():
    if request.method == "POST":
        print(request.get)
    return render_template("voice.html")


@app.route('/download/<file>')
def download_file(file):
    try:
        path = os.path.join(app.config['UPLOAD_FOLDER'],file)
        return send_file(path, as_attachment=True)
    except Exception:
        flash("File Not Found")
        return redirect(request.url)


@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect("/")

# ************************************************************************************************************************




