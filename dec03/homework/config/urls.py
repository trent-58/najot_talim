from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from markaz.models import Student, Course, Instructor, Enrollment

def home_view(request):
    return render(request, 'home.html')

def texnika_gallery_view(request):
    return render(request, 'gallery.html')

def image_detail_view(request, image_id):
    # Image data mapping
    images = {
        1: {
            'title': 'Image 1',
            'description': 'This is the first image in our gallery. It showcases beautiful visuals and artistic composition.',
            'filename': 'Untitled.jpg',
            'path': '/media/items/Untitled.jpg',
            'previous': None,
            'next': 2
        },
        2: {
            'title': 'Image 2',
            'description': 'This is the second image in our collection. Explore the stunning details and rich colors.',
            'filename': 'Untitled1.jpg',
            'path': '/media/items/Untitled1.jpg',
            'previous': 1,
            'next': 3
        },
        3: {
            'title': 'Image 3',
            'description': 'This is the third and final image in our gallery. A perfect ending to the visual journey.',
            'filename': 'Untitled2.jpg',
            'path': '/media/items/Untitled2.jpg',
            'previous': 2,
            'next': None
        }
    }
    
    if image_id not in images:
        return render(request, 'gallery.html')
    
    image_data = images[image_id]
    context = {
        'image_number': image_id,
        'image_title': image_data['title'],
        'image_description': image_data['description'],
        'image_filename': image_data['filename'],
        'image_path': image_data['path'],
        'previous_image': image_data['previous'],
        'next_image': image_data['next']
    }
    
    return render(request, 'image_detail.html', context)

def markaz_gallery_view(request):
    return render(request, 'markaz_gallery.html')

def markaz_students_view(request, student_id=None):
    students = list(Student.objects.all())
    
    if not students:
        return render(request, 'markaz_gallery.html')
    
    if student_id is None or student_id not in [s.id for s in students]:
        student_id = students[0].id
    
    student = Student.objects.get(id=student_id)
    current_index = next(i for i, s in enumerate(students) if s.id == student_id) + 1
    
    previous_id = None
    next_id = None
    
    for i, s in enumerate(students):
        if s.id == student_id:
            if i > 0:
                previous_id = students[i - 1].id
            if i < len(students) - 1:
                next_id = students[i + 1].id
            break
    
    context = {
        'title': f'{student.first_name} {student.last_name}',
        'type_label': 'Students',
        'item_type': 'students',
        'items': [
            {'label': 'First Name', 'value': student.first_name},
            {'label': 'Last Name', 'value': student.last_name},
            {'label': 'ID', 'value': f'#{student.id}'},
        ],
        'description': f'Student profile for {student.first_name} {student.last_name}. This is a registered student in our education center.',
        'current_index': current_index,
        'total_count': len(students),
        'previous_id': previous_id,
        'next_id': next_id,
    }
    
    return render(request, 'markaz_detail.html', context)

def markaz_courses_view(request, course_id=None):
    courses = list(Course.objects.all())
    
    if not courses:
        return render(request, 'markaz_gallery.html')
    
    if course_id is None or course_id not in [c.id for c in courses]:
        course_id = courses[0].id
    
    course = Course.objects.get(id=course_id)
    current_index = next(i for i, c in enumerate(courses) if c.id == course_id) + 1
    
    previous_id = None
    next_id = None
    
    for i, c in enumerate(courses):
        if c.id == course_id:
            if i > 0:
                previous_id = courses[i - 1].id
            if i < len(courses) - 1:
                next_id = courses[i + 1].id
            break
    
    context = {
        'title': course.title,
        'type_label': 'Courses',
        'item_type': 'courses',
        'items': [
            {'label': 'Course Title', 'value': course.title},
            {'label': 'Course ID', 'value': f'#{course.id}'},
            {'label': 'Status', 'value': 'Active'},
        ],
        'description': f'{course.description}',
        'current_index': current_index,
        'total_count': len(courses),
        'previous_id': previous_id,
        'next_id': next_id,
    }
    
    return render(request, 'markaz_detail.html', context)

def markaz_instructors_view(request, instructor_id=None):
    instructors = list(Instructor.objects.all())
    
    if not instructors:
        return render(request, 'markaz_gallery.html')
    
    if instructor_id is None or instructor_id not in [i.id for i in instructors]:
        instructor_id = instructors[0].id
    
    instructor = Instructor.objects.get(id=instructor_id)
    current_index = next(i for i, instr in enumerate(instructors) if instr.id == instructor_id) + 1
    
    previous_id = None
    next_id = None
    
    for i, instr in enumerate(instructors):
        if instr.id == instructor_id:
            if i > 0:
                previous_id = instructors[i - 1].id
            if i < len(instructors) - 1:
                next_id = instructors[i + 1].id
            break
    
    context = {
        'title': instructor.name,
        'type_label': 'Instructors',
        'item_type': 'instructors',
        'items': [
            {'label': 'Instructor Name', 'value': instructor.name},
            {'label': 'Instructor ID', 'value': f'#{instructor.id}'},
            {'label': 'Hire Date', 'value': instructor.hire_date.strftime('%Y-%m-%d')},
        ],
        'description': f'Instructor profile for {instructor.name}. Hired on {instructor.hire_date.strftime("%B %d, %Y")}.',
        'current_index': current_index,
        'total_count': len(instructors),
        'previous_id': previous_id,
        'next_id': next_id,
    }
    
    return render(request, 'markaz_detail.html', context)

def markaz_enrollments_view(request, enrollment_id=None):
    enrollments = list(Enrollment.objects.all())
    
    if not enrollments:
        return render(request, 'markaz_gallery.html')
    
    if enrollment_id is None or enrollment_id not in [e.id for e in enrollments]:
        enrollment_id = enrollments[0].id
    
    enrollment = Enrollment.objects.get(id=enrollment_id)
    current_index = next(i for i, e in enumerate(enrollments) if e.id == enrollment_id) + 1
    
    previous_id = None
    next_id = None
    
    for i, e in enumerate(enrollments):
        if e.id == enrollment_id:
            if i > 0:
                previous_id = enrollments[i - 1].id
            if i < len(enrollments) - 1:
                next_id = enrollments[i + 1].id
            break
    
    context = {
        'title': f'{enrollment.student.first_name} - {enrollment.course.title}',
        'type_label': 'Enrollments',
        'item_type': 'enrollments',
        'items': [
            {'label': 'Student', 'value': f'{enrollment.student.first_name} {enrollment.student.last_name}'},
            {'label': 'Course', 'value': enrollment.course.title},
            {'label': 'Instructor', 'value': enrollment.instructor.name},
            {'label': 'Enrollment Date', 'value': enrollment.enrollment_date.strftime('%Y-%m-%d')},
        ],
        'description': f'{enrollment.student.first_name} {enrollment.student.last_name} is enrolled in {enrollment.course.title} instructed by {enrollment.instructor.name}. Enrollment date: {enrollment.enrollment_date.strftime("%B %d, %Y")}.',
        'current_index': current_index,
        'total_count': len(enrollments),
        'previous_id': previous_id,
        'next_id': next_id,
    }
    
    return render(request, 'markaz_detail.html', context)

def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('', home_view, name='home'),
    path('texnika/gallery/', texnika_gallery_view, name='texnika_gallery'),
    path('image/<int:image_id>/', image_detail_view, name='image_detail'),
    path('markaz/gallery/', markaz_gallery_view, name='markaz_gallery'),
    path('markaz/students/', markaz_students_view, name='markaz_students_list'),
    path('markaz/students/<int:student_id>/', markaz_students_view, name='markaz_student_detail'),
    path('markaz/courses/', markaz_courses_view, name='markaz_courses_list'),
    path('markaz/courses/<int:course_id>/', markaz_courses_view, name='markaz_course_detail'),
    path('markaz/instructors/', markaz_instructors_view, name='markaz_instructors_list'),
    path('markaz/instructors/<int:instructor_id>/', markaz_instructors_view, name='markaz_instructor_detail'),
    path('markaz/enrollments/', markaz_enrollments_view, name='markaz_enrollments_list'),
    path('markaz/enrollments/<int:enrollment_id>/', markaz_enrollments_view, name='markaz_enrollment_detail'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)