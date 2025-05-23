from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gelistirme_anahtari'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Flask-Login configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relationship with Personel
    personeller = db.relationship('Personel', back_populates='kullanici')

# Personnel model
class Personel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    workstationn = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(50), nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Reverse relationship with User
    kullanici = db.relationship('User', back_populates='personeller')

# Load user from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('E-posta veya şifre hatalı!', 'danger')
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    personnels = Personel.query.filter_by(kullanici_id=current_user.id).order_by(Personel.id.desc()).all()
    return render_template('dashboard.html', personnel=personnels)

# Add personnel
@app.route('/dashboard/add_personnel', methods=['GET', 'POST'])
@login_required
def add_personnel():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        workstation = request.form.get('workstation')
        service = request.form.get('service')

        new_personnel = Personel(
            name=name,
            surname=surname,
            workstationn=workstation,
            service=service,
            kullanici_id=current_user.id
        )
        db.session.add(new_personnel)
        db.session.commit()

        flash('Personel başarıyla eklendi!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_personnel.html')

# Personnel list page (new route)
@app.route('/dashboard/personnel_list')
@login_required
def personnel_list():
    personnels = Personel.query.filter_by(kullanici_id=current_user.id).all()
    return render_template('personnel_list.html', personnel=personnels)

# Edit personnel
@app.route('/dashboard/edit_personnel/<int:personnel_id>', methods=['GET', 'POST'])
@login_required
def edit_personnel(personnel_id):
    personel = Personel.query.get_or_404(personnel_id)

    if personel.kullanici_id != current_user.id:
        flash("Bu personele erişim yetkiniz yok!", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        personel.name = request.form['name']
        personel.surname = request.form['surname']
        personel.workstationn = request.form['workstation']
        personel.service = request.form['service']
        db.session.commit()
        flash('Personel bilgileri güncellendi.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_personnel.html', personnel=personel)

# Delete personnel (corrected route)
@app.route('/delete/personnel/<int:personnel_id>', methods=['POST'])
@login_required
def delete_personnel(personnel_id):
    personel = Personel.query.get_or_404(personnel_id)

    if personel.kullanici_id != current_user.id:
        flash("Bu kaydı silemezsiniz!", "danger")
        return redirect(url_for('dashboard'))

    db.session.delete(personel)
    db.session.commit()
    flash("Personel başarıyla silindi!", "success")
    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


#if __name__ == '__main__':
#    with app.app_context():
#        db.create_all()
#    app.run(debug=True)

import os 
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
