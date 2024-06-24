from blog import app, db
from blog.models import User, Post, Entry

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Entry': Entry}

if __name__ == "__main__":
    app.run()