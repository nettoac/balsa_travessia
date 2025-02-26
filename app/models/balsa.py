from .. import db

class Balsa(db.Model):
    __tablename__ = 'balsa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade_maxima = db.Column(db.Integer, nullable=False)
    viagens = db.relationship('Viagem', backref='balsa', lazy=True)