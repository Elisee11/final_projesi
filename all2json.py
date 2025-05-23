from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Modeller tablolar
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    personnels = db.relationship('personnel', backref='user', lazy=True)

class personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.Text, nullable=False)
    workstation = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(50), nullable=False)
    
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def export_all_to_json():
    with app.app_context():
        users = User.query.all()
        data = []
        for user in users:
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'personnels': []
            }

            for personnel in user.personnels:
                gunluk_data = {
                    'id': personnel.id,
                    'name': personnel.name,
                    'surname': personnel.surname,
                    'workstation': personnel.workstation,
                    'service': personnel.service,
                }
                user_data['personnels'].append(gunluk_data)

            data.append(user_data)

        with open('kullanicilar_ve_personnel.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Veriler başarıyla kullanicilar_ve_gunlukler.json dosyasına kaydedildi!")

if __name__ == '__main__':
    export_all_to_json()