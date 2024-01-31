from flask import Flask, render_template,redirect,url_for,session
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .Utils.database import db
import json

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
 return render_template("home.html", user=current_user)

@routes.route('/about')
def about():
 return render_template("about.html", user=current_user)

@routes.route('/author')
def author():
 return render_template("author.html", user=current_user)

@routes.route('/recommended')
def recommended():
 return render_template("recomended.html", user=current_user)

@routes.route('/myorders')
@login_required
def myorders():
 return render_template("myorders.html", user=current_user)


@routes.route('/404')

def fourhundredfour():
 return render_template("404.html", user=current_user)



@routes.route('/cards')
@login_required
def cards():
 return render_template("/simplePages/cards.html", user=current_user)

@routes.route('/forgotpassword')
def forgotpassword():
 return render_template("forgotpassword.html", user=current_user)





    
