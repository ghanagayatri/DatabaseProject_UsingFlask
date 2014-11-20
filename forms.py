from wtforms import SelectField, SubmitField,TextField,TextAreaField,RadioField
from wtforms.validators import Required
from flask.ext.wtf import Form

class QuerySelectForm(Form):
	selected_query = SelectField('Please Select One Query',coerce =int,
		choices = [(1,'<<Select One From Following>>'),
		(2,'Select From Where'),
		(3,'Select From Where Order By'),
		(4,'Select From Where Order By Limit'),
		(5, 'Select From Where with an implied join'),
		(6, 'Select From Where Group By'),
		(7, 'Select From Where Group By Having'),
		(8, 'customized query'),
		(9,'Update With Where Clause'),
		(10,'Create User'),
		(11,'Drop User'),
		(12,'Create Table'),
		(13,'Insert Rows into Table')] ,validators=[Required()]) 
	submit = SubmitField('Submit')

class SelectFromWhereForm(Form):
	tablename = TextField("Table Name",validators=[Required()])
	where_condition = TextField("Where Condition In Format Column = Value",validators=[Required()])
	submit = SubmitField('Execute Query')

class SelectFromWhereOrderByForm(Form):
	tablename = TextField("Table Name",validators=[Required()])
	where_condition = TextField("Where Condition In Format Column = Value",validators=[Required()])
	orderby = TextField("OrderByColumn",validators=[Required()])
	submit = SubmitField('Execute Query')

class SelectFromWhereOrderByLimitForm(Form):
	tablename = TextField("Table Name",validators=[Required()])
	where_condition = TextField("Where Condition In Format Column = Value",validators=[Required()])
	orderby = TextField("OrderByColumn",validators=[Required()])
	limit = TextField("Enter a Number For Limit ",validators=[Required()])
	submit = SubmitField('Execute Query')

class SelectFromWhereJoinForm(Form):
	table1 = TextField("First Table Name",validators=[Required()])
	table2 = TextField("Second Table Name",validators=[Required()])
	join = TextField("Enter Whether Left/Right/Outer Join",validators=[Required()])
	oncondition = TextField("ON Condition",validators=[Required()])
	submit = SubmitField('Execute Query')

class UpdateWhereSetForm(Form):
	table = TextField("Table Name",validators=[Required()])
	setcondition = TextField("Set Condition",validators=[Required()])
	where_condition = TextField("Where Condition",validators = [Required()])
	submit = SubmitField('Execute Query')

class InsertIntoTableForm(Form):
	query = TextAreaField("Enter Insert Query",validators = [Required()])
	submit = SubmitField('Execute Query')

class CreateTableForm(Form):
	createtable = TextAreaField("Enter Create Table Query",validators = [Required()])
	submit = SubmitField('Execute Query')

class CreateUserForm(Form):
	createuser = TextField("Enter User Name and Select One Choice",validators = [Required()])
	select_options = RadioField("Please Select One", choices=[('CREATEDB','CREATEDB'),('NOCREATEDB','NOCREATEDB')],validators = [Required()])
	submit = SubmitField('Execute Query')

class DropUserForm(Form):
	user = TextField("Enter User To Be Dropped",validators = [Required()])
	submit = SubmitField('Execute Query')

class SelectWhereGroupBy(Form):
	selectcondition = TextField("Enter the Column names and Aggregate function ",validators=[Required()])
	tablename = TextField("Table Name",validators=[Required()])
	where_condition = TextField("Where Condition In Format Column = Value",validators=[Required()])
	groupby = TextField("GroupByColumn",validators=[Required()])
	submit = SubmitField('Execute Query')

class SelectWhereGroupByHaving(Form):
	selectcondition = TextField("Enter the Column names and Aggregate function ",validators=[Required()])
	tablename = TextField("Table Name",validators=[Required()])
	where_condition = TextField("Where Condition In Format Column = Value",validators=[Required()])
	groupby = TextField("GroupByColumn",validators=[Required()])
	having =  TextField("Having Condition",validators=[Required()])
	submit = SubmitField('Execute Query')

class CustomizedQueryForm(Form):
	query = TextAreaField("Enter The Query:",validators=[Required()])
	submit = SubmitField('Execute Query')