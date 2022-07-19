"""Database manager. It is used to add new questions to existing database. """
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.database_model import Quiz, Question, QuestionProgress, Answer, Base, Version
from src.question_model import QuizModel

DATABASE_PREFIX = 'sqlite:///'
DATABASE_VERSION = (0, 0, 1)


def add_quiz(database_path: str, model: QuizModel) -> None:
    """Add new quiz to existing database.
    It may raise SQLite3 exception if there will be problem with the database file.
    """
    engine = create_engine(DATABASE_PREFIX + database_path, echo=False)

    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()

    questions = []
    for question in model.questions:
        questions.append(Question(text=question.text,
                                  image_path=question.image_path,
                                  comment=question.comment,
                                  user_comment=question.user_comment,
                                  answers=[Answer(**answer.dict()) for answer in question.answers],
                                  progress=[QuestionProgress(**question_progress.dict())
                                            for question_progress in question.progress]
                                  ))
    model_orm = Quiz(name=model.name, description=model.description, questions=questions)
    session.add(model_orm)
    session.commit()


def get_quizzes(database_path: str) -> Optional[List[QuizModel]]:
    """Returns list of object representation of quizzes stored in a database. """
    engine = create_engine(DATABASE_PREFIX + database_path, echo=False)

    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()

    quizzes_orm_objects = session.query(Quiz).all()

    return [QuizModel.from_orm(quiz_orm) for quiz_orm in quizzes_orm_objects]


def create_database(database_path: str):
    """ Create database in path, initialised tables and put record with database version. """
    engine = create_engine(DATABASE_PREFIX + database_path, echo=False)
    Base.metadata.create_all(engine)

    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()

    version_model = Version(major=DATABASE_VERSION[0], minor=DATABASE_VERSION[1], patch=DATABASE_VERSION[2])
    session.add(version_model)
    session.commit()
