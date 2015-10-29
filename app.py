#/bin/python
# -*- coding: utf-8 -*-
"""
	Flask simple blog
	~~~~~~~~
"""
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
from sqlite3 import dbapi2 as sqlite3


app = Flask(__name__)

app.config.update(dict(
	DEBUG = True
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def hello():
	# return 'Hello, this is a snippet.'
	return render_template('index.html')

@app.route('/login')
def login():
	return 'Hello, this is a snippet.'

if __name__ == '__main__':
	app.run()
