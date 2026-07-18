from app import create_app, db
from app.models import User, Edition, Speaker, Partner, Statistic
from flask_migrate import upgrade
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Contexte pour le shell Flask"""
    return {'db': db, 'User': User, 'Edition': Edition, 'Speaker': Speaker, 'Partner': Partner, 'Statistic': Statistic}

@app.cli.command()
def init_db():
    """Initialiser la base de données avec des données de démonstration"""
    db.create_all()
    
    # Créer l'utilisateur admin par défaut
    admin = User(
        username='admin',
        email='admin@fassie.org',
        first_name='Admin',
        last_name='FASSIE',
        is_admin=True,
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Créer des statistiques par défaut
    stats = [
        Statistic(metric_name='participants', metric_value=500),
        Statistic(metric_name='speakers', metric_value=50),
        Statistic(metric_name='countries', metric_value=30),
        Statistic(metric_name='partners', metric_value=20),
        Statistic(metric_name='editions', metric_value=1)
    ]
    for stat in stats:
        db.session.add(stat)
    
    # Créer l'édition 2027
    from datetime import date
    edition_2027 = Edition(
        year=2027,
        theme='Souveraineté Numérique et Intelligence Économique pour l\'Afrique',
        start_date=date(2027, 6, 15),
        end_date=date(2027, 6, 17),
        venue='Palais des Congrès',
        city='Abidjan',
        country='Côte d\'Ivoire',
        description='La première édition du FASSIE se concentrera sur les défis et opportunités de la souveraineté numérique et de l\'intelligence économique en Afrique.',
        is_active=True
    )
    db.session.add(edition_2027)
    
    db.session.commit()
    print('Base de données initialisée avec succès!')
    print('Utilisateur admin créé: username=admin, password=admin123')
    print('N\'oubliez pas de changer le mot de passe par défaut!')

@app.cli.command()
def create_admin():
    """Créer un nouvel administrateur"""
    import getpass
    
    username = input('Nom d\'utilisateur: ')
    email = input('Email: ')
    first_name = input('Prénom: ')
    last_name = input('Nom: ')
    password = getpass.getpass('Mot de passe: ')
    password_confirm = getpass.getpass('Confirmer le mot de passe: ')
    
    if password != password_confirm:
        print('Les mots de passe ne correspondent pas!')
        return
    
    if User.query.filter_by(username=username).first():
        print('Ce nom d\'utilisateur existe déjà!')
        return
    
    if User.query.filter_by(email=email).first():
        print('Cet email existe déjà!')
        return
    
    admin = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_admin=True,
        is_active=True
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    
    print(f'Administrateur {username} créé avec succès!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
