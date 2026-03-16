from flask import render_template, request
from flask_login import current_user, login_required
from app.main import bp
from app import db
from app.models import Post
from app.main.forms import SearchForm


@bp.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    page = request.args.get("page", 1, type=int)
    query = Post.query.order_by(Post.timestamp.desc())

    if form.validate_on_submit():
        term = form.q.data
        if term:
            query = query.filter(Post.title.ilike(f"%{term}%"))

    pagination = query.paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    return render_template(
        "main/index.html",
        form=form,
        posts=posts,
        pagination=pagination
    )


@bp.route("/profile")
@login_required
def profile():
    user_posts = current_user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("main/profile.html", user=current_user, posts=user_posts)