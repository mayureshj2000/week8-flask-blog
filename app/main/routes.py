from flask import render_template, request, url_for, redirect, flash, current_app, abort, Response
from flask_login import current_user, login_required
from app.main import bp
from app import db
from app.models import Post
from app.main.forms import SearchForm, PostForm, CommentForm, ContactForm
from app.models import Post, Comment
from werkzeug.utils import secure_filename
import os

@bp.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    page = request.args.get("page", 1, type=int)
    query = Post.query.order_by(Post.timestamp.desc())

    term = None
    if form.validate_on_submit():
        term = form.q.data
        return redirect(url_for("main.index", q=term, page=1))

    if request.method == "GET":
        term = request.args.get("q", "")

    if term:
        form.q.data = term
        query = query.filter(Post.title.ilike(f"%{term}%"))

    pagination = query.paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    total_posts = Post.query.count()
    total_comments = 0
    categories_count = 0
    popular_post_title = "N/A"

    active_users = []

    return render_template(
        "main/index.html",
        form=form,
        posts=posts,
        pagination=pagination,
        total_posts=total_posts,
        total_comments=total_comments,
        categories_count=categories_count,
        popular_post_title=popular_post_title,
        active_users=active_users,
    )


@bp.route("/profile")
@login_required
def profile():
    user_posts = current_user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("main/profile.html", user=current_user, posts=user_posts)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
        )
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            path = os.path.join(upload_folder, filename)
            form.image.data.save(path)
            post.image_filename = filename

        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("main/new_post.html", form=form)

@bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            body=form.body.data,
            post=post,
            author=current_user,  # assuming User has comments relationship
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("main.post_detail", post_id=post.id))
    comments = post.comments.filter_by(approved=True).order_by(Comment.timestamp.desc()).all()
    return render_template("main/post_detail.html", post=post, form=form, comments=comments)

@bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for("main.post_detail", post_id=post.id))
    return render_template("main/edit_post.html", form=form, post=post)


@bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("main.index"))

@bp.route("/feed")
def feed():
    posts = Post.query.order_by(Post.timestamp.desc()).limit(20).all()
    xml = render_template("feed.xml", posts=posts)
    return Response(xml, mimetype="application/rss+xml")

@bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # For assignment, just flash or store in DB; real app would send email
        flash("Thank you for your message!", "success")
        return redirect(url_for("main.contact"))
    return render_template("main/contact.html", form=form)
