#IMPORTS
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from flask import url_for, flash, render_template, redirect, request
from package import app
from package.forms import DegreeForm
from io import BytesIO

import secrets
import os
import sys
import requests
import random
import json

#GLOBAL VARS
direction = ""
json_file_url = os.path.join(app.root_path, 'static', 'json', 'pxSizes.json')
print("ROOT_PATH: %s " % (app.root_path),  file = sys.stderr)
json_file = open(json_file_url, 'r')
json_file_data = json.load(json_file)
x1 = 0
x2 = 0
#

@app.route('/home', methods=['GET', 'POST'])
def home():
    form = DegreeForm()
    #LOGIC FOR ACCEPTING POST REQUESTS
    if request.method == 'POST':
        if request.form['navbutton'] == 'Home':
            return redirect(url_for('home'))
        elif request.form['navbutton'] == 'Research':
            return render_template('research.html', title=' Research Section ')
        elif request.form['navbutton'] == 'About':
            return render_template('about.html', title=' About Section')
        elif request.form['navbutton'] == 'Degree':
            return render_template('degree.html', form=form)
    else:
        return render_template('home.html', title='Home')

#REDIRECTING ROUTS
@app.route('/', methods=['GET', 'POST'])
def blank():
    return redirect(url_for('home'))

#Degree form
@app.route('/degree', methods=['GET', 'POST'])
def degree():
    form = DegreeForm()
    return render_template('degree.html', form=form)


#EDITING DEGREE PICTURE PHOTO FUNC
def edit_text(url, text1, text2, x1, x2, y1, y2):

    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + '.png'
    picture_path = os.path.join(app.root_path,'static', 'degree_photos',
                                picture_fn)
    font_url = os.path.join(app.root_path, 'fonts', 'DejaVuSans.ttf')
    font = ImageFont.truetype(font_url, 50)
    i = Image.open(url)
    draw = ImageDraw.Draw(i)
    draw.text((x1/2, y1/2), text1, font=font, fill="black")
    draw.text((x2/2, y2/2), text2, font = font, fill = "black")

    i.save(picture_path)
    return picture_fn

#FUNCTION FOR DOMAIN POSITION
def get_dom_pos(dom):
    
    global json_file_data
    global x1
    for position in json_file_data['px_size']:
        x1 = position[str(len(dom))]
    return x1

#FUNCTION FOR NAME POSITION
def get_name_pos(name):

    global json_file_data
    global x2
    for position in json_file_data['px_size']:
        x2 = position[str(len(name))]
    return x2


#FUNCTION FOR EDITING AND ACCEPTING POST REQUESTS FOR DEGREE
@app.route('/photo', methods=['POST'])
def photo():
    form = DegreeForm()
    global x1 
    global x2
    if request.method == 'POST':
        name=form.name.data
        dom =form.domain.data
        dom_pos = get_dom_pos(dom)
        name_pos = get_name_pos(name)
        url= os.path.join(app.root_path, 'static', 'site_photos', 'P.H.D.png')
        final_degree = edit_text(url, dom, name, dom_pos, name_pos, 1079, 445)
    post_degree = url_for('static', filename='degree_photos/'+final_degree)
    return render_template('photo.html', images=post_degree, domain=form.domain.data, 
                            name=form.name.data)
