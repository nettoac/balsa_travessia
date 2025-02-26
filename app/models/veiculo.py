from .. import db

class Veiculo(db.Model):
    __tablename__ = 'veiculo'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    peso_medio = db.Column(db.Float, nullable=False)

    # Relacionamento com RegistroTravessia
    registros = db.relationship('RegistroTravessia', back_populates='veiculo')