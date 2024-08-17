from flask import Blueprint,render_template,redirect,url_for,request,flash
from .models import User,ResearchTopic,Papers,Note
from werkzeug.security import generate_password_hash,check_password_hash
from .models import db
from flask_login import login_user,logout_user,login_required,current_user

#define the file as blue print
auth = Blueprint('auth',__name__)


@auth.route('/login',methods= ['POST','GET'])
def login():
    if request.method =='POST':
        email= request.form.get('email')
        password = request.form.get('password')

        #getting email and password from database to check validity
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in Successfully!', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.landing'))
            else:
                flash('Incorrect Password, Retry !', category='error')
        else:
            flash('Email does not exist!',category='error')

    return render_template('login.html',user= current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/signup',methods=['POST','GET'])
def signup():
    #getting user information from the signup form
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email exists already.', category='error')
        elif len (email) < 10:
            flash('Email length must be greater than 10 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 2 characters', category='error')
        elif len(password1) < 7:
             flash('Password must be at least 7 character.',category='error')
        elif password1 != password2:
             flash('Passwords do not match.',category='error')
        else:
            # add user to database
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
            new_user = User(email=email,first_name=first_name,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account successfully created.',category='success')
            return redirect(url_for('views.landing'))
        
    return render_template('signup.html',user=current_user)




@auth.route('/create',methods =['POST','GET'])
@login_required
def create_research():

    #getting research information from the form
    if request.method == 'POST':
        title = request.form.get('title')
        research_type = request.form.get('researchType')
        organization = request.form.get('owner')
        description =request.form.get('description')


        #check if topic has already been created
        topic = ResearchTopic.query.filter_by(title=title).first()
        if topic :
            flash('Research Topic  already exists.', category='error')
        elif len(title) < 4 :
            flash('Research Title should be more than 4 characters.', category='error')
        elif len(description) < 5:
            flash('Research description should be more than 5 characters.',category='error')
        else:
            new_research = ResearchTopic(title=title,
                                         research_type=research_type,
                                         organization=organization,
                                         description=description,
                                         user_id=current_user.id)
            db.session.add(new_research)
            db.session.commit()
            flash('Research topic has successfully been created.', category='success')

            return redirect(url_for('views.landing'))
    return render_template('/create.html',user=current_user)



@auth.route('/add_paper/<int:topic_id>', methods=['POST', 'GET'])
@login_required
def add_paper(topic_id):
    if request.method == 'POST':
        title = request.form.get('title')
        doi = request.form.get('doi')
        ISBN = request.form.get('ISBN')
        author = request.form.get('author')
        abstract = request.form.get('abstract')

        paper = Papers.query.filter_by(title=title).first()
        if paper:
            flash('Book title already exists.', category='error')
        elif len(title) < 4:
            flash('Book Title should be more than 4 characters.', category='error')
        elif len(author) < 10:
            flash('Name of author should be more than 10 characters.', category='error')
        elif len(ISBN) < 4:
            flash('Paper ISBN should be more than 4 characters.', category='error')
        else:
            new_paper = Papers(
                title=title,
                doi=doi,
                ISBN=ISBN,
                author=author,
                abstract=abstract,
                topic_id=topic_id,
                user_id=current_user.id
            )
            db.session.add(new_paper)
            db.session.commit()
            flash('Research paper has successfully been added.', category='success')
            return redirect(url_for('views.view_topic',topic_id=topic_id))  # Redirect to a page after adding a paper

    return render_template('add_paper.html', user=current_user)

@auth.route('/add_note/<int:paper_id>', methods=['POST', 'GET'])
@login_required
def add_note(paper_id):
    if request.method == 'POST':
        note_data = request.form.get('note')
        if len(note_data) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note_data, user_id=current_user.id, paper_id=paper_id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            return redirect(url_for('views.view_paper', paper_id=paper_id))
    
    return render_template("note_form.html", paper_id=paper_id, edit_mode=False)

@auth.route('/edit_note/<int:note_id>', methods=['POST', 'GET'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        note_data = request.form.get('note')
        if len(note_data) < 1:
            flash('Note is too short!', category='error')
        else:
            note.data = note_data
            db.session.commit()
            flash('Note updated!', category='success')
            return redirect(url_for('views.view_paper', paper_id=note.paper_id))
    
    return render_template("note_form.html", note=note, edit_mode=True)
