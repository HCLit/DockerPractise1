from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, default='')
    lessons = relationship('Lesson', back_populates='course', cascade='all, delete-orphan')

class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    title = Column(String(255), nullable=False)
    slide_filename = Column(String(255), nullable=False)
    notes = Column(Text, default='')
    index = Column(Integer, nullable=False)

    course = relationship('Course', back_populates='lessons')
