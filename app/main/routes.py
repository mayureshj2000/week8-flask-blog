from flask import render_template, request, url_for, redirect
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

    # Support both POSTed search and ?q= search so refresh keeps the term
    term = None
    if form.validate_on_submit():
        term = form.q.data
        # redirect to GET with query param to avoid form resubmit on refresh
        return redirect(url_for("main.index", q=term, page=1))

    # If coming from a GET with ?q=, use that
    if request.method == "GET":
        term = request.args.get("q", "")

    if term:
        form.q.data = term
        query = query.filter(Post.title.ilike(f"%{term}%"))

    pagination = query.paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items

    # Simple example stats (adjust once you have real data)
    total_posts = Post.query.count()
    total_comments = 0          # placeholder until you have a Comment model
    categories_count = 0        # placeholder if you add categories
    popular_post_title = "N/A"  # placeholder

    # active_users can later be a list of objects with username and post_count
    active_users = None

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