from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post
from app.posts import bp
from app.posts.forms import PostForm


@bp.route("/", methods=["GET"])
def list_posts():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=5, error_out=False
    )
    posts = pagination.items
    return render_template("posts/post_list.html", posts=posts, pagination=pagination)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            published=form.published.data,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("posts.list_posts"))
    return render_template("posts/post_form.html", form=form, title="New Post")


@bp.route("/<int:post_id>", methods=["GET"])
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/post_detail.html", post=post)


@bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.published = form.published.data
        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("posts.detail", post_id=post.id))
    return render_template("posts/post_form.html", form=form, title="Edit Post")


@bp.route("/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("posts.list_posts"))