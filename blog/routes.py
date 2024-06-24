from flask import render_template, redirect, url_for, request
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm

@app.route("/", methods=['GET', 'POST'])
def index():
    form = EntryForm()

    if form.validate_on_submit():
        manage_entry(form)
        return redirect(url_for('index'))

    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()
    return render_template("homepage.html", all_posts=all_posts, form=form)

@app.route("/new-entry", methods=['GET', 'POST'])
def new_entry():
    form = EntryForm()

    if form.validate_on_submit():
        manage_entry(form)
        return redirect(url_for('index'))

    return render_template('entry_form.html', form=form)

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    form = EntryForm(obj=entry)
    errors = None

    if request.method == 'POST':
        if form.validate_on_submit():
            manage_entry(form, entry)
            return redirect(url_for('index'))
        else:
            errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)

def manage_entry(form, entry=None):
    if not entry:
        entry = Entry()

    form.populate_obj(entry)
    db.session.add(entry)
    db.session.commit()