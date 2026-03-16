from flask import redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Comment, Post
from app.comments import bp
from app.comments.forms import CommentForm


@bp.route("/add/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user,
            post=post,
            approved=True,  # basic flow; could add moderation later
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment added.", "success")
    else:
        flash("Failed to add comment.", "danger")
    return redirect(url_for("posts.detail", post_id=post.id))
