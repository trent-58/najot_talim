from django.urls import path

from .views import (
    index,
    students,
    add_student,
    show_student,
    edit_student,
    instructors,
    add_instructor,
    show_instructor,
    edit_instructor,
    courses,
    add_course,
    show_course,
    edit_course,
    enrollments,
    add_enrollment,
    show_enrollment,
    edit_enrollment,
)

urlpatterns = [
    path("", index, name="markaz"),
    # Students
    path("students/", students, name="students"),
    path("students/add", add_student, name="add_student"),
    path("students/<int:pk>", show_student, name="show_student"),
    path("students/<int:pk>/edit", edit_student, name="edit_student"),
    # Instructors
    path("instructors/", instructors, name="instructors"),
    path("instructors/add", add_instructor, name="add_instructor"),
    path("instructors/<int:pk>", show_instructor, name="show_instructor"),
    path("instructors/<int:pk>/edit", edit_instructor, name="edit_instructor"),
    # Courses
    path("courses/", courses, name="courses"),
    path("courses/add", add_course, name="add_course"),
    path("courses/<int:pk>", show_course, name="show_course"),
    path("courses/<int:pk>/edit", edit_course, name="edit_course"),
    # Enrollments
    path("enrollments/", enrollments, name="enrollments"),
    path("enrollments/add", add_enrollment, name="add_enrollment"),
    path("enrollments/<int:pk>", show_enrollment, name="show_enrollment"),
    path("enrollments/<int:pk>/edit", edit_enrollment, name="edit_enrollment"),
]
