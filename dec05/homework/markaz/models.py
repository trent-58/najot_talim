from django.db import models
import os
import uuid


def upload_to(instance, filename):
    ext = filename.split(".")[-1]
    folder = instance.__class__.__name__.lower()
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(folder, filename)


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    hire_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    def __str__(self):
        return (
            f"{self.student} enrolled in {self.course} instructed by {self.instructor}"
        )


