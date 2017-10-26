from flask import Flask, request, redirect, render_template, flash, session
from models import User, Blog
from app import db, app


@app.before_request
def require_login():
    allowed_routes = ['index', 'display_blogs', 'login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect ('/')

 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("logged in")
            return redirect ('/addpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html')
 
 
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if not is_email(email):
            flash(email + '" does not seem like an email address')
            return redirect('/signup')
        email_db_count = User.query.filter_by(email=email).count()
        if email_db_count > 0:
            flash(email + '" is already taken please click login.')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect('/newpost')
        
            #return '<h1>You already have an account.  Please <a href="/login">login.</a></h1>'
    
    else:
        
        return render_template('signup.html')

def is_email(string):
    # for our purposes, an email string has an '@' followed by a '.'
    # there is an embedded language called 'regular expression' that would crunch this implementation down
    # to a one-liner, but we'll keep it simple:
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present
        
        
            
        
#@app.route('/logout')
#def logout():
#    del session['email']
#    flash('Logged out')
#    return redirect('/blog')                
 


@app.route('/logout')
def logout():
    if 'email' in session:
        del session['email']
        return redirect('/')   
    elif 'email' not in session:
        return redirect('/')


@app.route('/blog', methods=['POST', 'GET'])
def display_blogs():

    if request.args.get("user"):
        user_id = request.args.get('user')
        user = User.query.get(user_id)
        blogs = Blog.query.filter_by(writer=user).all()
        return render_template('singleuser.html', blogs=blogs)

    elif  request.args.get('id'):
        blog_id = (request.args.get('id'))
        blog = Blog.query.get(blog_id)
        user_id = (request.args.get('id'))
        user = User.query.filter_by(id=user_id)
        return render_template('post.html', title="blogz", blog=blog, user=user)       
    
    else: 
        blogs = Blog.query.all()
        writer_id = (request.args.get('writer_id'))
        user = User.query.filter_by(id=writer_id)
        return render_template('blog.html', title="blogz", blogs=blogs, user=user)


@app.route('/')
def index():     
    users = User.query.all()
    return render_template('index.html', users=users)

    
@app.route("/addpost", methods=['POST', 'GET'])
def add_post():
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body'] 
        

    return render_template('addpost.html')
  

@app.route("/newpost", methods=['POST', 'GET'])
def new_post():
    title_error =""
    body_error = ""
    if request.method == "POST":
        title =request.form['title']
        body = request.form['body']
        writer = User.query.filter_by(email=session['email']).first()
        if (title == ""):
            title_error = "Please enter title"
            return render_template("addpost.html", title_error=title_error)
        if (body == ""):
            body_error = "Please enter body"
            return render_template("addpost.html", body_error=body_error)
        
        else:
            
            new_blog = Blog(title, body, writer)
        
            #new_body = Blog(body)
            db.session.add(new_blog)
            db.session.commit()  
            return render_template('newpost.html', title=title, body=body)
    
    return render_template('addpost.html')



    

if __name__ == '__main__':
    app.run()