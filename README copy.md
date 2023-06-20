# backend

Backend - Django Project
Introduction
This repository contains the source code for the backend of the Rqm project, built using the Django framework. The backend provides the APIs that are used by the frontend to access the data and perform various operations.

Getting Started
The following instructions will help you set up the backend of the Rqm project on your local machine for development and testing purposes.

Prerequisites
Python 3.6 or higher
Django 3.0 or higher
Virtualenv (recommended)
pip
Installing
Clone this repository to your local machine:

$ git clone <https://github.com/><username>/rqm-backend.git
Navigate into the cloned repository:

$ cd rqm-backend
Create a virtual environment:

$ virtualenv env
Activate the virtual environment:

$ source env/bin/activate
Install the required packages:

$ pip install -r requirements.txt
Apply the migrations:

$ python manage.py migrate
Start the development server:

$ python manage.py runserver
Commit Naming Rules
We follow a standard naming convention for commits to ensure consistency and ease of understanding. The commit messages should be in the following format:

[<type>] <subject>

<body>
where:

<type>: Indicates the type of change made. It should be one of the following:
feat: A new feature.
fix: A bug fix.
docs: Documentation changes.
style: Changes that do not affect the meaning of the code (whitespace, formatting, missing semi-colons, etc.).
refactor: A code change that neither fixes a bug nor adds a feature.
perf: A code change that improves performance.
test: Adding missing tests.
chore: Changes to the build process or auxiliary tools and libraries such as documentation generation.
<subject>: A short description of the change. The subject should not be more than 50 characters and should start with a capital letter.

<body>: A longer description of the change, if necessary.
Branching Rules
We use a branching model similar to Git Flow. The following branches are used in the project:

master: The main branch that contains the latest stable release.
develop: The branch where the development happens. All feature branches are merged into this branch.
feature/<feature_name>: A branch for a new feature. When the feature is ready, it is merged into the develop branch.
