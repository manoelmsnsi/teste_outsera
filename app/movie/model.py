from app.extensions import db

class MoviesData(db.Model):
    __tablename__ = "movies"
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela se já existir

    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(254), nullable=False)
    studios = db.Column(db.String(254), nullable=False)
    producers = db.Column(db.String(254), nullable=False)
    winner = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return f"<MoviesData {self.title}>"
