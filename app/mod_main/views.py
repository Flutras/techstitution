from flask import Blueprint, render_template, request, redirect, url_for, Response, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextField, SubmitField, TextAreaField, RadioField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired
from bson import ObjectId
from app import mongo
from bson import json_util
import json

mod_main = Blueprint('main', __name__)


@mod_main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return redirect(url_for('main.index'))
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('mod_main/login.html', error=error)
    else:
        return render_template('mod_main/login.html', error=error)


class AddPeopleForm(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired("Please fill out firstname")])
    lastname = StringField('Lastname', validators=[InputRequired()])
    # submit = SubmitField("Submit")

@mod_main.route('/index', methods=['GET', 'POST'])
def indexpage():
    form=AddPeopleForm();
    if request.method == 'GET':
        reports = mongo.db.reports.find()
        return render_template('mod_main/index.html', reports=reports, form=form)

@mod_main.route('/', methods=['GET', 'POST'])
def index():
    form = AddPeopleForm()
    if request.method == 'GET':
        reports = mongo.db.reports.find()
        audits = mongo.db.audits.find()
        return render_template('mod_main/dashboard.html', reports=reports, audits=audits, form=form)

    elif request.method == 'POST' and form.validate_on_submit():
        mongo.db.reports.insert({
            "firstname": request.form['firstname'],
            "lastname": request.form['lastname']
        })
        return redirect(url_for('main.index'))


@mod_main.route('/audit_list', methods=['GET', 'POST'])
def audit_list():
    audits = mongo.db.audits.find()
    return render_template('mod_main/audit_list.html', audits=audits)


# New Audit Form
class AddAuditForm(FlaskForm):
    audit_ref_num = IntegerField('Reference number', validators=[InputRequired("Please enter audit reference number!")])
    audit_title = StringField('Title', validators=[InputRequired("Please enter audit title!")])
    audit_type = StringField('Audit type', validators=[InputRequired("Please enter audit type!")])
    audit_organization = StringField('Organization', validators=[InputRequired("Please enter organization!")])
    audit_start_date = DateTimeField('Audit Start Date', validators=[InputRequired("Please enter start date!")])
    audit_end_date = DateTimeField('Audit End Date', validators=[InputRequired("Please enter end date!")])
    audit_auditee = StringField('Auditee', validators=[InputRequired("Please enter auditee!")])
    audit_place = StringField('Place', validators=[InputRequired("Please enter place!")])
    audit_frefnum = IntegerField('Follow-up reference number', validators=[InputRequired("Please enter follow-up reference number!")])
    audit_chrefnum = IntegerField('Change reference number', validators=[InputRequired("Please enter changed reference number!")])
    audit_tl = StringField('Audit Team Leader', validators=[InputRequired("Please enter team leader name!")])
    audit_tm = StringField('Audit Team Members', validators=[InputRequired("Please enter team members!")])
    audit_ap = StringField('Auditee Participants', validators=[InputRequired("Please enter auditee participants!")])
    submit = SubmitField("Submit")


@mod_main.route('/add_audit_form', methods=['GET', 'POST'])
def add_audit_form():
    form = AddAuditForm()
    if request.method == 'GET':
        audits = mongo.db.audits.find()
        return render_template('mod_main/add_audit_form.html', audits=audits, form=form)

    elif request.method == 'POST':
        data = request.form

        new_inputs = ({})
        counter = 1
        while counter < 5:
            if 'input'+str(counter) in data:
                new_inputs.update({
                    'input_'+str(counter): data['input'+str(counter)]
                })
            counter += 1

        print new_inputs

        mongo.db.audits.insert({
            "new_inputs": new_inputs,
            "audit_ref_num": request.form['audit_ref_num'],
            "audit_title": request.form['audit_title'],
            "audit_type": request.form['audit_type'],
            "audit_organization": request.form['audit_organization'],
            "audit_start_date": request.form['audit_start_date'],
            "audit_end_date": request.form['audit_end_date'],
            "audit_auditee": request.form['audit_auditee'],
            "audit_place": request.form['audit_place'],
            "audit_frefnum": request.form['audit_frefnum'],
            "audit_chrefnum": request.form['audit_chrefnum'],
            "audit_tl": request.form['audit_tl'],
            "audit_tm": request.form['audit_tm'],
            "audit_ap": request.form['audit_ap']
        })
        return redirect(url_for('main.index'))


# New NC Form
class AddNCForm(FlaskForm):
    nc_title = StringField('Title', validators=[InputRequired("Please enter NC title!")])
    nc_operator_auditee = StringField('Operator Auditee', validators=[InputRequired("Please enter operator auditee!")])
    nc_number = IntegerField('Number', validators=[InputRequired("Please enter number!")])
    nc_date = DateTimeField('Date', validators=[InputRequired("Please enter date!")])
    nc_status = StringField('Status', validators=[InputRequired("Please enter status!")])
    nc_agreed_date_for_CAP = DateTimeField('Agreed date for CAP', validators=[InputRequired("Please enter agreed date for CAP!")])
    nc_level = StringField('Level', validators=[InputRequired("Please enter level!")])
    nc_due_date = DateTimeField('Due Date', validators=[InputRequired("Please enter due date!")])
    nc_closure_date = DateTimeField('Closure Date', validators=[InputRequired("Please enter closure date!")])
    nc_requirement_references = StringField('Requirement References', validators=[InputRequired("Please enter requirement refeences!")])
    nc_further_references = StringField('Further References', validators=[InputRequired("Please enter further references!")])
    nc_auditor_ofcaa = StringField('Auditor of CAA', validators=[InputRequired("Please enter auditor of CAA!")])
    nc_auditee_rfCAP = StringField('Auditee responsible for CAP', validators=[InputRequired("Please enter auditee!")])
    requirement_references = TextAreaField('', validators=[InputRequired("Please enter requirement references!")])
    nc_details = TextAreaField('Non Conformity Details', validators=[InputRequired("Please enter details!")])
    submit = SubmitField("Submit")


@mod_main.route('/<string:audit_id>/add_nc_form', methods=['GET', 'POST'])
def add_nc_form(audit_id):
    form = AddNCForm()
    if request.method == 'GET':
        audit = mongo.db.audits.find({"_id": ObjectId(audit_id)})
        return render_template('mod_main/add_nc_form.html', audit=audit, form=form)

    elif request.method == 'POST':
        # print "post request"

        mongo.db.audits.update({"_id": ObjectId(audit_id)}, {"$set": {nonconformities: {
            "nc_title": request.form['nc_title'],
            "nc_operator_auditee": request.form['nc_operator_auditee'],
            "nc_number": request.form['nc_number'],
            "nc_date": request.form['nc_date'],
            "nc_status": request.form['nc_status'],
            "nc_agreed_date_for_CAP": request.form['nc_agreed_date_for_CAP'],
            "nc_level": request.form['nc_level'],
            "nc_due_date": request.form['nc_due_date'],
            "nc_closure_date": request.form['nc_closure_date'],
            "nc_requirement_references": request.form['nc_requirement_references'],
            "nc_further_references": request.form['nc_further_references'],
            "nc_auditor_ofcaa": request.form['nc_auditor_ofcaa'],
            "nc_auditee_rfCAP": request.form['nc_auditee_rfCAP'],
            "requirement_references": request.form['requirement_references'],
            "nc_details": request.form['nc_details']
        }}})
        return redirect(url_for('main.show_audit', audit_id=audit_id))


# New NC Form
class AddCAForm(FlaskForm):
    ca_description = StringField('Corrective Action Description', validators=[InputRequired("Please enter description!")])
    ca_date_of_capapproval = DateTimeField('Date of CAP approval', validators=[InputRequired("Please enter date!")])
    ca_due_date = DateTimeField('Due Date', validators=[InputRequired("Please enter due date!")])
    ca_contact_person = StringField('Contact Person', validators=[InputRequired("Please enter contact!")])
    ca_closure_date = DateTimeField('Closure Date', validators=[InputRequired("Please enter due date!")])
    ca_due_date_history = TextAreaField('Due Date History', validators=[InputRequired("Please enter due date!")])

    submit = SubmitField("Submit")


@mod_main.route('/<string:audit_id>/add_ca_form', methods=['GET', 'POST'])
def add_ca_form(audit_id):
    form = AddCAForm()
    if request.method == 'GET':
        audit = mongo.db.audits.find({"_id": ObjectId(audit_id)})
        return render_template('mod_main/add_ca_form.html', audit=audit, form=form)
    elif request.method == 'POST':
        # print "post request"
        mongo.db.correctiveactions.update({"_id": ObjectId(audit_id)}, {"$set": {
            "ca_description": request.form['ca_description'],
            "ca_date_of_capapproval": request.form['ca_date_of_capapproval'],
            "ca_due_date": request.form['ca_due_date'],
            "ca_contact_person": request.form['ca_contact_person'],
            "ca_closure_date": request.form['ca_closure_date'],
            "ca_due_date_history": request.form['ca_due_date_history']
        }})
        return redirect(url_for('main.show_nc', audit_id=audit_id))



@mod_main.route('/add_people_form', methods=['GET', 'POST'])
def add_people_form():
    form = AddPeopleForm()
    if request.method == 'GET':
        reports = mongo.db.reports.find()
        return render_template('mod_main/add_people_form.html', reports=reports, form=form)

    elif request.method == 'POST' and form.validate_on_submit():
        # print "post request"
        mongo.db.reports.insert({
            "firstname": request.form['firstname'],
            "lastname": request.form['lastname']
        })
        # return "Form successfully submitted!"
        return redirect(url_for('main.indexpage'))


# behet post request ne kete url
@mod_main.route('/remove/audit', methods=['POST'])
def remove_audit():
    if request.method == 'POST':
        audit_id = request.form['id']
        mongo.db.audits.remove({"_id": ObjectId(audit_id)})
        return Response(json.dumps({"removed": True}), mimetype='application/json')


@mod_main.route('/remove/report', methods=['POST'])
def remove_report():
    if request.method == 'POST':
        report_id = request.form['id']
        mongo.db.reports.remove({"_id": ObjectId(report_id)})
        return Response(json.dumps({"removed": True}), mimetype='application/json')


@mod_main.route('/show_audit/<string:audit_id>', methods=['GET', 'POST'])
def show_audit(audit_id):
    form = AddAuditForm()
    if request.method == 'GET':
        audit = mongo.db.audits.find_one({"_id": ObjectId(audit_id)})
        return render_template('mod_main/audit_details.html', audit=audit, form=form)


@mod_main.route('/edit/<string:audit_id>', methods=['GET', 'POST'])
def edit_audit(audit_id):
    form = AddAuditForm()
    if request.method == 'GET':
        audit = mongo.db.audits.find_one({"_id": ObjectId(audit_id)})
        return render_template('mod_main/audit_edit.html', audit=audit, form=form)
    elif request.method == 'POST':
        audit = mongo.db.audits.find_one({"_id": ObjectId(audit_id)})
        mongo.db.audits.update({"_id": ObjectId(audit_id)}, {"$set": {
             "audit_ref_num": request.form['audit_ref_num'],
             "audit_title": request.form['audit_title'],
             "audit_type": request.form['audit_type'],
             "audit_organization": request.form['audit_organization'],
             "audit_start_date": request.form['audit_start_date'],
             "audit_end_date": request.form['audit_end_date'],
             "audit_auditee": request.form['audit_auditee'],
             "audit_place": request.form['audit_place'],
             "audit_frefnum": request.form['audit_frefnum'],
             "audit_chrefnum": request.form['audit_chrefnum'],
             "audit_tl": request.form['audit_tl'],
             "audit_tm": request.form['audit_tm'],
             "audit_ap": request.form['audit_ap']
         }})
        return redirect(url_for('main.show_audit', audit_id= audit_id))

    # return 'Showing result ' + str(result)


@mod_main.route('/show_report/<string:report_id>', methods=['GET'])
def show_report(report_id):
    result = mongo.db.reports.find_one({"_id": ObjectId(report_id)})
    return 'Showing result ' + str(result)


@mod_main.route('/add-people', methods=['GET', 'POST'])
def add_people():
    # TODO: Implement POST REQUEST
    # if success:
    form = AddPeopleForm()
    reports = mongo.db.reports.find();
    if request.method == 'GET':
        return render_template('mod_main/index.html', form=form, reports=reports)
    elif request.method == 'POST':
        # Get form
        form = AddPeopleForm()

        # Get form data
        data = form.data

        # Add document to the database
        added_report_id = mongo.db.reports.insert(data)

        # Get the added document
        report_doc = mongo.db.reports.find_one({"_id": ObjectId(added_report_id)})

        # Return a json response
        return Response(json_util.dumps(report_doc),mimetype="application/json")
    else:
        return Response(json_util.dumps({"error":"Something went wrong!"}),mimetype="application/json")


@mod_main.route('/add-audit', methods=['GET', 'POST'])
def add_audit():
    # TODO: Implement POST REQUEST
    # if success:
    form = AddAuditForm()
    if request.method == 'POST':
        if form.validate() == False:
            # flash('All fields are required!')
            audits = mongo.db.audits.find()
            return render_template('mod_main/add_audit.html', audits=audits, form=form)
        else:
            mongo.db.audits.insert({
                "audit_title": request.form['audit_title'],
                "audit_ref_num": request.form['audit_ref_num'],
                "audit_start_date": request.form['audit_start_date']
            })
            return redirect(url_for('main.audit_list'))
    elif request.method == 'GET':
        return render_template('mod_main/add_audit.html', form=form)





# views for new bootstrap admin dashboard theme template



@mod_main.route('/corrective_actions', methods=['GET', 'POST'])
def corrective_actions():
    # audits = mongo.db.audits.find()
    return render_template('mod_main/corrective_actions.html')


@mod_main.route('/forms', methods=['GET', 'POST'])
def forms():
    # audits = mongo.db.audits.find()
    return render_template('mod_main/forms.html')


@mod_main.route('/blank-page', methods=['GET', 'POST'])
def blank_page():
    # audits = mongo.db.audits.find()
    return render_template('mod_main/blank-page.html')







