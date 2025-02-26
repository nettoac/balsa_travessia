from ..models.registro_travessia import RegistroTravessia
from .. import db

class RegistroService:
    @staticmethod
    def get_all_registros():
        return RegistroTravessia.query.all()
    
    @staticmethod
    def get_registro_by_viagem_e_veiculo(viagem_id, veiculo_id):
        return RegistroTravessia.query.filter_by(viagem_id=viagem_id, veiculo_id=veiculo_id).first()

    @staticmethod
    def create_registro(data):
        registro = RegistroTravessia(
            viagem_id=data['viagem_id'],
            veiculo_id=data['veiculo_id'],
            quantidade=data['quantidade']
        )
        db.session.add(registro)
        db.session.commit()
        return registro