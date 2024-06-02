import json
from os import environ
import re

from flask import request

from app import app
from models import db, Bakery, BakedGood

class TestApp:
    '''Flask application in flask_app.py'''

    def test_creates_baked_goods(self):
        '''can POST new baked goods through "/baked_goods" route.'''

        with app.app_context():

            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if af:
                db.session.delete(af)
                db.session.commit()

            response = app.test_client().post(
                '/baked_goods',
                data={
                    "name": "Apple Fritter",
                    "price": 2,
                    "bakery_id": 5,
                }
            )

            af = BakedGood.query.filter_by(name="Apple Fritter").first()

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            assert af.id

    def test_updates_bakeries(self):
        '''can PATCH bakeries through "bakeries/<int:id>" route.'''

        with app.app_context():

            mb = Bakery.query.get(1)

            if mb is None:
                # If the bakery with id=1 doesn't exist, create one for testing
                mb = Bakery(id=1, name="Initial Bakery")
                db.session.add(mb)
                db.session.commit()

            # Update the bakery's name
            mb.name = "ABC Bakery"
            db.session.commit()

            # Re-query the database to get the updated state of mb
            updated_mb = Bakery.query.get(1)

            response = app.test_client().patch(
                '/bakeries/1',
                data={
                    "name": "Your Bakery",
                }
            )

            assert response.status_code == 200
            assert response.content_type == 'application/json'

            # Re-query the database to get the updated state of mb after the patch
            updated_mb_after_patch = Bakery.query.get(1)

            assert updated_mb_after_patch is not None
            assert updated_mb_after_patch.name == "Your Bakery"

    def test_deletes_baked_goods(self):
        '''can DELETE baked goods through "baked_goods/<int:id>" route.'''

        with app.app_context():
            
            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if not af:
                af = BakedGood(
                    name="Apple Fritter",
                    price=2,
                    bakery_id=5,
                )
                db.session.add(af)
                db.session.commit()
            

            response = app.test_client().delete(
                f'/baked_goods/{af.id}'
            )

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert not BakedGood.query.filter_by(name="Apple Fritter").first()