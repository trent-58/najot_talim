# Quick Start Guide - CRUD Operations

## Running the Project

```bash
python manage.py runserver
```

Then visit: `http://localhost:8000/`

---

## Markaz App - Complete CRUD

### Students
- **List**: `/markaz/students/`
- **Add**: `/markaz/students/add`
- **View**: `/markaz/students/<id>`
- **Edit**: `/markaz/students/<id>/edit`
- **Delete**: Click Delete on student detail page

### Instructors
- **List**: `/markaz/instructors/`
- **Add**: `/markaz/instructors/add`
- **View**: `/markaz/instructors/<id>`
- **Edit**: `/markaz/instructors/<id>/edit`
- **Delete**: Click Delete on instructor detail page

### Courses
- **List**: `/markaz/courses/`
- **Add**: `/markaz/courses/add`
- **View**: `/markaz/courses/<id>`
- **Edit**: `/markaz/courses/<id>/edit`
- **Delete**: Click Delete on course detail page

### Enrollments
- **List**: `/markaz/enrollments/`
- **Add**: `/markaz/enrollments/add`
- **View**: `/markaz/enrollments/<id>`
- **Edit**: `/markaz/enrollments/<id>/edit`
- **Delete**: Click Delete on enrollment detail page

---

## Texnika App - Complete CRUD

### Items
- **List**: `/texnika/items/`
- **Add**: `/texnika/items/add`
- **View**: `/texnika/items/<id>`
- **Edit**: `/texnika/items/<id>/edit`
- **Delete**: Click Delete on item detail page

### Categories
- **List**: `/texnika/categories/`
- **Add**: `/texnika/categories/add`
- **View**: `/texnika/categories/<id>`
- **Edit**: `/texnika/categories/<id>/edit`
- **Delete**: Click Delete on category detail page

### Manufacturers
- **List**: `/texnika/manufacturers/`
- **Add**: `/texnika/manufacturers/add`
- **View**: `/texnika/manufacturers/<id>`
- **Edit**: `/texnika/manufacturers/<id>/edit`
- **Delete**: Click Delete on manufacturer detail page

---

## Features

✅ Create new records with forms
✅ Read/View detailed information
✅ Update/Edit existing records
✅ Delete records with confirmation dialog
✅ Image upload support (Students, Instructors, Items)
✅ Foreign key relationships (Enrollment, Items)
✅ Responsive navigation with back buttons
✅ Simple, clean HTML styling (no CSS framework)

---

## Database Models

### Markaz App
- **Student**: first_name, last_name, image
- **Instructor**: name, hire_date, image
- **Course**: title, description
- **Enrollment**: student(FK), course(FK), instructor(FK), enrollment_date

### Texnika App
- **Item**: name, description, image, category_fk(FK), manufacturer_fk(FK)
- **Category**: title
- **Manufacturer**: name, country

---

## Technical Details

- Framework: Django
- Database: SQLite (default)
- Forms: Django ModelForms
- Templates: Simple HTML with form.as_p
- File Uploads: UUID-based naming with folder organization
- URLs: Named routes for easy linking

---

## Tips

1. **For Image Upload**: Make sure `/media/` directory exists and DEBUG=True in settings
2. **Foreign Keys**: When adding Enrollments, select from existing Students, Courses, and Instructors
3. **Date Fields**: Enrollment and Instructor hire dates use HTML5 date picker
4. **Navigation**: Every page has a "Back" button to maintain context
5. **URL Naming**: All URL names are descriptive (e.g., 'show_student', 'edit_course')

