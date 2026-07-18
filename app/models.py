from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Association tables pour les relations many-to-many
participant_edition = db.Table('participant_edition',
    db.Column('participant_id', db.Integer, db.ForeignKey('participants.id'), primary_key=True),
    db.Column('edition_id', db.Integer, db.ForeignKey('editions.id'), primary_key=True)
)

session_speaker = db.Table('session_speaker',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    """Modèle utilisateur pour l'authentification admin"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    """Rôles des utilisateurs"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Role {self.name}>'

class Edition(db.Model):
    """Éditions du FASSIE"""
    __tablename__ = 'editions'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    theme = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(255))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    description = db.Column(db.Text)
    banner_image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    sessions = db.relationship('Session', backref='edition', lazy='dynamic', cascade='all, delete-orphan')
    participants = db.relationship('Participant', secondary=participant_edition, backref=db.backref('editions', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Edition {self.year}>'

class Participant(db.Model):
    """Participants au forum"""
    __tablename__ = 'participants'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    organization = db.Column(db.String(255))
    position = db.Column(db.String(255))
    profile_type = db.Column(db.String(50))  # participant, speaker, media, sponsor, partner, guest
    photo = db.Column(db.String(255))
    cv_path = db.Column(db.String(255))
    message = db.Column(db.Text)
    is_confirmed = db.Column(db.Boolean, default=False)
    confirmation_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Participant {self.registration_number}>'

class Speaker(db.Model):
    """Intervenants du forum"""
    __tablename__ = 'speakers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100))
    position = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    country = db.Column(db.String(100))
    biography = db.Column(db.Text)
    photo = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    sessions = db.relationship('Session', secondary=session_speaker, backref=db.backref('speakers', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Speaker {self.full_name}>'

class CommitteeMember(db.Model):
    """Membres des comités"""
    __tablename__ = 'committee_members'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    committee_type = db.Column(db.String(50))  # scientific, strategic, organization
    biography = db.Column(db.Text)
    photo = db.Column(db.String(255))
    is_chair = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CommitteeMember {self.first_name} {self.last_name}>'

class Session(db.Model):
    """Sessions du programme"""
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    edition_id = db.Column(db.Integer, db.ForeignKey('editions.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    session_type = db.Column(db.String(50))  # panel, roundtable, workshop, keynote
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    room = db.Column(db.String(100))
    moderator = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Session {self.title}>'

class Partner(db.Model):
    """Partenaires et sponsors"""
    __tablename__ = 'partners'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255))
    website = db.Column(db.String(255))
    category = db.Column(db.String(50))  # platinum, gold, silver, bronze, media, partner
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Partner {self.name}>'

class News(db.Model):
    """Actualités et blog"""
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    category = db.Column(db.String(50))
    featured_image = db.Column(db.String(255))
    author = db.Column(db.String(100))
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<News {self.title}>'

class Publication(db.Model):
    """Publications stratégiques"""
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    publication_type = db.Column(db.String(50))  # white_paper, report, strategic_note, recommendation
    file_path = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    publication_date = db.Column(db.Date)
    author = db.Column(db.String(255))
    edition_id = db.Column(db.Integer, db.ForeignKey('editions.id'))
    download_count = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Publication {self.title}>'

class Document(db.Model):
    """Documents divers"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    document_type = db.Column(db.String(50))
    category = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Document {self.title}>'

class Gallery(db.Model):
    """Galerie photos"""
    __tablename__ = 'galleries'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    edition_id = db.Column(db.Integer, db.ForeignKey('editions.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    images = db.relationship('GalleryImage', backref='gallery', lazy='dynamic', cascade='all, delete-orphan')

class GalleryImage(db.Model):
    """Images de la galerie"""
    __tablename__ = 'gallery_images'
    
    id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Video(db.Model):
    """Vidéos"""
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    video_path = db.Column(db.String(255))
    youtube_id = db.Column(db.String(50))
    thumbnail = db.Column(db.String(255))
    edition_id = db.Column(db.Integer, db.ForeignKey('editions.id'))
    is_featured = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Newsletter(db.Model):
    """Inscriptions newsletter"""
    __tablename__ = 'newsletters'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    """Messages de contact"""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.name}>'

class Statistic(db.Model):
    """Statistiques du site"""
    __tablename__ = 'statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), unique=True, nullable=False)
    metric_value = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
