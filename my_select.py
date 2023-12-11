from sqlalchemy import func, desc, select, and_

# Імпорт необхідних моделей та сесії бази даних
from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_01():
    """
    --1. Знайти 5 студентів з найвищим середнім балом по всіх предметах.
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    """
    --2. Знайти студента з найвищим середнім балом по конкретному предмету.
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


def select_03():
    """
    --3. Знайти середній бал в групах по конкретному предмету.
    """
    result = session.query(Student.group_id, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.group_id) \
        .order_by(Student.group_id).all()
    return result


def select_04():
    """
    --4. Знайти середній бал по всіх оцінках.
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade).all()
    return result


def select_05():
    """
    --5. Знайти предмети, які викладає конкретний вчитель.
    """
    result = session.query(Teacher.fullname, Subject.name) \
        .select_from(Teacher).join(Subject).filter(Teacher.id == 1).all()
    return result


def select_06():
    """
    --6. Знайти список студентів у конкретній групі.
    """
    result = session.query(Student.fullname).select_from(Student).filter(Student.group_id == 1).all()
    return result


def select_07():
    """
    --7. Знайти оцінки студентів у конкретній групі по конкретному предмету.
    """
    result = session.query(Student.fullname, Grade.grade) \
        .select_from(Student).join(Grade).filter(and_(Student.group_id == 1, Grade.subjects_id == 1)).all()
    return result


def select_08():
    """
    --8. Знайти середній бал, який виставив конкретний вчитель у своїх предметах.
    """
    result = session.query(Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .select_from(Teacher).join(Subject).join(Grade).filter(Teacher.id == 1)\
        .group_by(Teacher.fullname, Subject.name).all()
    return result


def select_09():
    """
    --9. Знайти список предметів, які вивчає конкретний студент.
    """
    result = session.query(Subject.name).select_from(Grade).join(Subject).filter(Grade.student_id == 1)\
        .group_by(Subject.id).all()
    return result


def select_10():
    """
    --10. Знайти список предметів, які вивчає конкретний вчитель у конкретного студента.
    """
    result = session.query(Subject.name).select_from(Grade).join(Subject)\
        .filter(and_(Subject.teacher_id == 1, Grade.student_id == 1))\
        .group_by(Subject.name).all()
    return result


def select_11():
    """
    --11. Знайти середній бал, який виставив конкретний вчитель конкретному студентові.
    """
    result = session.query(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade'))\
        .select_from(Grade).join(Student).join(Subject).join(Teacher)\
        .filter(and_(Grade.student_id == 1, Teacher.id == 1)).group_by(Student.fullname, Teacher.fullname).all()
    return result


def select_12():
    """
    --12. Знайти останню оцінку конкретного студента з конкретного предмета.
    """
    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subjects_id == 2, Student.group_id == 3
    ))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.grade_date == subquery)).all()

    return result


if __name__ == '__main__':
    print(select_01())
    print(select_02())
    print(select_03())
    print(select_04())
    print(select_05())
    print(select_06())
    print(select_07())
    print(select_08())
    print(select_09())
    print(select_10())
    print(select_11())
    print(select_12())
