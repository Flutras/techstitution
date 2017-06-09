from flask import Blueprint, render_template, request, redirect, url_for
from bson import ObjectId
from app import mongo

mod_main = Blueprint('main', __name__)


@mod_main.route('/', methods=['GET','POST'])
def index():

	if request.method == 'GET':
		reports=mongo.db.reports.find()
		return render_template('mod_main/index.html',reports=reports)

	elif request.method == 'POST':
		mongo.db.reports.insert({
			"firstname":request.form['firstname'],
			"lastname":request.form['lastname']
		})
		return "POST REQUEST"

@mod_main.route('/remove/<string:report_id>', methods=['GET'])
def remove(report_id):
	if request.method == 'GET':
		mongo.db.reports.remove({"_id":ObjectId(report_id)})
		return redirect(url_for('main.index'))



@mod_main.route('/show/<string:report_id>', methods=['GET'])
def show(report_id):
	result=mongo.db.reports.find_one({"_id":ObjectId(report_id)})
	return 'Showing result '+str(result)