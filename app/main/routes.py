from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_required
from app.main import bp
from app import db
from app.models import Post
from app.main.forms import SearchForm, PostForm
from flask import abort
from app.models import Post

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
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("main/new_post.html", form=form)

@bp.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("main/post_detail.html", post=post)