# FASSIE - Forum Africain de la Souveraineté Stratégique et de l'Intelligence Économique

Plateforme web professionnelle et évolutive pour le Forum Africain de la Souveraineté Stratégique et de l'Intelligence Économique (FASSIE).

## 🚀 Technologies

### Backend
- **Python 3.8+**
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM
- **Flask-Login** - Authentification
- **Flask-Migrate** - Migrations de base de données
- **Flask-Mail** - Envoi d'emails
- **Flask-Bcrypt** - Hashage des mots de passe
- **MySQL** - Base de données

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript ES6**
- **Bootstrap 5** - Framework CSS
- **GSAP** - Animations
- **AOS** - Animations au scroll
- **Font Awesome** - Icônes
- **Google Fonts** - Typographie

## 📋 Prérequis

- Python 3.8 ou supérieur
- MySQL 5.7 ou supérieur
- pip (gestionnaire de paquets Python)
- virtualenv (recommandé)

## 🛠️ Installation

### 1. Cloner le repository

```bash
git clone <repository-url>
cd fassie
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

#### Windows:
```bash
venv\Scripts\activate
```

#### Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données MySQL

```sql
CREATE DATABASE fassie_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=votre-cle-secrete-ici
DATABASE_URL=mysql+pymysql://root:votre_mot_de_passe@localhost/fassie_db?charset=utf8mb4
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=votre_email@gmail.com
MAIL_PASSWORD=votre_mot_de_passe_app
MAIL_DEFAULT_SENDER=noreply@fassie.org
```

### 6. Initialiser la base de données

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Créer les données initiales

```bash
flask init-db
```

Cela créera:
- Un utilisateur admin (username: `admin`, password: `admin123`)
- Des statistiques par défaut
- L'édition FASSIE 2027

⚠️ **Important**: Changez le mot de passe admin par défaut après la première connexion!

### 8. Lancer l'application

```bash
python run.py
```

L'application sera accessible sur `http://localhost:5000`

## 📁 Structure du projet

```
FASSIE/
├── app/
│   ├── __init__.py          # Initialisation de l'application Flask
│   ├── models.py            # Modèles de base de données
│   ├── forms.py             # Formulaires WTForms
│   ├── auth/                # Blueprint authentification
│   ├── admin/               # Blueprint administration
│   ├── api/                 # Blueprint API
│   ├── errors/              # Gestion des erreurs
│   ├── main/                # Blueprint principal
│   ├── templates/           # Templates Jinja2
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── register.html
│   │   ├── contact.html
│   │   └── auth/
│   │       └── login.html
│   └── static/              # Fichiers statiques
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       ├── images/
│       ├── documents/
│       └── uploads/
├── migrations/              # Migrations de base de données
├── config.py               # Configuration de l'application
├── requirements.txt        # Dépendances Python
├── run.py                 # Point d'entrée
└── README.md              # Ce fichier
```

## 👥 Utilisateurs

### Créer un nouvel administrateur

```bash
flask create-admin
```

Suivez les instructions pour créer un nouveau compte administrateur.

## 🔐 Sécurité

- **CSRF Protection**: Activée par défaut avec Flask-WTF
- **XSS Protection**: Templates Jinja2 échappent automatiquement le HTML
- **SQL Injection Protection**: SQLAlchemy utilise des requêtes paramétrées
- **Password Hashing**: Utilisation de bcrypt avec Flask-Bcrypt
- **Session Security**: Cookies sécurisés avec HTTPOnly et SameSite

## 📊 Fonctionnalités

### Site Public
- ✅ Page d'accueil avec hero section et compte à rebours
- ✅ Page À propos (vision, mission, valeurs)
- ✅ Pages des éditions (2027, 2028, 2029)
- ✅ Page des intervenants
- ✅ Page des partenaires
- ✅ Système de blog/actualités
- ✅ Bibliothèque de publications
- ✅ Formulaire de contact
- ✅ Système d'inscription des participants
- ✅ Newsletter

### Administration
- ✅ Tableau de bord avec statistiques
- ✅ Gestion des participants
- ✅ Export CSV/Excel des inscrits
- ✅ Gestion des intervenants
- ✅ Gestion des partenaires
- ✅ Gestion des actualités
- ✅ Gestion des publications
- ✅ Gestion des éditions
- ✅ Gestion du programme
- ✅ Gestion des contacts
- ✅ Gestion des statistiques

## 🎨 Design

- **Palette de couleurs**:
  - Vert foncé: `#1a4d2e`
  - Doré: `#d4af37`
  - Blanc: `#ffffff`
  - Gris clair: `#f8f9fa`

- **Typographie**:
  - Titres: Playfair Display
  - Corps: Montserrat

- **Animations**:
  - GSAP pour les animations complexes
  - AOS pour les animations au scroll
  - Transitions CSS fluides

## 🚀 Déploiement

### Production

1. Définir les variables d'environnement de production
2. Désactiver le mode debug
3. Utiliser un serveur WSGI (Gunicorn)
4. Configurer HTTPS
5. Optimiser les fichiers statiques
6. Configurer les backups de base de données

### Exemple avec Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## 📝 Personnalisation

### Logo

Placez votre logo dans:
- `app/static/images/logo.png` (version couleur)
- `app/static/images/logo-white.png` (version blanche pour footer)

### Images de fond

Placez les images dans:
- `app/static/images/` pour les images statiques
- `app/static/videos/` pour les vidéos

### Configuration

Modifiez `config.py` pour ajuster:
- Les paramètres de base de données
- La configuration email
- Les paramètres de session
- Les limites d'upload

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.

## 📞 Support

Pour toute question ou problème, contactez:
- Email: contact@fassie.org
- Site web: https://fassie.org

## 🙏 Remerciements

- L'équipe Flask pour le framework excellent
- La communauté Python pour les bibliothèques incroyables
- Tous les contributeurs du projet

---

**Développé avec ❤️ pour l'Afrique**
