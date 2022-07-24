"""Database manager. It is used to add new questions to existing database. """
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.database_model import Quiz, Question, QuestionProgress, Answer, Base, Version
from src.database.singleton_meta import SingletonMeta
from src.question_model import QuizModel


class DatabaseManager(metaclass=SingletonMeta):
    """Database manager class. """
    DATABASE_PREFIX = 'sqlite:///'
    DATABASE_VERSION = (0, 0, 1)

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.engine = create_engine(self.DATABASE_PREFIX + database_path, echo=True)
        # TODO exception if the database doesn't exist

        SessionClass = sessionmaker(bind=self.engine)
        self.session = SessionClass()

    def add_quiz(self, model: QuizModel) -> None:
        """Add new quiz to existing database.
        It may raise SQLite3 exception if there will be problem with the database file.
        """
        questions = []
        for question in model.questions:
            questions.append(Question(text=question.text,
                                      image_path=question.image_path,
                                      comment=question.comment,
                                      user_comment=question.user_comment,
                                      answers=[Answer(**answer.dict()) for answer in question.answers],
                                      progress=QuestionProgress(**question.progress.dict()) if question.progress else None
                                      ))
        model_orm = Quiz(name=model.name, description=model.description, questions=questions)
        self.session.add(model_orm)
        self.session.commit()

    def get_quizzes(self) -> List[QuizModel]:
        """Returns list of object representation of quizzes stored in a database. """
        quizzes_orm_objects = self.session.query(Quiz).all()

        [print(quiz_orm) for quiz_orm in quizzes_orm_objects]
        return [QuizModel.from_orm(quiz_orm) for quiz_orm in quizzes_orm_objects]

    def get_quizzes_names(self) -> List[QuizModel]:
        """Return quizzes names. """
        quizzes_orm_objects = self.session.query(Quiz.name).all()

        return [quiz_orm[0] for quiz_orm in quizzes_orm_objects]

    def get_quiz(self, quiz_name: str) -> QuizModel:
        """Return quiz object. """
        quizzes_orm = self.session.query(Quiz).filter(Quiz.name.is_(quiz_name)).all()

        return QuizModel.from_orm(quizzes_orm[0])

    def erase_all_quizzes(self) -> None:
        """Erase all quizzes from a database including depending on structures as questions and answers. """
        self.session.query(Answer).delete()
        self.session.query(QuestionProgress).delete()
        self.session.query(Question).delete()
        self.session.query(Quiz).delete()
        self.session.commit()

    @classmethod
    def create_database(cls, database_path: str):
        """ Create database in path, initialised tables and put record with database version. """
        print(database_path)
        engine = create_engine(cls.DATABASE_PREFIX + database_path, echo=False)
        Base.metadata.create_all(engine)

        SessionClass = sessionmaker(bind=engine)
        session = SessionClass()

        version_model = Version(
            major=cls.DATABASE_VERSION[0], minor=cls.DATABASE_VERSION[1], patch=cls.DATABASE_VERSION[2])
        session.add(version_model)
        session.commit()

# create_database('./data/quiz.db')
