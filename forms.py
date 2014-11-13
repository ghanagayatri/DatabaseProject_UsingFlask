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
		(8, 'Select From Where with two joins,max and avg functions'),
		(9,'Select From Where With Not and In Operator,Nested Query'),
		(10,'Set Command With Where Clause'),
		(11,'Update With Where Clause'),
		(12,'Create User'),
		(13,'Drop User'),
		(14,'Start Transaction'),
		(15,'Rollback Transaction'),
		(16,'Create Table'),
		(17,'Insert Rows into Table')] ,validators=[Required()]) 
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

