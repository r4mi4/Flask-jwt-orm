from app.database import Column, Table


class Users(Table):
    username = Column('uniqe')
    password = Column(str)
    email = Column('uniqe')
    image = Column(str)
    bio = Column(str)
    phone_number = Column(str)

