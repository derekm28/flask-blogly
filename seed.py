"""Seed file to make sample data for User db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
Alan = User(first_name='Alan', last_name = "Alda") #image_url = DEFAULT_IMAGE_URL)
Joel = User(first_name = 'Joel', last_name = "Burton") #image_url = 'DEFAULT_IMAGE_URL')
Jane = User(first_name = 'Jane', last_name = "Smith") #image_url = 'DEFAULT_IMAGE_URL')

# Add new objects to session, so they'll persist
db.session.add(Alan)
db.session.add(Joel)
db.session.add(Jane)

# Commit--otherwise, this never gets saved!
db.session.commit()
