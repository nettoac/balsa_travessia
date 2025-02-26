import unittest
from app import create_app, db
from app.models.balsa import Balsa

class BalsaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_balsa(self):
        balsa = Balsa(nome='Balsa 1', capacidade_maxima=100)
        db.session.add(balsa)
        db.session.commit()
        self.assertEqual(Balsa.query.count(), 1)