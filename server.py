from flask import Flask, request, redirect, render_template, flash, session
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "lkjf8lelf"

# email_validation is NAME of DB which already exists! 
mysql = MySQLConnector(app, 'email_validation')

@app.route('/')
def index(): 
	return render_template('index.html')

@app.route('/emails', methods=['POST'])
def validate(): 
	if not EMAIL_REGEX.match(request.form['email']): 
		flash("EMAIL IS NOT VALID!", 'error')
		return redirect('/')
	else: 
		query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
		data = {
			'email': request.form['email']
		}
		mysql.query_db(query, data)
		flash('Email {} is valid!'.format(request.form['email']), 'success')
		return redirect('/success')

@app.route('/success', methods=['GET'])
def show(): 
	query = "SELECT * FROM emails"
	emails = mysql.query_db(query)
	return render_template('success.html', all_emails = emails)

@app.route('/destroy/<email_id>', methods=['POST'])
def delete(email_id): 
	query = "DELETE FROM emails WHERE id = :id"
	data = {'id': email_id}
	mysql.query_db(query, data) 
	return redirect('/success')

app.run(debug=True)

