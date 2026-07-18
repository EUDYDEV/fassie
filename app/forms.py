from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, DateField, DateTimeField, IntegerField, BooleanField, FileField, EmailField, TelField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError
from app.models import User, Participant

class LoginForm(FlaskForm):
    """Formulaire de connexion admin"""
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')

class RegistrationForm(FlaskForm):
    """Formulaire d'inscription participant simplifié"""
    first_name = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    
    email = EmailField('Email', validators=[DataRequired(), Email()])
    whatsapp = TelField('WhatsApp', validators=[DataRequired(), Length(max=20)])
    phone = TelField('Téléphone (joignable)', validators=[DataRequired(), Length(max=20)])
    
    def validate_email(self, field):
        if Participant.query.filter_by(email=field.data).first():
            raise ValidationError('Cet email est déjà utilisé.')

class ContactForm(FlaskForm):
    """Formulaire de contact"""
    name = StringField('Nom complet', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Téléphone', validators=[Optional(), Length(max=20)])
    subject = StringField('Sujet', validators=[DataRequired(), Length(min=3, max=255)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])

class NewsletterForm(FlaskForm):
    """Formulaire d'inscription newsletter"""
    email = EmailField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Prénom', validators=[Optional(), Length(max=50)])
    last_name = StringField('Nom', validators=[Optional(), Length(max=50)])

class SpeakerForm(FlaskForm):
    """Formulaire intervenant (admin)"""
    first_name = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    position = StringField('Fonction', validators=[Optional(), Length(max=255)])
    organization = StringField('Organisation', validators=[Optional(), Length(max=255)])
    country = StringField('Pays', validators=[Optional(), Length(max=100)])
    biography = TextAreaField('Biographie', validators=[Optional()])
    photo = FileField('Photo', validators=[Optional()])
    linkedin = StringField('LinkedIn', validators=[Optional(), Length(max=255)])
    twitter = StringField('Twitter', validators=[Optional(), Length(max=255)])
    is_featured = BooleanField('Intervenant vedette')

class PartnerForm(FlaskForm):
    """Formulaire partenaire (admin)"""
    name = StringField('Nom', validators=[DataRequired(), Length(min=2, max=255)])
    website = StringField('Site web', validators=[Optional(), Length(max=255)])
    category = SelectField('Catégorie', choices=[
        ('platinum', 'Platine'),
        ('gold', 'Or'),
        ('silver', 'Argent'),
        ('bronze', 'Bronze'),
        ('media', 'Média'),
        ('partner', 'Partenaire')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    logo = FileField('Logo', validators=[Optional()])
    is_active = BooleanField('Actif', default=True)

class NewsForm(FlaskForm):
    """Formulaire actualité (admin)"""
    title = StringField('Titre', validators=[DataRequired(), Length(min=3, max=255)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=255)])
    excerpt = StringField('Extrait', validators=[Optional(), Length(max=500)])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    category = SelectField('Catégorie', choices=[
        ('actualite', 'Actualité'),
        ('communique', 'Communiqué'),
        ('interview', 'Interview'),
        ('analyse', 'Analyse')
    ], validators=[DataRequired()])
    featured_image = FileField('Image à la une', validators=[Optional()])
    author = StringField('Auteur', validators=[Optional(), Length(max=100)])
    is_published = BooleanField('Publié', default=False)

class PublicationForm(FlaskForm):
    """Formulaire publication (admin)"""
    title = StringField('Titre', validators=[DataRequired(), Length(min=3, max=255)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Optional()])
    publication_type = SelectField('Type', choices=[
        ('white_paper', 'Livre blanc'),
        ('report', 'Rapport'),
        ('strategic_note', 'Note stratégique'),
        ('recommendation', 'Recommandation')
    ], validators=[DataRequired()])
    file = FileField('Fichier', validators=[DataRequired()])
    publication_date = DateField('Date de publication', validators=[DataRequired()])
    author = StringField('Auteur', validators=[Optional(), Length(max=255)])
    is_published = BooleanField('Publié', default=False)

class EditionForm(FlaskForm):
    """Formulaire édition (admin)"""
    year = IntegerField('Année', validators=[DataRequired()])
    theme = StringField('Thème', validators=[DataRequired(), Length(max=255)])
    start_date = DateField('Date de début', validators=[DataRequired()])
    end_date = DateField('Date de fin', validators=[DataRequired()])
    venue = StringField('Lieu', validators=[Optional(), Length(max=255)])
    city = StringField('Ville', validators=[Optional(), Length(max=100)])
    country = StringField('Pays', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    banner_image = FileField('Bannière', validators=[Optional()])
    is_active = BooleanField('Active', default=True)

class SessionForm(FlaskForm):
    """Formulaire session (admin)"""
    edition_id = SelectField('Édition', coerce=int, validators=[DataRequired()])
    title = StringField('Titre', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Optional()])
    session_type = SelectField('Type', choices=[
        ('keynote', 'Conférence principale'),
        ('panel', 'Panel'),
        ('roundtable', 'Table ronde'),
        ('workshop', 'Atelier')
    ], validators=[DataRequired()])
    start_time = DateTimeField('Heure de début', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    end_time = DateTimeField('Heure de fin', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    room = StringField('Salle', validators=[Optional(), Length(max=100)])
    moderator = StringField('Modérateur', validators=[Optional(), Length(max=255)])
    order = IntegerField('Ordre', validators=[Optional()], default=0)
