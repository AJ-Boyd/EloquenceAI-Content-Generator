"""
auth: AJ Boyd
date: 6/29/2024
file: routes.py
desc: handles the form requests for the generator
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from .generate_content import *
import os

routes = Blueprint("routes", __name__)
llm = config_LLM()

@routes.route('/', methods=['POST', 'GET'])
def home():
    final_content = session.get("final_content", "")
    return render_template("index.html", content=final_content)

@routes.route('/generate', methods=["POST"])
def submit():
    attributes = []
    # print("form:", request.form)
    # print("subject prompt:", request.form.get("subject"))
    for d in request.form:
        x = request.form[d]
        if request.form[d] == "--":
            x = None
        attributes.append(x)
    
    file = request.files.get("example")  # File field
    # Handle file upload
    if file and file.filename != '':
        # Save the file to the upload folder
        filename = os.path.join('uploads', file.filename)
        file.save(filename)

    try:
        # Read the content of the file
        with open(filename, 'r') as f:
            file_content = f.read()
            # data['file'] = file_content  # Update the 'file' field with content
            print("file content:", file_content)
            attributes.append(file_content)
    except:
        file_content = None
        attributes.append(file_content)
        
    if file and file.filename != '':
        os.remove(filename)


    print("attributes:", attributes)
    content = gen_content(llm, attributes)
    session["final_content"] = content
    return redirect(url_for('routes.home'))