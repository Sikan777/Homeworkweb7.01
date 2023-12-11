import logging
import random
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

# Імпорт необхідних бібліотек та модулів
from conf.db import session
from conf.models import Grade, Teacher, Student, Group, Subject

# Створення об'єкту Faker для генерації випадкових даних
fake = Faker('uk-Ua')

# Додавання груп
def insert_groups():
    for _ in range(3):
        group = Group(
            name=fake.word()
        )
        session.add(group)

# Додавання вчителів
def insert_teachers():
    for _ in range(3):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)

# Додавання предметів з вказанням вчителя
def insert_subjects():
    teachers = session.query(Teacher).all()
    for _ in range(5):
        subject = Subject(
            name=fake.word(),
            teacher_id=random.choice(teachers).id
        )
        session.add(subject)

# Додавання студентів з вказанням групи
def insert_students():
    groups = session.query(Group).all()
    for _ in range(40):
        student = Student(
            fullname=fake.name(),
            group_id=random.choice(groups).id
        )
        session.add(student)

# Додавання оцінок
def insert_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()

    for student in students:
        number_of_grades = random.randint(10, 20)
        for _ in range(number_of_grades):
            grade = Grade(
                grade=random.randint(0, 100),
                grade_date=fake.date_this_decade(),
                student_id=student.id,
                subjects_id=random.choice(subjects).id
            )
            session.add(grade)

# Основний блок програми
if __name__ == '__main__':
    try:
        # Виклик функції, яка додає групи
        insert_groups()
        # Виклик функції, яка додає вчителів
        insert_teachers()
        session.commit()

        # Виклик функції, яка додає предмети
        insert_subjects()
        # Виклик функції, яка додає студентів
        insert_students()
        session.commit()

        # Виклик функції, яка додає оцінки
        insert_grades()
        session.commit()

    except SQLAlchemyError as e:
        # Обробка помилок та виведення в консоль
        logging.error(e)
        # Відкат транзакції в разі помилки
        session.rollback()
    finally:
        # Закриття сесії
        session.close()