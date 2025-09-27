from database import get_db
from database.models import Comment


def create_comment_db(text, uid, pid):
    with next(get_db()) as db:
        new_comment = Comment(text=text, uid=uid, pid=pid)
        db.add(new_comment)
        db.commit()
        return True


def get_all_or_exact_comments_db(comment_id=0):
    with next(get_db()) as db:

        if comment_id:
            comment = db.query(Comment).filter_by(id=comment_id).first()

            if comment:
                return comment
            return False
        return db.query(Comment).all()


def delete_comment_db(comment_id):
    with next(get_db()) as db:
        comment_to_delete = db.query(Comment).filter_by(id=comment_id).first()

        if comment_to_delete:
            db.delete(comment_to_delete)
            db.commit()

            return True
        return False


def update_comment_db(comment_id, new_text):
    with next(get_db()) as db:
        comment = db.query(Comment).filter_by(id=comment_id).first()

        if comment:
            comment.comment = new_text
            db.commit()

            return True
        return False
