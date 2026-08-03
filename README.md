<div align="center">

# Academe.io

**A school management API for organizing academic records, people, schedules, and events.**

[![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-A30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Neon](https://img.shields.io/badge/Neon-00E599?logo=postgresql&logoColor=black)](https://neon.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

[Overview](#overview) · [Features](#features) · [Getting started](#getting-started) · [Tech stack](#tech-stack)

</div>

## Overview

Academe.io is a school management API built with Django REST Framework. It provides a central backend for managing students, attendance, exams, classes, lessons, subjects, teachers, parents, and school events through structured REST endpoints.

The API uses PostgreSQL hosted on Neon for persistent data, Redis for caching and request throttling, and JWT authentication to protect restricted resources.

## Features

- Manage student, teacher, and parent records
- Record and retrieve student attendance
- Organize exams and related academic data
- Manage classes, lessons, and subjects
- Create and maintain school events
- Secure protected endpoints with JWT authentication
- Improve response performance through Redis caching
- Limit repeated API requests through throttling
- Run the application in a consistent Docker environment

## Managed resources

| Resource   | Responsibility                           |
| ---------- | ---------------------------------------- |
| Students   | Student profiles and academic records    |
| Attendance | Student attendance records               |
| Exams      | Examination information and results      |
| Classes    | Class organization and enrollment data   |
| Lessons    | Lesson schedules and learning activities |
| Subjects   | Academic subject information             |
| Teachers   | Teacher profiles and assignments         |
| Parents    | Parent or guardian records               |
| Events     | School activities and scheduled events   |

## Architecture

| Layer                 | Responsibility                                                  |
| --------------------- | --------------------------------------------------------------- |
| Django REST Framework | REST endpoints, serialization, validation, and request handling |
| Django                | Application structure, domain models, and business logic        |
| PostgreSQL and Neon   | Persistent cloud-hosted school data                             |
| Redis                 | Caching and API throttling                                      |
| JWT                   | Authentication for protected API resources                      |
| Docker                | Reproducible local and deployment environments                  |

## Getting started

### Prerequisites

- [Docker](https://www.docker.com/) with Docker Compose
- A [Neon](https://neon.com/) PostgreSQL database
- A Redis instance when it is not provided by Docker Compose

### Environment variables

Create a `.env` file for the application configuration:

```env
SECRET_KEY=replace_with_a_secure_secret
DEBUG=True
DATABASE_URL=your_neon_postgresql_connection_string
REDIS_URL=your_redis_connection_url
```

> [!NOTE]
> Use the exact variable names referenced by the Django settings if they differ from this example.

> [!IMPORTANT]
> Never commit `.env` or expose the Django secret key and database credentials. Use secure environment configuration in production.

### Run with Docker

Build and start the application services:

```bash
docker compose up --build
```

Apply the database migrations from the Django container:

```bash
docker compose exec web python manage.py migrate
```

Create an administrator account when required:

```bash
docker compose exec web python manage.py createsuperuser
```

> [!NOTE]
> The commands above assume the Django service is named `web`. Replace `web` with the service name defined in `compose.yaml` or `docker-compose.yml`.

## Tech stack

| Technology                                                      | Purpose                             |
| --------------------------------------------------------------- | ----------------------------------- |
| [Django](https://www.djangoproject.com/)                        | Backend framework and domain models |
| [Django REST Framework](https://www.django-rest-framework.org/) | REST API development                |
| [PostgreSQL](https://www.postgresql.org/)                       | Relational database                 |
| [Neon](https://neon.com/)                                       | Managed PostgreSQL hosting          |
| [Redis](https://redis.io/)                                      | Caching and API throttling          |
| [Docker](https://www.docker.com/)                               | Containerized runtime environment   |
| [JWT](https://jwt.io/)                                          | Protected API authentication        |

## Project goals

- Centralize essential school information in one API
- Keep academic and administrative data organized
- Secure access to protected school resources
- Improve API performance and resilience through caching and throttling
- Provide a maintainable backend for school management applications
