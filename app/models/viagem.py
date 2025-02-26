from .. import db

class Viagem(db.Model):
    __tablename__ = 'viagem'
    id = db.Column(db.Integer, primary_key=True)
    balsa_id = db.Column(db.Integer, db.ForeignKey('balsa.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    quantidade_veiculos = db.Column(db.Integer, nullable=False)

    # Relacionamento com RegistroTravessia (com cascata)
    registros = db.relationship('RegistroTravessia', back_populates='viagem', cascade="all, delete-orphan")

    def get_quantidade_veiculo(self, veiculo_id):
        for registro in self.registros:
            if registro.veiculo_id == veiculo_id:
                return registro.quantidade
        return 0