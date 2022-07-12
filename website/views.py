from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import login_required, current_user
from .models import User, Pile, PileUpdate
import os

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    Stats = Pile.query.filter_by(user_id=current_user.id).first()
    if Stats:
        displayRatio = Stats.ratio
    else: displayRatio = "0 because you need to Create a Pile!"


    if request.method == 'POST':
        ingredient = int(request.form.get('ingredient'))
        volumeAdd = request.form.get('volume')
        if len(volumeAdd) <= 0:
            flash('Volume cannot be zero', category='error')
        else:
            eventCreate = PileUpdate(ratio=ingredient, volume=volumeAdd, user_id=current_user.id)
            db.session.add(eventCreate)
            db.session.commit()
            currentPile = Pile.query.filter_by(user_id= current_user.id).first()
            #print(currentPile)
            volume = currentPile.volume
            volumeUpdate = volume + int(volumeAdd)
            carbonAdd = int(ingredient)*int(volumeAdd)
            ratio = currentPile.ratio
            carbonTotal = ratio*volume
            carbonTotal += carbonAdd
            ratioNew = carbonTotal/volumeUpdate
            currentPile.volume = volumeUpdate
            currentPile.ratio = ratioNew
            db.session.commit()
            flash('You added to your pile!', category='success')
            return redirect(url_for('views.home'))
    return render_template("home.html", user=current_user, ratio= displayRatio)
