"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect, session

import hackbright

app = Flask(__name__)

@app.route("/")
def homepage():
    """ shows list of students and projects"""
    students = hackbright.get_all_students()

    projects = hackbright.get_all_projects()

    return render_template("homepage.html", students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    projects = hackbright.get_grades_by_github(github)



    #return "{} is the GitHub account for {} {}".format(github, first, last)

    html = render_template("student_info.html", 
                            first=first, 
                            last=last,
                            github=github, projects=projects)
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/add-student")
def get_form_info():
    """ shows user template for adding new student"""

    return render_template("new_student.html")



@app.route("/add-student", methods=['POST'])
def add_new_student():
    """ add new student to student table in hackbright db"""

    last_name = request.form["lname"]
    first_name = request.form["fname"]
    github = request.form["github"]

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("made_student.html", first_name=first_name, github=github)

@app.route("/add-project")
def get_project_info():
    """ shows user template for adding new student"""

    return render_template("new_project.html")

@app.route("/add-project", methods=['POST'])
def add_new_project():
    """ add new project to projects table in hackbright db"""

    title = request.form["title"]
    description = request.form["description"]
    max_grade = request.form["max_grade"]

    hackbright.make_new_project(title, description, max_grade)

    return redirect("/")

@app.route("/project")
def view_project_info():

    title = request.args.get('title')
    
    project_info = hackbright.get_project_by_title(title)

    grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html", project_info=project_info, grades=grades)




# @app.route("/made-student")
# def view_new_student():
#     """ displays link to view new student info"""

#     return render_template("made_student.html")



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
