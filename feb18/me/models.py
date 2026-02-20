from django.db import models


class Profile(models.Model):
    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    tagline = models.CharField(max_length=180)
    bio = models.TextField()
    email = models.EmailField()
    location = models.CharField(max_length=120)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    category = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    level = models.PositiveSmallIntegerField(default=80)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "category", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200)
    project_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    featured = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-featured", "title"]

    def __str__(self):
        return self.title


class Experience(models.Model):
    company = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    period = models.CharField(max_length=80)
    summary = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "company"]

    def __str__(self):
        return f"{self.role} @ {self.company}"
