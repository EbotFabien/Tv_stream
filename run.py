from app import create_app,db
# from flask_migrate import Migrate, MigrateCommand, upgrade
#from flask_script import Manager
from app.Models import User,Suggestion,Journey,Impression

app = create_app()
#manager = Manager(app)
# migrate = Migrate(app, db)
#manager.add_command('db', MigrateCommand)


#@manager.command
def recreate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        print('ok')

def mla():
    with app.app_context():
        imp=('Late Departure','Very Good','Very Poor','disrespecful')
        for i in imp:
            final=Impression(impression=i)
            db.session.add(final)
            db.session.commit()

if __name__ =='__main__':
    #mla()
    recreate_db()
    app.run(debug=True)