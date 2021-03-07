import os
from flask import Flask, render_template, request, flash, redirect, session, g
from models import connect_db, db, User, Party, PartyMember, Resturaunt, Vote
from forms import UserForm, LoginForm, AddMemberForm, PartyForm, VoteForm, BooleanField, VoteAgainForm
import requests

CURR_USER_KEY = "curr_user"


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///speed_eats'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]




"""Basic Routes"""

@app.route('/')
def show_home():
    res = []
    print(res)
    
    if g.user:
        return render_template('/home/home.html')
    return render_template('/home/home-anon.html')

@app.route('/404')
def give_404():
    return render_template('404.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()

    if g.user:
        flash('You are already signed in.', category='warning')
        return 

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            form.email.errors.append("email must be unique")
            flash("That email is already taken", category='warning')
            return render_template('/users/signup.html', form=form)
        try:
            u = User.create(
                email=form.email.data,
                password=form.password.data,
                name=form.name.data)
        except:
            return redirect('/404')
        if type(u) == str:
            flash(u, category='warning')
            return render_template('/users/signup.html', form=form)
        do_login(u)
        flash('Success! Account created!', category='success')
        flash('You have been automatically logged in', category='info')
        return redirect('/')
    return render_template('/users/signup.html', form=form)

@app.route('/logout')
def log_out_user():
    if g.user:
        do_logout()
        flash('Come back soon!', category='success')
    else:
        flash("You weren't logged in.", category='info')
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def log_in_user():
    form = LoginForm()
    if g.user:
        flash('You are already logged in', category='info')
        return redirect('/')
    if form.validate_on_submit():
        try:
            u = User.authenticate(email=form.email.data, password=form.password.data)
        except:
            return render_template('404.html')
        if u:
            do_login(u)
            flash('Successfully Logged in!', category='success')
            return redirect('/')
        else:
            flash('Invalid Credentials', category='danger')

    return render_template('/users/login.html', form=form)

"""Party Routes"""

@app.route('/parties/add_member', methods=['GET', 'POST'])
def add_member():
    if not g.user:
        flash('You must log in for that', category='danger')
        return redirect('/login')
    form = AddMemberForm()

    if form.validate_on_submit():
        p = Party.query.filter_by(id=form.party_id.data).first()
        if not p:
            flash("We're sorry, that Party Id is invalid", category='danger')
            return render_template('/parties/add-member.html')
        if g.user in p.members:
            flash("You are already a member of that party", category="info")
            return render_template('/')
        new_member = p.add_member(g.user.id)
        if new_member:
            flash("You have been successfully added to the party", category='success')
    return render_template('/parties/add-member.html', form=form)

@app.route('/parties/create', methods=['POST', 'GET'])
def create_party():
    if not g.user:
        flash('You must log in for that', category='danger')
        return redirect('/login')
    form = PartyForm()
    if form.validate_on_submit():
        p = Party.create(
            name=form.name.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            leader_id=g.user.id
        )
        if type(p) == str:
            flash(p, category='info')
        else:
            flash('Successfully added party', category='success')
            resturaunts = Resturaunt.get_resturaunts(party_id=p.id)
            if type(resturaunts) == str:
                flash(resturaunts, category='warning')
            return redirect('/')
    return render_template('/parties/create.html', form=form)

@app.route('/parties/delete/<int:party_id>', methods=['POST'])
def delete_party(party_id):
    party = Party.query.filter_by(id=party_id).first()
    if not party:
        flash("Couldn't find that party!", category='warning')
        return redirect('/404')

    if not g.user or g.user != party.leader:
        flash('You must be logged in as the party leader to do that!', category='danger')
        return redirect('/')
    db.session.delete(party)
    try:
        db.session.commit()
    except:
        flash('Error interfacing with databases', category='danger')
        return redirect('/404')
    flash('Party was successfully deleted', category='success')
    return redirect('/')



@app.route('/parties/<int:party_id>')
def show_party(party_id):
    party = Party.query.filter_by(id=party_id).first()
    if not party:
        flash("Sorry, we can't find that party", category='warning')
        return redirect('/')
    if party.done_voting():
        return redirect(f'/done_voting/{party_id}')
    return render_template('/parties/view.html', party=party)


@app.route('/parties/<int:party_id>/accept_members', methods=['POST'])
def open_voting(party_id):
    party = Party.query.filter_by(id=party_id).first()
    if not party:
        return redirect('/404')
    if not g.user or g.user != party.leader:
        flash('You must be logged in as the party leader to do that!', category='danger')
        return redirect(f'/parties/{party_id}')
    if not party.accepting_members:
        votes = Vote.query.filter_by(party_id=party.id).all()
        for vote in votes:
            db.session.delete(vote)
        resturaunts = Resturaunt.query.filter_by(party_id=party.id)
        for resturaunt in resturaunts:
            db.session.delete(resturaunt)
    party.accepting_members = False if party.accepting_members else True
    db.session.add(party)
    db.session.commit()
    if party.accepting_members:
        flash("Accepting new Members!", category="success")
    else:
        flash("Members locked in!", category="warning")
    return redirect(f'/parties/{party_id}')
        

"""Voting Routes"""


@app.route('/vote/<int:party_id>', methods=['GET'])
def vote_form(party_id):
    if not g.user:
        flash('You must be logged in for that!', category='info')
        return redirect('/login')
    party = Party.query.filter_by(id=party_id).first()
    if not party:
        flash("We can't find that party", category='danger')
        return redirect('/404')
    if g.user not in party.members:
        flash('You are not a memeber of this party', category='warning')
        return redirect('/')
    resturaunts = Resturaunt.query.filter_by(party_id=party.id, voted_out=False).all()
    yet_to_be_voted = []
    for resturaunt in resturaunts:
        if not Vote.query.filter_by(member_id=g.user.id, resturaunt_id=resturaunt.id).first():
            yet_to_be_voted.append(resturaunt)
    if len(yet_to_be_voted) != 0:

        form = VoteForm()
        resturaunt=yet_to_be_voted[0]
        return render_template('/parties/vote.html', form=form, resturaunt=resturaunt)
    else:
        flash("""You're done voting for now, refresh this page
                        to see when the resturaunt is chosen""", category='success')
        return redirect(f'/parties/{party_id}')

@app.route('/vote/<int:party_id>/<int:resturaunt_id>', methods=['POST'])
def handle_vote(party_id, resturaunt_id):
    form = VoteForm()
    if form.validate_on_submit():
        yay_or_nay = form.yay_or_nay.data
        vote = Vote.vote(member=g.user,
                    party_id=party_id,
                    resturaunt_id=resturaunt_id,
                    yay=yay_or_nay)
        if vote:
            if vote.party.done_voting():
                return redirect(f'/done_voting/{party_id}')
            return redirect(f'/vote/{party_id}')
        else:
            flash("""You're done voting for now, refresh this page
                         to see when the resturaunt is chosen""", category='success')
            return redirect(f'/parties/{party_id}')
    return redirect(f'/vote/{party_id}')
    


@app.route('/done_voting/<int:party_id>', methods=['GET'])
def finished_voting(party_id):
    if not g.user:
        return redirect(f"/parties/{party_id}")
    p = Party.query.filter_by(id=party_id).first()
    if not p or not p.done_voting():
        flash("Not quite!", category='info')
        return redirect('/')
    leader_data = Vote.get_winners(party_id=p.id)
    
    resturaunts = Resturaunt.query.filter_by(party_id=party_id, voted_out=True).all()
    return render_template('done_voting.html', leaders=leader_data, resturaunts=resturaunts, party=p)



    
   
            
        





"""Stop flask from caching anything"""
@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req