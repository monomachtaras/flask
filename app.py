from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (
    Department, Application, Client
)
engine = create_engine(
    'mysql+mysqlconnector://itea:itea@localhost/itea')
Session = sessionmaker(bind=engine)
session = Session()


app = Flask(__name__)


@app.route('/')
def index_page():
   return render_template('index.html')


@app.route('/departments', methods=['GET', 'POST'])
def departments():
   if request.method == 'POST' and \
           not session.query(Department).filter(Department.city == request.form['city']).one_or_none():
      city = request.form['city']
      count_of_workers = request.form['count_of_workers']
      new_department = Department(city=city,
                                  count_of_workers=count_of_workers)
      session.add(new_department)
      session.commit()

   departments = session.query(Department).all()
   return render_template('departments.html',
                          departments=departments)


@app.route('/departments/<int:department_id>',
           methods=['GET', 'POST'])
def departments_detail(department_id=None):

   department = session.query(Department).filter(
      Department.id == department_id).first()

   clients = department.clients
   return render_template('departments_detail.html',
                          clients=clients)


if __name__=='__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
