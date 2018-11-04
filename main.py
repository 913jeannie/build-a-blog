from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'sjddfhk'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        
@app.route("/")
def index():
   #/blog is the main page or index
    return redirect("/blog")

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    id = request.query_string
    if request.method == 'GET':
        if not id:
            return render_template('blog.html', blogs=blogs)
        else:
            b = int(request.args.get('b'))
            blog = Blog.query.get(b)
            return render_template('singlepost.html', blog=blog)

@app.route('/newpost', methods = ['GET'])
def newpost():
    return render_template('newpost.html')

@app.route('/newpost', methods=['POST'])
def add_post():
    title = request.form['title']
    body = request.form['body']

    if not title and not body:
        return render_template('newpost.html', title_error='Title cannot be blank', body_error='Enter a blog')

    elif not title:
        return render_template('newpost.html', title_error='Title cannot be blank', body=body)
    
    elif not body:
        return render_template('newpost.html', title=title, body_error='Enter a blog')
        
    else:
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/blog')

    #return render_template('newpost.html')
if __name__ == '__main__':
    app.run() 