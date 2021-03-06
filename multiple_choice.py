import os
import itertools
import flask.views
from flask import Flask,render_template,session,redirect,url_for,flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from forms import QuerySelectForm,SelectFromWhereForm,SelectFromWhereOrderByForm,SelectFromWhereOrderByLimitForm
from forms import InsertIntoTableForm,CreateTableForm,CreateUserForm,DropUserForm,SelectWhereGroupBy,SelectWhereGroupByHaving
from forms import SelectFromWhereJoinForm,UpdateWhereSetForm,CustomizedQueryForm
############ Connection to Postgres Database ##################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:**********@localhost/Normalized'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

################## Secret key to validate the Web App ##########

app.config['SECRET_KEY'] = 'gayatri'
################################################################


####### Function Which calls Postgres Database##################

def callDatabase(db,Columns_Query,Query):
	column_names = db.engine.execute(Columns_Query).fetchall()
	merged = list(itertools.chain(*column_names))
	col_names = [str(x) for x in merged]
	names = []
	names.append(col_names)
	result = db.engine.execute(Query).fetchall()
	rows = map(list,result)
	result_set = []
	for row in rows:
   		tuple = [str(x) for x in row]
  		result_set.append(tuple)
  	# Combine the Columns Names and Rows into a Single List
  	Final_Result = names + result_set
  	return Final_Result

########### Renders the Template ##############################
@app.route('/', methods=['GET', 'POST']) 
def index():
	query = 0
	form = QuerySelectForm()
	if form.validate_on_submit():
		query = form.selected_query.data
	if query == 2:
		return redirect(url_for('selectwhere'))
	if query == 3:
		return redirect(url_for('selectwhereorderby'))
	if query == 4:
		return redirect(url_for('selectwhereorderbylimit'))
	if query == 5:
		return redirect(url_for('selectwherejoin'))
	if query == 6:
		return redirect(url_for('selectwheregroupby'))
	if query == 7:
		return redirect(url_for('selectwheregroupbyhaving'))
	if query == 8:
		return redirect(url_for('customizedquery'))
	if query == 9:
		return redirect(url_for('updatewhere'))
	if query == 10:
		return redirect(url_for('createuser'))
	if query == 11:
		return redirect(url_for('dropuser'))
	if query == 12:
		return redirect(url_for('createtable'))
	if query == 13:
		return redirect(url_for('insertintotable'))
	else:
		return flask.render_template('index.html', form=form)
#############################################################

################## Cutomized Query function #################
@app.route('/customizedquery', methods=['GET', 'POST'])
def customizedquery():
	form = CustomizedQueryForm()
	query = form.query.data
	if not query:
		return flask.render_template('querydetails.html',form = form)
	else:
		columns = db.engine.execute(query)._metadata.keys
		result = db.engine.execute(query).fetchall()
		cols = []
		for ele in columns:
			cols.append(str(ele))
		rows = map(list,result)
		result_set = []
		result_set.append(cols)
		for row in rows:
			tuple = [str(x) for x in row]
			result_set.append(tuple)
		try:
			if form.validate_on_submit():
				flash(query)
				return flask.render_template('querydetails.html',form = form,result = result_set)
		except Exception:
			flash("Something Wrong With The Query")
			return flask.render_template('querydetails.html',form = form)


##################### Update Where function #################
@app.route('/updatewhere', methods=['GET', 'POST'])
def updatewhere():
	form = UpdateWhereSetForm()
	table = form.table.data
	setcondition = form.setcondition.data
	where_condition = form.where_condition.data
	if not table:
		return flask.render_template('querydetails.html',form = form)
	else:
		try:
			UpdateQuery = "UPDATE " + table + " SET " + setcondition +" WHERE " +where_condition +';'
			Columns_Query = "SELECT column_name FROM information_schema.columns WHERE table_name ='"+ table +"'"
			Select_Query = " SELECT * FROM "+ table + " WHERE " + where_condition;
			Final_Result = callDatabase(db,Columns_Query,Select_Query)
			db.engine.execute(UpdateQuery)
			if form.validate_on_submit():
				flash(UpdateQuery)
				return flask.render_template('querydetails.html',form = form,result = Final_Result)
		except Exception:
			flash("Something Wrong With The Query")
			return flask.render_template('querydetails.html',form = form)

##################### selectwhere join function #############
@app.route('/selectwherejoin', methods=['GET', 'POST'])
def selectwherejoin():
	form = SelectFromWhereJoinForm()
	table1 = form.table1.data
	table2 = form.table2.data
	join = form.join.data
	oncondition = form.oncondition.data
	if not table1:
		return flask.render_template('querydetails.html',form = form)
	else:
		Query = "SELECT * FROM " + table1 + join + table2 +"ON" +oncondition +';'
		result = db.engine.execute(Query).fetchall()
		rows = map(list,result)
		result_set = []
		for row in rows:
   			tuple = [str(x) for x in row]
  			result_set.append(tuple)
		try:
			if form.validate_on_submit():
				flash(Query)
				return flask.render_template('querydetails.html',form = form,result = result_set)
		except Exception:
			flash("Something Wrong With The Query")
			return flask.render_template('querydetails.html',form = form)

# #################### selectwheregroupby function ##########
@app.route('/selectwheregroupby', methods=['GET', 'POST'])
def selectwheregroupby():
	form = SelectWhereGroupBy()
	selectcondition = form.selectcondition.data
	tablename = form.tablename.data
	where_condition = form.where_condition.data
	groupby = form.groupby.data
	if not selectcondition:
		return flask.render_template('querydetails.html',form = form)
	else:
		Query = "SELECT " + selectcondition + " FROM " + tablename + " WHERE " + where_condition + " GROUP BY " + groupby+';'
		result = db.engine.execute(Query).fetchall()
		rows = map(list,result)
		result_set = []
		for row in rows:
   			tuple = [str(x) for x in row]
  			result_set.append(tuple)
		try:
			if form.validate_on_submit():
				flash(Query)
				return flask.render_template('querydetails.html',form = form,result = result_set)
		except Exception:
			flash("Something Wrong With The Query")
			return flask.render_template('querydetails.html',form = form)


#################selectwheregroupbyhaving function ########
@app.route('/selectwheregroupbyhaving', methods=['GET', 'POST'])
def selectwheregroupbyhaving():
	form = SelectWhereGroupByHaving()
	selectcondition = form.selectcondition.data
	tablename = form.tablename.data
	where_condition = form.where_condition.data
	groupby = form.groupby.data
	having = form.having.data
	if not selectcondition:
		return flask.render_template('querydetails.html',form = form)
	else:
		Query = "SELECT " + selectcondition + " FROM " + tablename + " WHERE " + where_condition + " GROUP BY " + groupby+ " HAVING " + having+';'
		result = db.engine.execute(Query).fetchall()
		rows = map(list,result)
		result_set = []
		for row in rows:
   			tuple = [str(x) for x in row]
  			result_set.append(tuple)
		try:
			if form.validate_on_submit():
				flash(Query)
				return flask.render_template('querydetails.html',form = form,result = result_set)
		except Exception:
			flash("Something Wrong With The Query")
			return flask.render_template('querydetails.html',form = form)



#################### DropUser Function ####################
@app.route('/dropuser', methods=['GET', 'POST'])
def dropuser():
	form = DropUserForm()
	user = form.user.data
	if not user:
		return flask.render_template('querydetails.html',form = form)
	else:
		Query = "DROP USER " + user + ';'
		try:
			if form.validate_on_submit():
				db.engine.execute(Query)
				flash("Dropped User Successfully !")
				return flask.render_template('querydetails.html',form = form)
		except Exception:
			flash("Something Wrong With The Drop User Query")
			return flask.render_template('querydetails.html',form = form)


#################### CreateUser Function ##################
@app.route('/createuser', methods=['GET', 'POST'])
def createuser():
	form = CreateUserForm()
	user = form.createuser.data
	createdb_choice = form.select_options.data
	if not user:
		return flask.render_template('querydetails.html',form = form)
	else:
		Query = "CREATE USER " + user + ' ' + createdb_choice + ';'
		try:
			if form.validate_on_submit():
				db.engine.execute(Query)
				flash("User Creation Successfull!")
				return flask.render_template('querydetails.html',form = form)
		except Exception:
			flash("Something Wrong With The Create User Query")
			return flask.render_template('querydetails.html',form = form)


##################### createtable function ##################
@app.route('/createtable', methods=['GET', 'POST']) 
def createtable():
	form = CreateTableForm()
	create_table = form.createtable.data
	if not create_table:
		return flask.render_template('querydetails.html',form = form)
	else:
		try:
			if form.validate_on_submit():
				# This creates the table
				db.engine.execute(create_table)
				# This gets all the table names in the schema
				Tables_Query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
				result = db.engine.execute(Tables_Query)
				rows = map(list,result)
				result_set = []
				for row in rows:
   					tuple = [str(x) for x in row]
  					result_set.append(tuple)
				flash("Table Creation Successfull !")
				return flask.render_template('querydetails.html',form = form,result = result_set)
		except Exception:
			flash("Something Wrong With The Create Table Query")
			return flask.render_template('querydetails.html',form = form)

################# insertintotable function ###################
@app.route('/insertintotable', methods=['GET', 'POST']) 
def insertintotable():
	form = InsertIntoTableForm()
	insert_query = form.query.data
	if not insert_query:
		return flask.render_template('querydetails.html',form = form)
	else:
		try:
			if form.validate_on_submit():
				db.engine.execute(insert_query)
				flash("Insertion Successfull!")
				return flask.render_template('querydetails.html',form = form)
		except Exception:
			flash("Something Wrong With The Insert Query")
			return flask.render_template('querydetails.html',form = form)

############# selectfromwhere function ########################
@app.route('/selectwhere', methods=['GET', 'POST']) 
def selectwhere():
	form = SelectFromWhereForm()
	tablename = form.tablename.data
	where_condition = form.where_condition.data
	if not tablename:
		return flask.render_template('querydetails.html', form=form)
	else:
		# Fetch the Column Names from the Table
		Columns_Query = "SELECT column_name FROM information_schema.columns WHERE table_name ='"+ tablename +"'"
		# Fetch the rows from the Table
		Query = "SELECT * FROM "+ tablename + ' WHERE ' + where_condition
		Final_Result = callDatabase(db,Columns_Query,Query)
		if form.validate_on_submit():
			flash(Query)
		return flask.render_template('querydetails.html', form=form,result = Final_Result)

############### selectfromwhere orderby function ##################
@app.route('/selectwhereorderby', methods=['GET', 'POST']) 
def selectwhereorderby():
	form = SelectFromWhereOrderByForm()
	tablename = form.tablename.data
	where_condition = form.where_condition.data
	orderbycolumn = form.orderby.data
	if not tablename:
		return flask.render_template('querydetails.html', form=form)
	else:
		# Fetch the Column Names from the Table
		Columns_Query = "SELECT column_name FROM information_schema.columns WHERE table_name ='"+ tablename +"'"
		# Fetch the rows from the Table
		Query = "SELECT * FROM "+ tablename + ' WHERE ' + where_condition + ' ORDER BY ' + orderbycolumn
		Final_Result = callDatabase(db,Columns_Query,Query)
		if form.validate_on_submit():
			flash(Query)
		return flask.render_template('querydetails.html', form=form,result = Final_Result)

############### selectfromwhere orderby limit function ##################
@app.route('/selectwhereorderbylimit', methods=['GET', 'POST']) 
def selectwhereorderbylimit():
	form = SelectFromWhereOrderByLimitForm()
	tablename = form.tablename.data
	where_condition = form.where_condition.data
	orderbycolumn = form.orderby.data
	limit = form.limit.data
	if not tablename:
		return flask.render_template('querydetails.html', form=form)
	else:
		# Fetch the Column Names from the Table
		Columns_Query = "SELECT column_name FROM information_schema.columns WHERE table_name ='"+ tablename +"'"
		# Fetch the rows from the Table
		Query = "SELECT * FROM "+ tablename + ' WHERE ' + where_condition + ' ORDER BY ' + orderbycolumn + ' LIMIT ' + limit
		Final_Result = callDatabase(db,Columns_Query,Query)
		if form.validate_on_submit():
			flash(Query)
		return flask.render_template('querydetails.html', form=form,result = Final_Result)

############# Handlers For Error Pages ########################
@app.errorhandler(404)
def page_not_found(e):
        return flask.render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return flask.render_template('500.html'), 500
###############################################################

bootstrap = Bootstrap(app)

if __name__ == '__main__':
        app.run(debug=True)
