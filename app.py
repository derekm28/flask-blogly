"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/', methods = ['GET'])
def user_list():
    """redirects to user list"""
    """shows list of users"""
    """has button for add user"""

    users = User.query.all()
    return render_template('user_list.html', users = users)

@app.route('/users', methods = ['GET'])
def user_list2():
    """shows list of users"""
    """has button for add user"""

    users = User.query.all()
    return render_template('user_list.html', users = users)


@app.route('/users/new', methods = ['GET'])
def input_form():
    """displays input form"""

    users = User.query.all()
    return render_template('input_form.html', users = users)

@app.route('/users/new', methods = ['POST'])
def add_user():
    """Add user and redirect to list."""

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None) #delete the other ) when you uncomment this line out

    #user = User(first_name = first_Name, last_name = fast_Name, image_url = image_Url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route("/<int:user_id>", methods = ['GET'])
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user = user)

@app.route('/users/<int:user_id>/edit', methods = ['GET'])
def edit_user(user_id):
    """Shows edit page"""
    """make edits to user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_form.html', user = user)


@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def post_edit(user_id):
    """post edits to user"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


    ###############################################


@app.route('/users/<int:user_id>/posts/new', methods = ['GET'])
def post_form(user_id):
    """displays post form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post_form.html', user = user, tags = tags)



@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def sumbmit_post_form(user_id):
    """submits post form"""


    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title = request.form['title'], content = request.form['content'], user = user, tags = tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added")

    return redirect(f"/{user_id}")


@app.route('/posts/<int:post_id>', methods = ['GET'])
def show_post(post_id):
    """shows actual post and has edit, delete options"""

    post = Post.query.get_or_404(post_id)
    return render_template("show_post.html", post = post)


@app.route('/posts/<int:post_id>/edit', methods = ['GET'])
def edit_post(post_id):
    """shows edit post form and has cancel option, redirects to post page"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post = post, tags = tags)


@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
def post_edited_post(post_id):
    """displays updated post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post ' {post.title}' edited.")

    return redirect(f"/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    """deletes existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post ' {post.title}' deleted.")

    return redirect(f"/{post.user_id}")



################################################




@app.route('/tags', methods = ['GET'])
def list_tags():
    """list all tags with link to tag detail page"""

    tags = Tag.query.all()
    return render_template('tag_list.html', tags = tags)



@app.route('/tags/new', methods = ['GET'])
def tag_form():
    """displays tag form"""

    posts = Post.query.all()
    return render_template('tag_form.html', posts = posts)


@app.route('/tags/new', methods = ['POST'])
def submit_tag_form():
    """handles submission for form"""

    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name = request.form['name'], posts = posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added")

    return redirect(f"/tags")


@app.route('/tags/<int:tag_id>', methods = ['GET'])
def tag_details(tag_id):
    """shows tag details(posts with that tag), has links to edit form and delete"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_details.html", tag = tag)


@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):
    """shows edit form for a tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag = tag, posts = posts)

@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def submit_edited_tag_form(tag_id):
    """handles submission for edit form"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.post = Post.query.filter(Post.id.in_(post_ids)).all()


    db.session.add(tag)
    db.session.commit()
    flash(f"Tag ' {tag.name}' edited.")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):
    """deletes a tag"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag ' {tag.name}' deleted.")

    return redirect("/tags")
