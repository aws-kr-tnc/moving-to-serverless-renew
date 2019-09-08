from datetime import datetime
from flask import current_app as app
from werkzeug.security import generate_password_hash
from cloudalbum.database.model_ddb import User, Photo


def solution_put_new_user(new_user_id, user_data):
    app.logger.info("RUNNING TODO#1 SOLUTION CODE:")
    app.logger.info("Put new signup user information!")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")

    user = User(new_user_id)
    user.email = user_data['email']
    user.password = generate_password_hash(user_data['password'])
    user.username = user_data['username']
    user.save()


def solution_get_user_data_with_idx(signin_data):
    app.logger.info("RUNNING TODO#2 SOLUTION CODE:")
    app.logger.info("Get user data with email which is Global Secondary Index")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")

    user = User.email_index.query(signin_data['email'])
    if user.total_count == 0:
        return None
    return user


def solution_put_photo_info_ddb(user_id, filename, form, filesize):
    app.logger.info("RUNNING TODO#3 SOLUTION CODE:")
    app.logger.info("Update Photo information into User table!")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")

    new_photo = Photo(id=filename,
          user_id=user_id,
          filename=filename,
          filename_orig=form['file'].filename,
          filesize=filesize,
          upload_date=datetime.today(),
          tags=form['tags'],
          desc=form['desc'],
          geotag_lat=form['geotag_lat'],
          geotag_lng=form['geotag_lng'],
          taken_date=datetime.strptime(form['taken_date'], "%Y:%m:%d %H:%M:%S"),
          make=form['make'],
          model=form['model'],
          width=form['width'],
          height=form['height'],
          city=form['city'],
          nation=form['nation'],
          address=form['address'])

    new_photo.save()


def solution_delete_photo_from_ddb(user, photo_id):
    app.logger.info("RUNNING TODO#4 SOLUTION CODE:")
    app.logger.info("Delete a photo from photos list, and update!")
    app.logger.info("Follow the steps in the lab guide to replace this method with your own implementation.")

    photo = Photo.get(user['user_id'], photo_id)
    photo.delete()
    filename = photo.filename

    return filename
