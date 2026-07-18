from flask import render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User, Participant, Speaker, Partner, News, Publication, Edition, Session, CommitteeMember, Contact, Statistic
from app.forms import SpeakerForm, PartnerForm, NewsForm, PublicationForm, EditionForm, SessionForm
from app import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import secrets
import csv
from io import StringIO

@bp.route('/dashboard')
def dashboard():
    """Tableau de bord admin"""
    # Statistiques
    total_participants = Participant.query.count()
    total_speakers = Speaker.query.count()
    total_partners = Partner.query.count()
    total_news = News.query.filter_by(is_published=True).count()
    
    # Inscriptions récentes
    recent_registrations = Participant.query.order_by(
        Participant.created_at.desc()
    ).limit(10).all()
    
    # Contacts non lus
    unread_contacts = Contact.query.filter_by(is_read=False).count()
    
    # Éditions
    editions = Edition.query.all()
    active_edition = Edition.query.filter_by(is_active=True).first()
    
    return render_template('admin/dashboard.html',
                         total_participants=total_participants,
                         total_speakers=total_speakers,
                         total_partners=total_partners,
                         total_news=total_news,
                         recent_registrations=recent_registrations,
                         unread_contacts=unread_contacts,
                         editions=editions,
                         active_edition=active_edition)

# Gestion des participants
@bp.route('/participants')
def participants():
    """Liste des participants"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Participant.query
    if search:
        query = query.filter(
            db.or_(
                Participant.first_name.ilike(f'%{search}%'),
                Participant.last_name.ilike(f'%{search}%'),
                Participant.email.ilike(f'%{search}%'),
                Participant.registration_number.ilike(f'%{search}%')
            )
        )
    
    participants = query.order_by(Participant.created_at.desc()).paginate(
        page=page, per_page=20
    )
    
    return render_template('admin/participants.html', participants=participants, search=search)

@bp.route('/participants/export')
def export_participants():
    """Exporter les participants en CSV"""
    participants = Participant.query.all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Numéro', 'Prénom', 'Nom', 'Email', 'Téléphone', 'Pays', 'Ville',
        'Organisation', 'Fonction', 'Type de profil', 'Date d\'inscription'
    ])
    
    for p in participants:
        writer.writerow([
            p.registration_number, p.first_name, p.last_name, p.email,
            p.phone, p.country, p.city, p.organization, p.position,
            p.profile_type, p.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'participants_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@bp.route('/participants/<int:id>/confirm')
def confirm_participant(id):
    """Confirmer un participant"""
    participant = Participant.query.get_or_404(id)
    participant.is_confirmed = True
    participant.confirmation_date = datetime.utcnow()
    db.session.commit()
    flash('Participant confirmé avec succès.', 'success')
    return redirect(url_for('admin.participants'))

@bp.route('/participants/<int:id>/delete')
def delete_participant(id):
    """Supprimer un participant"""
    participant = Participant.query.get_or_404(id)
    db.session.delete(participant)
    db.session.commit()
    flash('Participant supprimé avec succès.', 'success')
    return redirect(url_for('admin.participants'))

# Gestion des intervenants
@bp.route('/speakers')
def speakers():
    """Liste des intervenants"""
    speakers = Speaker.query.order_by(Speaker.last_name).all()
    return render_template('admin/speakers.html', speakers=speakers)

@bp.route('/speakers/new', methods=['GET', 'POST'])
def new_speaker():
    """Ajouter un intervenant"""
    form = SpeakerForm()
    if form.validate_on_submit():
        speaker = Speaker(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            full_name=f"{form.first_name.data} {form.last_name.data}",
            position=form.position.data,
            organization=form.organization.data,
            country=form.country.data,
            biography=form.biography.data,
            linkedin=form.linkedin.data,
            twitter=form.twitter.data,
            is_featured=form.is_featured.data
        )
        
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.photo.data.save(filepath)
            speaker.photo = f'uploads/{unique_filename}'
        
        db.session.add(speaker)
        db.session.commit()
        flash('Intervenant ajouté avec succès.', 'success')
        return redirect(url_for('admin.speakers'))
    
    return render_template('admin/speaker_form.html', form=form, title='Nouvel intervenant')

@bp.route('/speakers/<int:id>/edit', methods=['GET', 'POST'])
def edit_speaker(id):
    """Modifier un intervenant"""
    speaker = Speaker.query.get_or_404(id)
    form = SpeakerForm(obj=speaker)
    
    if form.validate_on_submit():
        speaker.first_name = form.first_name.data
        speaker.last_name = form.last_name.data
        speaker.full_name = f"{form.first_name.data} {form.last_name.data}"
        speaker.position = form.position.data
        speaker.organization = form.organization.data
        speaker.country = form.country.data
        speaker.biography = form.biography.data
        speaker.linkedin = form.linkedin.data
        speaker.twitter = form.twitter.data
        speaker.is_featured = form.is_featured.data
        
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.photo.data.save(filepath)
            speaker.photo = f'uploads/{unique_filename}'
        
        db.session.commit()
        flash('Intervenant modifié avec succès.', 'success')
        return redirect(url_for('admin.speakers'))
    
    return render_template('admin/speaker_form.html', form=form, title='Modifier intervenant')

@bp.route('/speakers/<int:id>/delete')
def delete_speaker(id):
    """Supprimer un intervenant"""
    speaker = Speaker.query.get_or_404(id)
    db.session.delete(speaker)
    db.session.commit()
    flash('Intervenant supprimé avec succès.', 'success')
    return redirect(url_for('admin.speakers'))

# Gestion des partenaires
@bp.route('/partners')
def partners():
    """Liste des partenaires"""
    partners = Partner.query.order_by(Partner.category.desc()).all()
    return render_template('admin/partners.html', partners=partners)

@bp.route('/partners/new', methods=['GET', 'POST'])
def new_partner():
    """Ajouter un partenaire"""
    form = PartnerForm()
    if form.validate_on_submit():
        partner = Partner(
            name=form.name.data,
            website=form.website.data,
            category=form.category.data,
            description=form.description.data,
            is_active=form.is_active.data
        )
        
        if form.logo.data:
            filename = secure_filename(form.logo.data.filename)
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.logo.data.save(filepath)
            partner.logo = f'uploads/{unique_filename}'
        
        db.session.add(partner)
        db.session.commit()
        flash('Partenaire ajouté avec succès.', 'success')
        return redirect(url_for('admin.partners'))
    
    return render_template('admin/partner_form.html', form=form, title='Nouveau partenaire')

@bp.route('/partners/<int:id>/edit', methods=['GET', 'POST'])
def edit_partner(id):
    """Modifier un partenaire"""
    partner = Partner.query.get_or_404(id)
    form = PartnerForm(obj=partner)
    
    if form.validate_on_submit():
        partner.name = form.name.data
        partner.website = form.website.data
        partner.category = form.category.data
        partner.description = form.description.data
        partner.is_active = form.is_active.data
        
        if form.logo.data:
            filename = secure_filename(form.logo.data.filename)
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.logo.data.save(filepath)
            partner.logo = f'uploads/{unique_filename}'
        
        db.session.commit()
        flash('Partenaire modifié avec succès.', 'success')
        return redirect(url_for('admin.partners'))
    
    return render_template('admin/partner_form.html', form=form, title='Modifier partenaire')

@bp.route('/partners/<int:id>/delete')
def delete_partner(id):
    """Supprimer un partenaire"""
    partner = Partner.query.get_or_404(id)
    db.session.delete(partner)
    db.session.commit()
    flash('Partenaire supprimé avec succès.', 'success')
    return redirect(url_for('admin.partners'))

# Gestion des actualités
@bp.route('/news')
def news():
    """Liste des actualités"""
    news = News.query.order_by(News.created_at.desc()).all()
    return render_template('admin/news.html', news=news)

@bp.route('/news/new', methods=['GET', 'POST'])
def new_news():
    """Ajouter une actualité"""
    form = NewsForm()
    if form.validate_on_submit():
        news = News(
            title=form.title.data,
            slug=form.slug.data,
            excerpt=form.excerpt.data,
            content=form.content.data,
            category=form.category.data,
            author=form.author.data,
            is_published=form.is_published.data,
            published_at=datetime.utcnow() if form.is_published.data else None
        )
        
        if form.featured_image.data:
            filename = secure_filename(form.featured_image.data.filename)
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.featured_image.data.save(filepath)
            news.featured_image = f'uploads/{unique_filename}'
        
        db.session.add(news)
        db.session.commit()
        flash('Actualité ajoutée avec succès.', 'success')
        return redirect(url_for('admin.news'))
    
    return render_template('admin/news_form.html', form=form, title='Nouvelle actualité')

@bp.route('/news/<int:id>/edit', methods=['GET', 'POST'])
def edit_news(id):
    """Modifier une actualité"""
    news = News.query.get_or_404(id)
    form = NewsForm(obj=news)
    
    if form.validate_on_submit():
        news.title = form.title.data
        news.slug = form.slug.data
        news.excerpt = form.excerpt.data
        news.content = form.content.data
        news.category = form.category.data
        news.author = form.author.data
        news.is_published = form.is_published.data
        
        if form.is_published.data and not news.published_at:
            news.published_at = datetime.utcnow()
        
        if form.featured_image.data:
            filename = secure_filename(form.featured_image.data.filename)
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.featured_image.data.save(filepath)
            news.featured_image = f'uploads/{unique_filename}'
        
        db.session.commit()
        flash('Actualité modifiée avec succès.', 'success')
        return redirect(url_for('admin.news'))
    
    return render_template('admin/news_form.html', form=form, title='Modifier actualité')

@bp.route('/news/<int:id>/delete')
def delete_news(id):
    """Supprimer une actualité"""
    news = News.query.get_or_404(id)
    db.session.delete(news)
    db.session.commit()
    flash('Actualité supprimée avec succès.', 'success')
    return redirect(url_for('admin.news'))

# Gestion des publications
@bp.route('/publications')
def publications():
    """Liste des publications"""
    publications = Publication.query.order_by(Publication.created_at.desc()).all()
    return render_template('admin/publications.html', publications=publications)

@bp.route('/publications/new', methods=['GET', 'POST'])
def new_publication():
    """Ajouter une publication"""
    form = PublicationForm()
    # Remplir le select des éditions
    form.edition_id.choices = [(e.id, f'FASSIE {e.year}') for e in Edition.query.all()]
    form.edition_id.choices.insert(0, (0, 'Aucune'))
    
    if form.validate_on_submit():
        file = form.file.data
        filename = file.filename
        unique_filename = f"{secrets.token_hex(8)}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        publication = Publication(
            title=form.title.data,
            slug=form.slug.data,
            description=form.description.data,
            publication_type=form.publication_type.data,
            file_path=f'uploads/{unique_filename}',
            file_size=os.path.getsize(filepath),
            publication_date=form.publication_date.data,
            author=form.author.data,
            edition_id=form.edition_id.data if form.edition_id.data != 0 else None,
            is_published=form.is_published.data
        )
        
        db.session.add(publication)
        db.session.commit()
        flash('Publication ajoutée avec succès.', 'success')
        return redirect(url_for('admin.publications'))
    
    return render_template('admin/publication_form.html', form=form, title='Nouvelle publication')

@bp.route('/publications/<int:id>/delete')
def delete_publication(id):
    """Supprimer une publication"""
    publication = Publication.query.get_or_404(id)
    db.session.delete(publication)
    db.session.commit()
    flash('Publication supprimée avec succès.', 'success')
    return redirect(url_for('admin.publications'))

@bp.route('/publications/<int:id>/edit', methods=['GET', 'POST'])
def edit_publication(id):
    """Modifier une publication"""
    publication = Publication.query.get_or_404(id)
    form = PublicationForm(obj=publication)
    form.edition_id.choices = [(e.id, f'FASSIE {e.year}') for e in Edition.query.all()]
    form.edition_id.choices.insert(0, (0, 'Aucune'))
    
    if form.validate_on_submit():
        publication.title = form.title.data
        publication.slug = form.slug.data
        publication.description = form.description.data
        publication.publication_type = form.publication_type.data
        publication.publication_date = form.publication_date.data
        publication.author = form.author.data
        publication.edition_id = form.edition_id.data if form.edition_id.data != 0 else None
        publication.is_published = form.is_published.data
        
        if form.file.data:
            file = form.file.data
            filename = file.filename
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            publication.file_path = f'uploads/{unique_filename}'
            publication.file_size = os.path.getsize(filepath)
        
        db.session.commit()
        flash('Publication modifiée avec succès.', 'success')
        return redirect(url_for('admin.publications'))
    
    return render_template('admin/publication_form.html', form=form, title='Modifier publication')

# Gestion des éditions
@bp.route('/editions')
def editions():
    """Liste des éditions"""
    editions = Edition.query.order_by(Edition.year.desc()).all()
    return render_template('admin/editions.html', editions=editions)

@bp.route('/editions/new', methods=['GET', 'POST'])
def new_edition():
    """Ajouter une édition"""
    form = EditionForm()
    if form.validate_on_submit():
        edition = Edition(
            year=form.year.data,
            theme=form.theme.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            venue=form.venue.data,
            city=form.city.data,
            country=form.country.data,
            description=form.description.data,
            is_active=form.is_active.data
        )
        
        if form.banner_image.data:
            filename = secure_filename(form.banner_image.data.filename)
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.banner_image.data.save(filepath)
            edition.banner_image = f'uploads/{unique_filename}'
        
        db.session.add(edition)
        db.session.commit()
        flash('Édition ajoutée avec succès.', 'success')
        return redirect(url_for('admin.editions'))
    
    return render_template('admin/edition_form.html', form=form, title='Nouvelle édition')

@bp.route('/editions/<int:id>/edit', methods=['GET', 'POST'])
def edit_edition(id):
    """Modifier une édition"""
    edition = Edition.query.get_or_404(id)
    form = EditionForm(obj=edition)
    
    if form.validate_on_submit():
        edition.year = form.year.data
        edition.theme = form.theme.data
        edition.start_date = form.start_date.data
        edition.end_date = form.end_date.data
        edition.venue = form.venue.data
        edition.city = form.city.data
        edition.country = form.country.data
        edition.description = form.description.data
        edition.is_active = form.is_active.data
        
        if form.banner_image.data:
            filename = secure_filename(form.banner_image.data.filename)
            unique_filename = f"{secrets.token_hex(8)}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            form.banner_image.data.save(filepath)
            edition.banner_image = f'uploads/{unique_filename}'
        
        db.session.commit()
        flash('Édition modifiée avec succès.', 'success')
        return redirect(url_for('admin.editions'))
    
    return render_template('admin/edition_form.html', form=form, title='Modifier édition')

@bp.route('/editions/<int:id>/delete')
def delete_edition(id):
    """Supprimer une édition"""
    edition = Edition.query.get_or_404(id)
    db.session.delete(edition)
    db.session.commit()
    flash('Édition supprimée avec succès.', 'success')
    return redirect(url_for('admin.editions'))

# Gestion des sessions
@bp.route('/sessions')
def sessions():
    """Liste des sessions"""
    sessions = Session.query.order_by(Session.start_time.desc()).all()
    return render_template('admin/sessions.html', sessions=sessions)

@bp.route('/sessions/new', methods=['GET', 'POST'])
def new_session():
    """Ajouter une session"""
    form = SessionForm()
    form.edition_id.choices = [(e.id, f'FASSIE {e.year}') for e in Edition.query.all()]
    
    if form.validate_on_submit():
        session = Session(
            edition_id=form.edition_id.data,
            title=form.title.data,
            description=form.description.data,
            session_type=form.session_type.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            room=form.room.data,
            moderator=form.moderator.data,
            order=form.order.data
        )
        
        db.session.add(session)
        db.session.commit()
        flash('Session ajoutée avec succès.', 'success')
        return redirect(url_for('admin.sessions'))
    
    return render_template('admin/session_form.html', form=form, title='Nouvelle session')

@bp.route('/sessions/<int:id>/delete')
def delete_session(id):
    """Supprimer une session"""
    session = Session.query.get_or_404(id)
    db.session.delete(session)
    db.session.commit()
    flash('Session supprimée avec succès.', 'success')
    return redirect(url_for('admin.sessions'))

@bp.route('/sessions/<int:id>/edit', methods=['GET', 'POST'])
def edit_session(id):
    """Modifier une session"""
    session = Session.query.get_or_404(id)
    form = SessionForm(obj=session)
    form.edition_id.choices = [(e.id, f'FASSIE {e.year}') for e in Edition.query.all()]
    
    if form.validate_on_submit():
        session.edition_id = form.edition_id.data
        session.title = form.title.data
        session.description = form.description.data
        session.session_type = form.session_type.data
        session.start_time = form.start_time.data
        session.end_time = form.end_time.data
        session.room = form.room.data
        session.moderator = form.moderator.data
        session.order = form.order.data
        
        db.session.commit()
        flash('Session modifiée avec succès.', 'success')
        return redirect(url_for('admin.sessions'))
    
    return render_template('admin/session_form.html', form=form, title='Modifier session')

# Gestion des contacts
@bp.route('/contacts')
def contacts():
    """Liste des contacts"""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@bp.route('/contacts/<int:id>/mark-read')
def mark_contact_read(id):
    """Marquer un contact comme lu"""
    contact = Contact.query.get_or_404(id)
    contact.is_read = True
    db.session.commit()
    flash('Contact marqué comme lu.', 'success')
    return redirect(url_for('admin.contacts'))

@bp.route('/contacts/<int:id>/delete')
def delete_contact(id):
    """Supprimer un contact"""
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact supprimé avec succès.', 'success')
    return redirect(url_for('admin.contacts'))

# Gestion des statistiques
@bp.route('/statistics')
def statistics():
    """Gestion des statistiques"""
    # Statistiques générales
    total_participants = Participant.query.count()
    total_speakers = Speaker.query.count()
    total_partners = Partner.query.count()
    total_news = News.query.filter_by(is_published=True).count()
    total_publications = Publication.query.filter_by(is_published=True).count()
    
    # Participants par type
    participants_by_type = {}
    for p in Participant.query.all():
        participants_by_type[p.profile_type] = participants_by_type.get(p.profile_type, 0) + 1
    
    # Participants par pays
    participants_by_country = {}
    for p in Participant.query.all():
        participants_by_country[p.country] = participants_by_country.get(p.country, 0) + 1
    
    # Inscriptions par mois (6 derniers mois)
    from datetime import datetime, timedelta
    registrations_by_month = {}
    for i in range(6):
        month_date = datetime.now() - timedelta(days=30*i)
        month_key = month_date.strftime('%Y-%m')
        count = Participant.query.filter(
            db.extract('year', Participant.created_at) == month_date.year,
            db.extract('month', Participant.created_at) == month_date.month
        ).count()
        registrations_by_month[month_key] = count
    
    # Partenaires par catégorie
    partners_by_category = {}
    for p in Partner.query.all():
        partners_by_category[p.category] = partners_by_category.get(p.category, 0) + 1
    
    # Messages non lus
    unread_messages = Contact.query.filter_by(is_read=False).count()
    
    # Téléchargements totaux
    total_downloads = sum(p.download_count for p in Publication.query.all())
    
    # Inscriptions cette semaine
    week_ago = datetime.now() - timedelta(days=7)
    weekly_registrations = Participant.query.filter(Participant.created_at >= week_ago).count()
    
    return render_template('admin/statistics.html',
                         total_participants=total_participants,
                         total_speakers=total_speakers,
                         total_partners=total_partners,
                         total_news=total_news,
                         total_publications=total_publications,
                         participants_by_type=participants_by_type,
                         participants_by_country=participants_by_country,
                         registrations_by_month=registrations_by_month,
                         partners_by_category=partners_by_category,
                         unread_messages=unread_messages,
                         total_downloads=total_downloads,
                         weekly_registrations=weekly_registrations)

@bp.route('/statistics/<int:id>/update', methods=['POST'])
def update_statistic(id):
    """Mettre à jour une statistique"""
    statistic = Statistic.query.get_or_404(id)
    value = request.form.get('value', type=int)
    statistic.metric_value = value
    db.session.commit()
    flash('Statistique mise à jour avec succès.', 'success')
    return redirect(url_for('admin.statistics'))
