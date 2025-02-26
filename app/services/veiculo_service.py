from ..models.veiculo import Veiculo
from .. import db

class VeiculoService:
    @staticmethod
    def get_all_veiculos():
        return Veiculo.query.all()

    @staticmethod
    def get_veiculo_by_id(id):
        return Veiculo.query.get_or_404(id)

    @staticmethod
    def create_veiculo(data):
        veiculo = Veiculo(tipo=data['tipo'], peso_medio=data['peso_medio'])
        db.session.add(veiculo)
        db.session.commit()
        return veiculo

    @staticmethod
    def update_veiculo(id, data):
        veiculo = Veiculo.query.get_or_404(id)
        veiculo.tipo = data['tipo']
        veiculo.peso_medio = data['peso_medio']
        db.session.commit()
        return veiculo

    @staticmethod
    def delete_veiculo(id):
        veiculo = Veiculo.query.get_or_404(id)
        db.session.delete(veiculo)
        db.session.commit()