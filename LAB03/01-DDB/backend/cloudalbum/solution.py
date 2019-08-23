from flask import app
from werkzeug.security import generate_password_hash
from cloudalbum.database.model_ddb import User


def solution_put_new_user(new_user_id, user_data):
    app.logger.info("RUNNING TODO#1 SOLUTION CODE:")
    app.logger.info("Put new signup user information!")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")

    user = User(new_user_id)
    user.email = user_data['email']
    user.password = generate_password_hash(user_data['password'])
    user.username = user_data['username']
    user.photos = []
    user.save()


def solution_get_user_data_with_idx(signin_data):
    app.logger.info("RUNNING TODO#2 SOLUTION CODE:")
    app.logger.info("Get user data with email which is Global Secondary Index")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")

    db_user = None
    for item in User.email_index.query(signin_data['email']):
        if item is not None:
            db_user = item
    return db_user

def solution_put_photo_info_ddb(user_id, new_photo):
    app.logger.info("RUNNING TODO#3 SOLUTION CODE:")
    app.logger.info("Update Photo informtation into User table!")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")

    try:
        User(id=user_id).update(
            actions=[
                User.photos.set((User.photos | []).append([new_photo]))
            ]
        )
    except Exception as e:
        app.logger.error(e)
        print(e.__cause__)
        raise e


def solution_delete_photo_from_ddb(user, photos, photo):
    app.logger.info("RUNNING TODO#4 SOLUTION CODE:")
    app.logger.info("Delete a photo from photos list, and update!")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")
    photos.remove(photo)
    User(id=user['user_id']).update(
        actions=[
            User.photos.set(photos)
        ]
    )
