import redis
from gevent.pywsgi import WSGIServer

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (
    Department, Application, Client, User, Base
)
from utils import login_required


app = Flask(__name__)


@app.route('/')
def index_page():
   return render_template('index.html')


@app.route('/departments', methods=['GET', 'POST'])
# @login_required
def departments():
   if request.method == 'POST' and \
           not app.mysql_session.query(Department).filter(Department.city == request.form['city']).one_or_none():
      city = request.form['city']
      count_of_workers = request.form['count_of_workers']
      new_department = Department(city=city,
                                  count_of_workers=count_of_workers)
      app.mysql_session.add(new_department)
      app.mysql_session.commit()

   departments = app.mysql_session.query(Department).all()
   return render_template('departments.html',
                          departments=departments)


@app.route('/applications', methods=['GET', 'POST'],
           defaults={'application_id': None})
@app.route('/applications/<int:application_id>',
           methods=['GET', 'POST'])
def applications(application_id):
    if application_id:
        application = app.mysql_session.query(Application).filter(
            Application.id == application_id).one_or_none()
        app.mysql_session.delete(application)
        app.mysql_session.commit()

    applications = app.mysql_session.query(Application).all()
    return render_template('applications.html',
                          applications=applications)

@app.route('/departments/<int:department_id>',
           methods=['GET', 'POST'])
def departments_detail(department_id=None):

   department = app.mysql_session.query(Department).filter(
      Department.id == department_id).first()

   clients = department.clients
   return render_template('departments_detail.html',
                          clients=clients)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = app.mysql_session.query(User).filter(User.email == email,
                                          User.password == password).one_or_none()
        if user:
            session['logged_in'] = user.email
            return redirect(url_for('departments'))
        return redirect(url_for('register'))
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    del session['logged_in']
    return redirect(url_for('index_page'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not app.mysql_session.query(User).filter(User.email == request.form['email']).one_or_none():
           login = request.form['login']
           password = request.form['password']
           email = request.form['email']
           new_user = User(login=login,password=password, email=email)
           app.mysql_session.add(new_user)
           app.mysql_session.commit()
        return redirect(url_for('login'))


    return render_template('register.html')


def main():
    # connection to mysql database
    engine = create_engine(
        'mysql+mysqlconnector://itea:itea@localhost/itea')
    mysql_session_class = sessionmaker(bind=engine)
    mysql_session = mysql_session_class()

    Base.metadata.create_all(engine)

    app.mysql_session = mysql_session
    app.secret_key = b'secret key'
    # app.run(host='0.0.0.0', port=5000, debug=True)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
