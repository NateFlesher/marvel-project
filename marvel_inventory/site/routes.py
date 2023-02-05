from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from marvel_inventory.forms import HeroForm
from marvel_inventory.models import Hero, db
from marvel_inventory.helpers import APIMarvel


site = Blueprint('site', __name__, template_folder='site_templates')

"""
Note in the above code, some arguments are specified when creating the
Blueprint object. The first argument, 'site', is the Blueprint's name, this is used by
Flask's routing mechanism. The second argument, __name__, is the Blueprint's import name,
Which Flask uses to locate the Blueprint's resources

"""

@site.route('/')
def home():
    return render_template('index.html')


@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_hero = HeroForm()
    try:
        if request.method == 'POST' and my_hero.validate_on_submit():
            x = APIMarvel(my_hero.name.data)
            for i in x:
                name = i["name"]
                description = i["description"]
                comics = i["id"]
                img_head = i["thumbnail"]["path"] + "." +  i["thumbnail"]["extension"]
                user_token = current_user.token

                hero = Hero(name, description, comics, img_head, user_token)

                db.session.add(hero)
                db.session.commit()

            return redirect(url_for('site.profile'))
    
    except:
        raise Exception('Hero not created, please check your form and try again!')

    user_token = current_user.token

    heroes = Hero.query.filter_by(user_token = user_token)
    
    return render_template('profile.html', form = my_hero, heroes = heroes)

    