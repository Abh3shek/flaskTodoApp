from flask import Blueprint, render_template, flash, request, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint("views", __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if len(request.form['taskTitle']) < 1 and len(request.form['taskDescription']) < 1:
            flash('Please provide title & description to add a task...!', category='error')
        else:
            todo = Note(taskTitle=request.form['taskTitle'], taskDescription=request.form['taskDescription'], user_id = current_user.id)
            db.session.add(todo)
            db.session.commit()
            flash('Task added successfully...!', category='success')

        user = Note.query.all()
    return render_template('index.html', user=current_user)

@views.route('/delete/<int:sr_no>')
def delete(sr_no):
    delRec = Note.query.filter_by(sr_no=sr_no).first()
    db.session.delete(delRec)
    db.session.commit()
    return redirect('/')

@views.route('update/<int:sr_no>', methods=['GET', 'POST'])
@login_required
def update(sr_no):
    if request.method == 'POST':
        updateTask = Note.query.filter_by(sr_no=sr_no).first()
        updateTask.taskTitle = request.form['taskTitle']
        updateTask.taskDescription = request.form['taskDescription']
        db.session.add(updateTask)
        db.session.commit()
        return redirect('/')
    
    updateTask = Note.query.filter_by(sr_no=sr_no).first()
    return render_template('update.html', updateTask=updateTask, user=current_user)