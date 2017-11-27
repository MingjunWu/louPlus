#! /usr/bin/env python3
from flask import Flask, render_template,abort
import json, os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Category %r>' % self.name

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category')
    def __init__(self,title,created_time,content, category):
        self.title = title
        self.created_time = created_time
        self.content = content
        self.category = category
    def __repr__(self):
        return '<File %r>' % self.title
def create_data():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java',datetime.utcnow(),'File Content = Java is cool!',java)
    file2 = File('Hello Python',datetime.utcnow(),'File Content - Python is cool!',python)
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
@app.route('/')
def index():
    return render_template('index.html',files = File.query.all())
@app.route('/files/<file_id>')
def file(file_id):
    file_item = File.query.get_or_404(file_id)
    return render_template('file.html',file_item = file_item)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404        
if __name__ == '__main__':
    app.run()
