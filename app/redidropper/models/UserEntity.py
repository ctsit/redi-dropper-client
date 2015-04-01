from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Examples:
# http://stackoverflow.com/questions/17972020/how-to-execute-raw-sql-in-sqlalchemy-flask-app
# http://www.dangtrinh.com/2013/06/sqlalchemy-python-module-with-mysql.html
# http://www.pythoncentral.io/sqlalchemy-orm-examples/

Base = declarative_base()

class UserEntity(Base):
    __tablename__ = 'User'

    usrID = Column(Integer, primary_key=True)
    usrEmail = Column(String(255))
    usrFirst = Column(String(255))
    usrLast = Column(String(255))

    def __init__(self, usrEmail, usrFirst, usrLast):
        self.usrEmail = usrEmail
        self.usrFirst = usrFirst
        self.usrLast = usrLast

    def __repr__(self):
        return "<UserEntity(%s, %s, %s)>" % (self.usrEmail, self.usrFirst, self.usrLast)


user = 'redidropper'
passwd = 'insecurepassword'
host = 'localhost'
db_name = 'RediDropper'

engine = create_engine('mysql://{}:{}@{}/{}'.format(user, passwd, host, db_name))

Session = scoped_session(sessionmaker(bind=engine))
sess = Session()

user = UserEntity("test@test.com", "usrFirst", "usrLast")
sess.add(user)
sess.commit()


users = sess.query(UserEntity).filter_by(usrEmail='test@test.com')
all_users = sess.query(UserEntity).all()
print users
print all_users

