"""Module contains models for object–relational mapping (ORM) communication with a database. """
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class Quiz(Base):
    """Quiz database table model. """
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime)

    questions = relationship("Question", backref=backref("quiz"))

    def __repr__(self):
        """ Model objects representation. It is to represent a class object as text. """
        return f'<Quiz(name=\'{self.name}\', description=\'{self.description}\', ' \
               f'date=\'{self.date}\', questions=\'{self.questions}\')>'


class Question(Base):
    """Question database table model. """
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id"))
    text = Column(Text, nullable=False)
    image_path = Column(Text)
    comment = Column(Text)

    answers = relationship("Answer", backref=backref("question"))
    user_data = relationship("QuestionUserData", backref=backref("question"), uselist=False)

    def __repr__(self):
        """ Model objects representation. It is to represent a class object as text. """
        return f'<Question (id=\'{self.id}\', quiz_id=\'{self.quiz_id}\', ' \
               f'text=\'{self.text}\', answers=\'{self.answers}\', user_data=\'{self.user_data}\')>'


class QuestionUserData(Base):
    """Question user data database table model. """
    __tablename__ = 'question_user_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    level = Column(Integer, nullable=False)
    correct_answer = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    def __repr__(self):
        """ Model objects representation. It is to represent a class object as text. """
        return f'<QuestionProgress (id=\'{self.id}\', question_id=\'{self.question_id}\', ' \
               f'level=\'{self.level}\', correct_answer=\'{self.correct_answer}\', comment=\'comment\')>'


class Answer(Base):
    """Answer database table model. """
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean)

    def __repr__(self):
        """ Model objects representation. It is to represent a class object as text. """
        return f'<Answer (id=\'{self.id}\', question_id=\'{self.question_id}\', ' \
               f'text=\'{self.text}\', is_correct=\'{self.is_correct}\')>'


class Version(Base):
    """Version database table model. """
    __tablename__ = 'version'

    id = Column(Integer, primary_key=True, autoincrement=True)
    major = Column(Integer, nullable=False)
    minor = Column(Integer, nullable=False)
    patch = Column(Integer, nullable=False)

    def __repr__(self):
        """ Model objects representation. It is to represent a class object as text. """
        return f'<Version (id=\'{self.id}\', major=\'{self.major}\', minor=\'{self.minor}\', patch=\'{self.patch}\')>'
