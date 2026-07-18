from flask import render_template, redirect, url_for, flash, request, current_app
from app.main import bp
from app.models import Edition, Speaker, Partner, News, Publication, Participant, Statistic
from app.forms import ContactForm, NewsletterForm, RegistrationForm
from app import db, mail
from flask_mail import Message
from datetime import datetime
import secrets

@bp.route('/')
def index():
    """Page d'accueil"""
    # Récupérer l'édition active
    active_edition = Edition.query.filter_by(is_active=True).first()
    
    # Récupérer les intervenants vedettes
    featured_speakers = Speaker.query.filter_by(is_featured=True).limit(6).all()
    
    # Récupérer les partenaires principaux
    main_partners = Partner.query.filter_by(is_active=True).filter(
        Partner.category.in_(['platinum', 'gold'])
    ).limit(8).all()
    
    # Récupérer les actualités récentes
    recent_news = News.query.filter_by(is_published=True).order_by(
        News.published_at.desc()
    ).limit(3).all()
    
    # Récupérer les vraies statistiques depuis la base de données
    stats = {
        'participants': Participant.query.count(),
        'speakers': Speaker.query.count(),
        'partners': Partner.query.filter_by(is_active=True).count(),
        'news': News.query.filter_by(is_published=True).count(),
        'publications': Publication.query.filter_by(is_published=True).count(),
        'countries': len(set(p.country for p in Participant.query.all())) if Participant.query.count() > 0 else 0
    }
    
    return render_template('index.html',
                         active_edition=active_edition,
                         featured_speakers=featured_speakers,
                         main_partners=main_partners,
                         recent_news=recent_news,
                         stats=stats)

@bp.route('/about')
def about():
    """Page À propos"""
    return render_template('about.html')

@bp.route('/edition/<int:year>')
def edition(year):
    """Page d'une édition spécifique"""
    edition = Edition.query.filter_by(year=year).first_or_404()
    sessions = edition.sessions.order_by('start_time').all()
    return render_template('edition.html', edition=edition, sessions=sessions, active_edition=edition)

@bp.route('/speakers')
def speakers():
    """Page des intervenants"""
    speakers = Speaker.query.order_by(Speaker.last_name).all()
    return render_template('speakers.html', speakers=speakers)

@bp.route('/speakers/<int:id>')
def speaker_detail(id):
    """Détail d'un intervenant"""
    speaker = Speaker.query.get_or_404(id)
    return render_template('speaker_detail.html', speaker=speaker)

@bp.route('/committee')
def committee():
    """Page des comités"""
    from app.models import CommitteeMember
    scientific = CommitteeMember.query.filter_by(committee_type='scientific').all()
    strategic = CommitteeMember.query.filter_by(committee_type='strategic').all()
    organization = CommitteeMember.query.filter_by(committee_type='organization').all()
    return render_template('committee.html',
                         scientific=scientific,
                         strategic=strategic,
                         organization=organization)

@bp.route('/partners')
def partners():
    """Page des partenaires"""
    partners = Partner.query.filter_by(is_active=True).order_by(
        Partner.category.desc()
    ).all()
    return render_template('partners.html', partners=partners)

@bp.route('/become-partner', methods=['GET', 'POST'])
def become_partner():
    """Page devenir partenaire"""
    return render_template('become_partner.html')

@bp.route('/news')
def news():
    """Page des actualités"""
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(is_published=True).order_by(
        News.published_at.desc()
    ).paginate(page=page, per_page=10)
    return render_template('news.html', news=news)

@bp.route('/news/<slug>')
def news_detail(slug):
    """Détail d'une actualité"""
    news = News.query.filter_by(slug=slug).first_or_404()
    return render_template('news_detail.html', news=news)

@bp.route('/publications')
def publications():
    """Page des publications"""
    publications = Publication.query.filter_by(is_published=True).order_by(
        Publication.publication_date.desc()
    ).all()
    return render_template('publications.html', publications=publications)

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Page de contact"""
    form = ContactForm()
    if form.validate_on_submit():
        from app.models import Contact
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        
        # Envoyer l'email
        msg = Message(f'Contact FASSIE: {form.subject.data}',
                      recipients=[current_app.config['MAIL_DEFAULT_SENDER']])
        msg.body = f'''
Nom: {form.name.data}
Email: {form.email.data}
Téléphone: {form.phone.data}
Sujet: {form.subject.data}

Message:
{form.message.data}
        '''
        mail.send(msg)
        
        flash('Votre message a été envoyé avec succès. Nous vous répondrons bientôt.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Page d'inscription"""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Générer un numéro d'inscription unique
        registration_number = f'FASSIE-{datetime.now().year}-{secrets.token_hex(4).upper()}'
        
        participant = Participant(
            registration_number=registration_number,
            profile_type='participant',
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender='A',
            email=form.email.data,
            phone=form.phone.data,
            whatsapp=form.whatsapp.data,
            country='Côte d\'Ivoire',
            city='Abidjan',
            organization='',
            position='',
            message='',
            is_confirmed=False
        )
        
        db.session.add(participant)
        db.session.commit()
        
        # Envoyer l'email de confirmation
        msg = Message('Confirmation d\'inscription FASSIE',
                      recipients=[form.email.data])
        msg.body = f'''
Cher/Chère {form.first_name.data} {form.last_name.data},

Votre inscription au FASSIE a été enregistrée avec succès.

Numéro d'inscription: {registration_number}

Nous vous contacterons bientôt avec plus d'informations.

Cordialement,
L'équipe FASSIE
        '''
        mail.send(msg)
        
        flash('Votre inscription a été enregistrée avec succès. Un email de confirmation vous a été envoyé.', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('register.html', form=form)

@bp.route('/newsletter', methods=['POST'])
def newsletter():
    """Inscription newsletter"""
    form = NewsletterForm()
    if form.validate_on_submit():
        from app.models import Newsletter
        newsletter = Newsletter(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(newsletter)
        db.session.commit()
        
        flash('Vous êtes maintenant inscrit à notre newsletter.', 'success')
    else:
        flash('Veuillez entrer une adresse email valide.', 'error')
    
    return redirect(url_for('main.index'))

@bp.route('/download/<int:id>')
def download_publication(id):
    """Télécharger une publication"""
    publication = Publication.query.get_or_404(id)
    publication.download_count += 1
    db.session.commit()
    return redirect(url_for('static', filename=publication.file_path))
