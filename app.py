import os
from flask import Flask, render_template, abort
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.portfolio

    projects_list = [e for e in app.db.projects.find({})]
    project_nav_index = {project['navtitle']: project for project in projects_list}

    @app.route("/")
    def home():
        kwargs = {
            "title": "Portfolio",
            "active": "home"
        }
        return render_template("home.html", **kwargs)

    @app.route("/about")
    def about():
        about_raw = [e for e in app.db.details.find({})][0]["about"]
        about_split = about_raw.split("|")
        kwargs = {
            "title": "About Me",
            "active": "about",
            "about": about_split
        }

        return render_template("about.html", **kwargs)

    @app.route("/contact")
    def contact():
        details = [e for e in app.db.details.find({})][0]
        kwargs = {
            "title": "Contact",
            "active": "contact",
            "email": details["email"],
            "linkedin": details["linkedin"]
        }

        return render_template("contact.html", **kwargs)
    
    @app.route("/projects")
    def projects():

        kwargs = {
            "title": "Projects",
            "active": "projects",
            "projects": projects_list
        }
        return render_template("projects.html", **kwargs)
    
    @app.route("/projects/<string:project_name>")
    def project(project_name: str):
        if project_name not in project_nav_index:
            abort(404)

        kwargs = {
            "project": project_nav_index[project_name],
            "title": project_nav_index[project_name]['title'],
            "active": "projects"
        }
        return render_template("project.html", **kwargs)
    
    return app
