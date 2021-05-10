from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import os
from pathlib import Path
import json
import requests
import base64


views = Blueprint('views', __name__)
Linkslist = []
listOfResposnes = []
listOfBase64Images = []

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/imgur', methods=['GET', 'POST'])
def imgur():
    """def createAlbum():
        if request.method == "POST":
            urlCreateAlbum = "https://api.imgur.com/3/album"
            payload={
            'ids[]': 'x4ulVyk',
            'title': request.form.get("title"),
            'description': request.form.get("description"),
            }

            headers = {
            'Authorization': 'Client-ID 4bf17ac773aa532'
            }

            response = requests.request("POST", urlCreateAlbum, headers=headers, data=payload)
            u = json.loads(response.text)
            if(response.status_code == 200):
                flash(f"Stworzono album: {u['data']['id']}", category='success')
                print(response.text)"""
    def uploadImage():
        if request.method == "POST":
            if request.files:
                #getting filename form POST request
                image = request.files["image"]
                filename = image.filename
                print(filename)

                #searching for specific file in system
                for root, dirs, files in os.walk(r'C:\Users'): 
                    for name in files:
                        if name == filename:
                            destination = os.path.abspath(os.path.join(root, name))

                with open(destination, 'rb') as binary_file:
                    binary_file_data = binary_file.read()
                    base64_encoded_data = base64.b64encode(binary_file_data)
                    base64_message = base64_encoded_data.decode('utf-8')

                    listOfBase64Images.append(base64_message)

                urlUploadImage = "https://api.imgur.com/3/image"
                payload={
                    'image': base64_message
                }
                headers = {
                'Authorization': 'Client-ID 4bf17ac773aa532',
                "type": "base64"
                }
                response = requests.request("POST", urlUploadImage, headers=headers, data=payload)
                print(response.text)

                u = json.loads(response.text)
                linkToFileImgur = (u["data"]["link"])
                if(response.status_code == 200):
                    flash(f"przesłano plik: {filename}; {linkToFileImgur}", category='success')
                    Linkslist.append(linkToFileImgur)
                    listOfResposnes.append(response.json())  

    def getUploadedImages():
        pass
    
    uploadImage()          
    print(Linkslist)
    return render_template("imgur.html", user=current_user, listOfBase64Images = listOfBase64Images, Linkslist = Linkslist)

