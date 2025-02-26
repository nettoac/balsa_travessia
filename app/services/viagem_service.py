from ..models.viagem import Viagem
from .. import db

class ViagemService:
    @staticmethod
    def get_all_viagens():
        return Viagem.query.all()

    @staticmethod
    def get_viagem_by_id(id):
        return Viagem.query.get_or_404(id)

    @staticmethod
    def create_viagem(data):
        viagem = Viagem(
            balsa_id=data['balsa_id'],
            data_hora=data['data_hora'],
            quantidade_veiculos=data['quantidade_veiculos']
        )
        db.session.add(viagem)
        db.session.commit()
        return viagem

    @staticmethod
    def update_viagem(id, data):
        viagem = Viagem.query.get_or_404(id)
        viagem.balsa_id = data['balsa_id']
        viagem.data_hora = data['data_hora']
        db.session.commit()
        return viagem

    @staticmethod
    def delete_viagem(id):
        viagem = Viagem.query.get_or_404(id)
        db.session.delete(viagem)
        db.session.commit()