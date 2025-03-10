from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from conf.db import SessionLocal
from entity.models import Student, Group, Teacher, Subject, Grade
from colorama import Fore, Style, init

session: Session = SessionLocal()

init(autoreset=True)

def round_results(results):
    if isinstance(results, tuple):
        return tuple(
            round(value, 2) if isinstance(value, float) else value for value in results
        )
    elif isinstance(results, list):
        return [round_results(result) for result in results]
    return results


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    result = (
        session.query(Student.name, func.avg(Grade.value).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
        .all()
    )
    return round_results(result)


# 2. Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject_name):
    result = (
        session.query(Student.name, func.avg(Grade.value).label("average_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .first()
    )
    if result:
        return round_results([result])[0]
    return result


# 3. Знайти середній бал у групах з певного предмета
def select_3(subject_name):
    SubjectAlias = aliased(Subject)

    query = (
        session.query(Group.name, func.avg(Grade.value).label("average_grade"))
        .select_from(Group)
        .join(Student)
        .join(Grade, Grade.student_id == Student.id)
        .join(SubjectAlias, SubjectAlias.id == Grade.subject_id)
        .filter(SubjectAlias.name == subject_name)
        .group_by(Group.name)
        .all()
    )

    return round_results(query)


# 4. Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4():
    result = session.query(func.avg(Grade.value).label("average_grade")).scalar()
    if result is not None:
        return round(result, 2)
    return result


# 5. Знайти які курси читає певний викладач
def select_5(teacher_name):
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return result


# 6. Знайти список студентів у певній групі
def select_6(group_name):
    result = (
        session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    )
    return result


# 7. Знайти оцінки студентів у окремій групі з певного предмета
def select_7(group_name, subject_name):
    result = (
        session.query(Student.name, Grade.value)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_name):
    result = (
        session.query(func.avg(Grade.value).label("average_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return round(result, 2) if result is not None else result


# 9. Знайти список курсів, які відвідує певний студент
def select_9(student_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .all()
    )
    return result


# 10. Список курсів, які певному студенту читає певний викладач
def select_10(student_name, teacher_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .all()
    )
    return result


# Функція для виведення результатів
def print_query_result(query_result, title):
    print(Fore.CYAN + Style.BRIGHT + title)
    if query_result:
        for row in query_result:
            print(Fore.GREEN + str(row))
    else:
        print(Fore.RED + "No results found.")
    print("\n" + "-" * 50)


if __name__ == "__main__":
    # Приклад використання функцій з кольоровим виведенням та округленням
    print_query_result(select_1(), "Top 5 Students by Average Grade")

    student_2 = select_2("Намір")
    if student_2:
        print_query_result([student_2], "Student with Highest Average in 'Намір'")
    else:
        print(Fore.RED + "No student found with the highest average in 'Намір.")

    select_3_result = select_3("Упор")
    if select_3_result:
        print_query_result(select_3_result, "Average Grade by Groups in 'Упор'")
    else:
        print(Fore.RED + "No groups found for the subject 'Упор'.")

    overall_avg = select_4()
    if overall_avg is not None:
        print(Fore.YELLOW + f"Overall Average Grade: {overall_avg}")
    else:
        print(Fore.RED + "No average grade found.")

    select_5_result = select_5("Вадим Франчук")
    if select_5_result:
        print_query_result(select_5_result, "Courses Taught by 'Вадим Франчук'")
    else:
        print(Fore.RED + "No courses found taught by 'Вадим Франчук'")

    select_6_result = select_6("Group 1")
    if select_6_result:
        print_query_result(select_6_result, "Students in Group 1")
    else:
        print(Fore.RED + "No students found in Group 1.")

    select_7_result = select_7("Group 1", "Сходити")
    if select_7_result:
        print_query_result(select_7_result, "Grades in Group 1 for 'Сходити'")
    else:
        print(Fore.RED + "No grades found in Group 1 for the 'Сходити' subject.")

    avg_8 = select_8("Данна Затовканюк")
    if avg_8 is not None:
        print(Fore.YELLOW + f"Данна 'Затовканюк' Average Grade: {avg_8}")
    else:
        print(Fore.RED + "No average grade found for 'Данна Затовканюк'")

    select_9_result = select_9("Пріска Пушкар")
    if select_9_result:
        print_query_result(select_9_result, "Courses Attended by 'Пріска Пушкар'")
    else:
        print(Fore.RED + "No courses found for 'Пріска Пушкар'")

    select_10_result = select_10("Максим Гречаник", "Адам Литвин")
    if select_10_result:
        print_query_result(
            select_10_result, "Courses Taught by Адам Литвин to Максим Гречаник"
        )
    else:
        print(Fore.RED + "No courses found for Максим Гречаник taught by Адам Литвин.")
