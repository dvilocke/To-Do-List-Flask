from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User, Task
from forms import LoginForm, singInForm
from flask_bootstrap import Bootstrap
import secrets

#Recursos: https://bootswatch.com/
#Recursos: https://getbootstrap.com/docs/5.1/components/navbar/
#Recursos: https://uigradients.com/#ColorsOfSky

#configurations
app = Flask(__name__)
app.secret_key = secrets.token_hex(20)

#mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'bd_proyecto_to_do'
mysql = MySQL(app=app)

#flask_login
login_manager = LoginManager(app=app)
login_manager.login_view = 'login'

#flask_bootstrap
Bootstrap(app=app)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('view'))
    else:
        ip = request.remote_addr
        return render_template('home.html', ip=ip)

@app.route('/view/')
@login_required
def view():
    task_user = Task.bring_user_tasks(current_user.get_id(),con=mysql)
    return render_template('view.html', task_user = task_user)

@app.route('/change_states/<string:name>/<string:description>/<string:state>/')
@login_required
def change_states(name, description, state):
    try:
        data = Task.get_task(id_user=current_user.id, name=name, description=description, state=state, con=mysql)[0]
        #cuidado con esto
        if data[3] == 0:
            Task.update_state(name, description, data[3], 1, mysql)
        else:
            Task.update_state(name, description, data[3], 0, mysql)
        flash(f'the task {name} was updated')
    except:
        flash(f'the task {name} status was not updated')
    finally:
        return redirect(url_for('index'))

@app.route('/delete/<string:name>/<string:description>/<string:state>/')
def delete(name, description, state):
    try:
        Task.delete_task(current_user.id, name, description, state, mysql)
        flash(f'the task {name} was eliminated')
    except:
        flash(f'the task {name} not was eliminated')
    finally:
        return redirect(url_for('index'))

@app.route('/add/', methods=['GET', 'POST'], defaults={'name':None, 'description':None, 'state':None})
@app.route('/edit/<string:name>/<string:description>/<string:state>/', methods=['GET', 'POST'])
@login_required
def add(name, description, state):
    if request.method == 'POST':
        if name and description and state:
            new_name = request.form['name']
            new_description = request.form['description']
            new_state = request.form['state']
            try:
                Task.update_task(name, description, state,new_name, new_description, new_state, mysql)
                flash('successfully updated task')
            except:
                flash('Task not updated successfully')
            finally:
                next = request.args.get('next')
                if not next:
                    return redirect(url_for('index'))
                return redirect(next)
        else:
            try:
                name = request.form['name']
                description = request.form['description']
                state = request.form['state']
                task = Task(current_user.id,name,description,state)
                task.save_task(mysql)
                flash(f'the task {name} was saved')
            except:
                flash(f'the task {name} not was saved')
            finally:
                next = request.args.get('next')
                if not next:
                    return redirect(url_for('index'))
                return redirect(next)
    if name and description and state:
        data = Task.get_task(current_user.id, name, description, state, mysql)[0]
        return render_template('add.html', data = data)
    else:
        return render_template('add.html', data = ['','','',''])


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_email(form.email.data, con=mysql)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remind_me.data)
            flash('Logged in successfully.')

            next = request.args.get('next')
            if not next:
                return redirect(url_for('index'))

            return redirect(next)
        else:
            flash('Email and passwords do not match')
        return redirect(url_for('index'))

    return render_template('login.html', form = form)

@app.route('/checkin/', methods=['GET', 'POST'])
def check_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = singInForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.email.data, form.password.data)
        try:
            user.save(mysql)
            flash('Successfully registered')

        except MySQLdb.IntegrityError:
            flash(f'the mail:{form.email.data} is already in use')
            return redirect(url_for('index'))
       
        next = request.args.get('next')

        if not next:
            return redirect(url_for('index'))
        return redirect(next)
    return render_template('checkin.html', form = form)

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id), con=mysql)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('closed session')
    return redirect(url_for('index'))




