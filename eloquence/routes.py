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
# content = ""

@routes.route('/', methods=['POST', 'GET'])
def home():
    return render_template("index.html")

@routes.route('/generate', methods=["POST"])
def submit():
    global content
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
    try:
        content = gen_content(llm, attributes)
        return jsonify({"status": 200, "content": content})
    except Exception as e:
        print(f"Error generating content: {e}")
        return jsonify({"status": 400, "content": "Error 400"})
    
@routes.route('/augment', methods=["POST"])
def augment():
    global content
    changes = []
    print("req:", request.form)
    for c in request.form:
        x = request.form[c]
        if x == "--" or x == "":
            x = None
        changes.append(x)   
    
    if any(element is not None for element in changes):
        augmented_content = aug_content(changes)
        content = augmented_content
        print("new content:", content)
        print("changes:", changes) 
        return jsonify({"status": 200, "content": augmented_content})
    else:
        print("no changes to be made")
        return jsonify({"status": 400, "error": "You must have at least one revision to make in order to re-generate content."})
    
        