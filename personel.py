# db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# Modèle utilisateur

class Personel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.Text, nullable=False)
    workstationn = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(50), nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Kullanıcıya ters ilişki

# Fonction d'export vers JSON
def export_users_to_json():
    with app.app_context():
        users = Personel.query.all()
        data = []
        for user in users:
            data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'password': user.password
            })

        import json
        with open('personel.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("✅ Utilisateurs exportés dans user.json avec succès !")

# Permet d'exécuter ce script seul
if __name__ == '__main__':
    export_users_to_json()
