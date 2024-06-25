from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm, LoginForm
from blog.config import Config

@app.route("/", methods=['GET', 'POST'])
def index():
    form = EntryForm()

    if form.validate_on_submit():
        manage_entry(form)
        return redirect(url_for('index'))

    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()
    return render_template("homepage.html", all_posts=all_posts, form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == Config.ADMIN_USERNAME and form.password.data == Config.ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('You have been logged in.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route("/new-entry", methods=['GET', 'POST'])
def new_entry():
    return manage_entry()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    return manage_entry(entry_id)

def manage_entry(entry_id=None):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if entry_id:
        # Edytowanie istniejącego wpisu
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
    else:
        # Tworzenie nowego wpisu
        entry = Entry()
        form = EntryForm()

    errors = None

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)
