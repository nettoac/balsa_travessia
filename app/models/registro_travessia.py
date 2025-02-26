from .. import db

class RegistroTravessia(db.Model):
    __tablename__ = 'registro_travessia'
    id = db.Column(db.Integer, primary_key=True)
    viagem_id = db.Column(db.Integer, db.ForeignKey('viagem.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    # Relacionamento com Veiculo
    veiculo = db.relationship('Veiculo', back_populates='registros')

    # Relacionamento com Viagem
    viagem = db.relationship('Viagem', back_populates='registros')