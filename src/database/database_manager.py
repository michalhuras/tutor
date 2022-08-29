"""Database manager. It is used to add new questions to existing database. """
from typing import List

from sqlalchemy import create_engine, update, exists
from sqlalchemy.orm import sessionmaker

from src.database.database_model import Quiz, Question, QuestionUserData, Answer, Base, Version
from src.database.singleton_meta import SingletonMeta
from src.question_model import QuizModel, QuestionUserDataModel


class DatabaseManager(metaclass=SingletonMeta):
    """Database manager class. """
    DATABASE_PREFIX = 'sqlite:///'
    DATABASE_VERSION = (0, 0, 1)

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.engine = create_engine(self.DATABASE_PREFIX + database_path, echo=False)
        # TODO exception if the database doesn't exist

        SessionClass = sessionmaker(bind=self.engine)
        self.session = SessionClass()

    def add_quiz(self, model: QuizModel) -> None:
        """Add new quiz to existing database.
        It may raise SQLite3 exception if there will be problem with the database file.
        """
        questions = []
        for question in model.questions:
            questions.append(Question(id=question.id,
                                      text=question.text,
                                      image_path=question.image_path,
                                      comment=question.comment,
                                      answers=[Answer(**answer.dict()) for answer in question.answers],
                                      user_data=
                                      QuestionUserData(**question.user_data.dict()) if question.user_data else None
                                      ))
        model_orm = Quiz(id=model.id, name=model.name, description=model.description, questions=questions)
        self.session.add(model_orm)
        self.session.commit()

    def get_quizzes(self) -> List[QuizModel]:
        """Returns list of object representation of quizzes stored in a database. """
        quizzes_orm_objects = self.session.query(Quiz).all()

        return [QuizModel.from_orm(quiz_orm) for quiz_orm in quizzes_orm_objects]

    def get_quizzes_names(self) -> List[str]:
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
        self.session.query(QuestionUserData).delete()
        self.session.query(Question).delete()
        self.session.query(Quiz).delete()
        self.session.commit()

    def update_question_user_data(self, user_data_model: QuestionUserDataModel, question_id: int) -> None:
        """Update a question's user note and progress parameters. """
        if not self.session.query(exists().where(QuestionUserData.question_id == question_id)).scalar():
            question_user_data = QuestionUserData(**user_data_model.dict())
            question_user_data.question_id = question_id
            self.session.add(question_user_data)
            self.session.commit()
        else:
            query = update(QuestionUserData) \
                .where(QuestionUserData.id == question_id) \
                .values(level=user_data_model.level,
                        correct_answer=user_data_model.correct_answer,
                        comment=user_data_model.comment) \
                .execution_options(synchronize_session="fetch")
            self.session.execute(query)
            self.session.commit()

    @classmethod
    def create_database(cls, database_path: str):
        """ Create database in path, initialised tables and put record with database version. """
        engine = create_engine(cls.DATABASE_PREFIX + database_path, echo=False)
        Base.metadata.create_all(engine)

        SessionClass = sessionmaker(bind=engine)
        session = SessionClass()

        version_model = Version(
            major=cls.DATABASE_VERSION[0], minor=cls.DATABASE_VERSION[1], patch=cls.DATABASE_VERSION[2])
        session.add(version_model)
        session.commit()

# DatabaseManager.create_database('./data/quiz.db')
