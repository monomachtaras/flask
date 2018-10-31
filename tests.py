import csv
import unittest

from bs4 import BeautifulSoup
from lxml import html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from models import Base, Department, Application, Client


class FlaskTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine(
            'mysql+mysqlconnector://iteatest:iteatest@localhost/iteatest')
        mysql_session_class = sessionmaker(bind=engine)
        mysql_session = mysql_session_class()
        app.mysql_session = mysql_session

        Base.metadata.create_all(engine)

        with open('department.csv', 'r') as c_file:
            reader = csv.reader(c_file)
            for n, row in enumerate(reader):
                if n == 0:
                    pass
                else:
                    department = Department(id=row[0],
                                            city=row[1],
                                            count_of_workers=row[2])
                    app.mysql_session.add(department)
        with open('client.csv', 'r') as c_file:
            reader = csv.reader(c_file)
            for n, row in enumerate(reader):
                if n == 0:
                    pass
                else:
                    client = Client(id=row[0],
                                    first_name=row[1],
                                    last_name=row[2],
                                    education=row[3],
                                    passport=row[4],
                                    city=row[5],
                                    age=row[6],
                                    department_id=row[7])
                    app.mysql_session.add(client)
        with open('application.csv', 'r') as c_file:
            reader = csv.reader(c_file)
            for n, row in enumerate(reader):
                if n == 0:
                    pass
                else:
                    application = Application(
                        suma=row[1],
                        credit_state=row[2],
                        currency=row[3],
                        client_id=row[4])
                    app.mysql_session.add(application)

        app.mysql_session.commit()

    @classmethod
    def tearDownClass(cls):
        app.mysql_session.execute('DELETE FROM applications;')
        app.mysql_session.execute('DELETE FROM clients;')
        app.mysql_session.execute('DELETE FROM departments;')
        app.mysql_session.commit()

    def setUp(self):
        # creates a test client
        self.client = app.test_client()
        # propagate the exceptions to the test client
        self.client.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('MyTitle', str(result.data))

        soup = BeautifulSoup(str(result.data), 'html.parser')
        self.assertEqual(soup.title.text, 'MyTitle - Dashboard')

        tree = html.fromstring(result.data)
        login_list = tree.xpath('//html/body/nav/ul/li[3]/div/a[3]/text()')
        self.assertEqual(login_list[0], 'Login')

    def test_departments(self):
        result = self.client.get('/departments')

        self.assertEqual(result.status_code, 200)

        soup = BeautifulSoup(str(result.data), 'html.parser')
        self.assertEqual(soup.title.text, 'Departments')

        self.assertIn('Kyiv', str(result.data))
