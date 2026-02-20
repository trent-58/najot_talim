from django.shortcuts import render

from .models import Experience, Profile, Project, Skill


DEFAULT_PROFILE = {
    "full_name": "Javohir To'rayev",
    "role": "Python Backend Developer",
    "tagline": "Analytical, creative, and people-focused. I turn ideas into practical software solutions.",
    "bio": (
        "Passionate about leadership, communication, and problem solving. "
        "I focus on building useful systems and helping teams grow through clear execution."
    ),
    "email": "trentjace58@gmail.com",
    "phone": "+998 77 728 39 38",
    "location": "Tashkent, Uzbekistan",
    "github_url": "#",
    "linkedin_url": "#",
    "resume_url": "#",
}

DEFAULT_SKILLS = [
    {"category": "Technical", "name": "Python Telegram Bot Development", "level": 90},
    {"category": "Productivity", "name": "Microsoft Office Suite", "level": 88},
    {"category": "Execution", "name": "Project Planning & Execution", "level": 86},
    {"category": "Execution", "name": "Time Management & Prioritization", "level": 85},
    {"category": "Thinking", "name": "Critical Thinking", "level": 87},
    {"category": "Mindset", "name": "Adaptability & Flexibility", "level": 89},
]

DEFAULT_PROJECTS = [
    {
        "title": "Telegram Bots for Company Workflows",
        "description": (
            "Built multiple Telegram bots for business tasks and continued on follow-up projects "
            "after strong initial delivery."
        ),
        "tech_stack": "Python, Telegram Bot API",
        "project_url": "#",
        "repo_url": "#",
        "featured": True,
    },
]

DEFAULT_EXPERIENCE = [
    {
        "company": "Kwork",
        "role": "Python Telegram Bot Developer (Freelancer)",
        "period": "November 2023 - Present",
        "summary": (
            "Developed Telegram bots for company use-cases. Continued to receive additional "
            "projects after demonstrating strong delivery quality."
        ),
    },
    {
        "company": "Agrobank (Turtkul, Karakalpakstan)",
        "role": "Front Office",
        "period": "2 months",
        "summary": "Supported front office operations and customer-facing workflows.",
    },
]

DEFAULT_EDUCATION = [
    {
        "institution": "Presidential School in Nukus",
        "details": "Focused on Physics, Computer Science, Maths, Statistics.",
        "period": "2019 - 2022",
    },
    {
        "institution": "New Uzbekistan University",
        "details": "Bachelor of Science in Industrial Management.",
        "period": "2022 - 2026",
    },
    {
        "institution": "Najot Ta'lim",
        "details": "Python Backend Development.",
        "period": "2025 - 2026",
    },
]

DEFAULT_LANGUAGES = [
    {"name": "Uzbek", "level": "Native"},
    {"name": "English", "level": "Fluent (reading, writing, listening, speaking)"},
]


def portfolio(request):
    profile = Profile.objects.first()
    skills = list(Skill.objects.all())
    projects = list(Project.objects.all())
    experiences = list(Experience.objects.all())

    context = {
        "profile": profile or DEFAULT_PROFILE,
        "skills": skills or DEFAULT_SKILLS,
        "projects": projects or DEFAULT_PROJECTS,
        "experiences": experiences or DEFAULT_EXPERIENCE,
        "education": DEFAULT_EDUCATION,
        "languages": DEFAULT_LANGUAGES,
        "project_count": len(projects) if projects else len(DEFAULT_PROJECTS),
    }
    return render(request, "me/portfolio.html", context)
