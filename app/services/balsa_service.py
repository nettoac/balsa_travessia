from ..models.balsa import Balsa
from .. import db

class BalsaService:
    @staticmethod
    def get_all_balsas():
        return Balsa.query.all()

    @staticmethod
    def get_balsa_by_id(id):
        return Balsa.query.get_or_404(id)

    @staticmethod
    def create_balsa(data):
        balsa = Balsa(nome=data['nome'], capacidade_maxima=data['capacidade_maxima'])
        db.session.add(balsa)
        db.session.commit()
        return balsa

    @staticmethod
    def update_balsa(id, data):
        balsa = Balsa.query.get_or_404(id)
        balsa.nome = data['nome']
        balsa.capacidade_maxima = data['capacidade_maxima']
        db.session.commit()
        return balsa

    @staticmethod
    def delete_balsa(id):
        balsa = Balsa.query.get_or_404(id)
        db.session.delete(balsa)
        db.session.commit()