from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('connection string')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Urls(Base):
    __tablename__ = 'urls'
    url_id = Column(Integer, primary_key=True)
    input_url = Column(String(50))
    short_link = Column(String(50))
    date = Column(String(120), unique=True)

    def __init__(self, url_id=None, input_url=None, short_link=None, date=None):
        self.url_id = url_id
        self.input_url = input_url
        self.short_link = short_link
        self.date = date

    def __repr__(self):
        return '{} {} {} {}'.format(self.url_id, self.input_url, self.short_link, self.date)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
