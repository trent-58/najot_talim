from django.shortcuts import render, redirect
from .models import Student, Instructor, Course, Enrollment
from django import forms


# ======================== MARKAZ MAIN PAGE ===========================
def index(request):
    items = [
        {
            "name": "Students",
            "path": "students/",
        },
        {
            "name": "Instructor",
            "path": "instructors/",
        },
        {
            "name": "Courses",
            "path": "courses/",
        },
        {
            "name": "Enrollments",
            "path": "enrollments/",
        },
    ]
    return render(request, "index.html", {"items": items})


# ======================== Manage Students ===========================
class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "image"]


def show_student(request, pk):
    student = Student.objects.get(pk=pk)

    if request.method == "POST":
        student.delete()
        return redirect("students")

    return render(
        request, "show_student.html", {"student": student, "back": "students"}
    )


def delete_student(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()


def add_student(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            return redirect("show_student", pk=student.pk)
    else:
        form = AddStudentForm()

    return render(
        request, "add.html", {"form": form, "title": "Add Student", "back": "students"}
    )


def students(request):
    students = Student.objects.all()
    return render(
        request,
        "list.html",
        {
            "items": students,
            "title": "Students",
            "back": "markaz",
            "add": "Add Student",
        },
    )


# ==================================== Manage Instructors ===============================================================
def instructors(request):
    instructors = Instructor.objects.all()
    return render(
        request,
        "list.html",
        {
            "items": instructors,
            "title": "Instructors",
            "back": "markaz",
            "add": "Add Instructor",
        },
    )


class AddInstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ["name", "hire_date", "image"]

        widgets = {
            "hire_date": forms.DateInput(attrs={"type": "date"}),  # HTML5 date picker
        }


def add_instructor(request):
    if request.method == "POST":
        form = AddInstructorForm(request.POST, request.FILES)
        if form.is_valid():
            instructor = form.save()
            return redirect("show_instructor", pk=instructor.pk)
    else:
        form = AddInstructorForm()

    return render(
        request,
        "add.html",
        {"form": form, "title": "Add Instructor", "back": "instructors"},
    )


def delete_instructor(request, pk):
    instructor = Instructor.objects.get(pk=pk)
    instructor.delete()


def show_instructor(request, pk):
    instructor = Instructor.objects.get(pk=pk)

    if request.method == "POST":
        instructor.delete()
        return redirect("instructors")

    return render(
        request,
        "show_instructor.html",
        {"instructor": instructor, "back": "instructors"},
    )


# ======================================== Manage Courses =====================================
def courses(request):
    courses = Course.objects.all()
    return render(request, "courses.html", {"items": courses})


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description"]


def add_course(request):
    if request.method == "POST":
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            return redirect("show_course", pk=course.pk)
    else:
        form = AddCourseForm()

    return render(
        request,
        "add_course.html",
        {"form": form, "title": "Add Course", "back": "courses"},
    )


def show_course(request, pk):
    course = Course.objects.get(pk=pk)

    if request.method == "POST":
        course.delete()
        return redirect("courses")

    return render(request, "show_course.html", {"course": course, "back": "courses"})


# ======================================== Manage Enrollments =====================================
class AddEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["student", "course", "instructor", "enrollment_date"]
        widgets = {
            "enrollment_date": forms.DateInput(attrs={"type": "date"}),
        }


def enrollments(request):
    enrollments = Enrollment.objects.all()
    return render(
        request,
        "list.html",
        {
            "items": enrollments,
            "title": "Enrollments",
            "back": "markaz",
            "add": "Add Enrollment",
        },
    )


def add_enrollment(request):
    if request.method == "POST":
        form = AddEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            return redirect("show_enrollment", pk=enrollment.pk)
    else:
        form = AddEnrollmentForm()

    return render(
        request,
        "add.html",
        {"form": form, "title": "Add Enrollment", "back": "enrollments"},
    )


def show_enrollment(request, pk):
    enrollment = Enrollment.objects.get(pk=pk)

    if request.method == "POST":
        enrollment.delete()
        return redirect("enrollments")

    return render(
        request,
        "show_enrollment.html",
        {"enrollment": enrollment, "back": "enrollments"},
    )


def edit_student(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == "POST":
        form = AddStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("show_student", pk=student.pk)
    else:
        form = AddStudentForm(instance=student)

    return render(
        request, "add.html", {"form": form, "title": "Edit Student", "back": "students"}
    )


def edit_instructor(request, pk):
    instructor = Instructor.objects.get(pk=pk)
    if request.method == "POST":
        form = AddInstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect("show_instructor", pk=instructor.pk)
    else:
        form = AddInstructorForm(instance=instructor)

    return render(
        request,
        "add.html",
        {"form": form, "title": "Edit Instructor", "back": "instructors"},
    )


def edit_course(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == "POST":
        form = AddCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("show_course", pk=course.pk)
    else:
        form = AddCourseForm(instance=course)

    return render(
        request,
        "add_course.html",
        {"form": form, "title": "Edit Course", "back": "courses"},
    )


def edit_enrollment(request, pk):
    enrollment = Enrollment.objects.get(pk=pk)
    if request.method == "POST":
        form = AddEnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect("show_enrollment", pk=enrollment.pk)
    else:
        form = AddEnrollmentForm(instance=enrollment)

    return render(
        request,
        "add.html",
        {"form": form, "title": "Edit Enrollment", "back": "enrollments"},
    )
