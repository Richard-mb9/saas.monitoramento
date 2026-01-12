from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from config import HOST_DB, PASSWORD_DB, USER_DB, PORT_DB, NAME_DB


class DatabaseManagerConnection:
    """class to manage database connection"""

    def __init__(self):
        self.connect()

    def connect(self):
        self.url_db = (
            f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"
        )
        self.engine = self.engine = create_engine(
            self.url_db, pool_size=25, max_overflow=10
        )
        self.session: scoped_session[Session] = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

    def close_session(self):
        self.session.close()
        self.engine.dispose()

    def commit(self):
        self.session.commit()
