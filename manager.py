from flask_script import Manager, Server

from flask_migrate import Migrate, MigrateCommand

from webapp import app
from webapp.models import db, Users, Post, Tag, Comment

manager = Manager(app, db)
manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=Users, Post=Post, Tag=Tag, Comment=Comment)

if __name__ == "__main__":
    app.run(debug=True)
    # db.create_all()