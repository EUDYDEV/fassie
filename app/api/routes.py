from flask import jsonify, request
from app.api import bp
from app.models import Participant, Speaker, Partner, News, Edition

@bp.route('/stats')
def api_stats():
    """API pour les statistiques"""
    from app.models import Statistic
    stats = Statistic.query.all()
    return jsonify({s.metric_name: s.metric_value for s in stats})

@bp.route('/speakers')
def api_speakers():
    """API pour les intervenants"""
    speakers = Speaker.query.all()
    data = [{
        'id': s.id,
        'name': s.full_name,
        'position': s.position,
        'organization': s.organization,
        'photo': s.photo
    } for s in speakers]
    return jsonify(data)

@bp.route('/partners')
def api_partners():
    """API pour les partenaires"""
    partners = Partner.query.filter_by(is_active=True).all()
    data = [{
        'id': p.id,
        'name': p.name,
        'logo': p.logo,
        'category': p.category,
        'website': p.website
    } for p in partners]
    return jsonify(data)

@bp.route('/news')
def api_news():
    """API pour les actualités"""
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(is_published=True).order_by(
        News.published_at.desc()
    ).paginate(page=page, per_page=10)
    data = [{
        'id': n.id,
        'title': n.title,
        'slug': n.slug,
        'excerpt': n.excerpt,
        'category': n.category,
        'featured_image': n.featured_image,
        'published_at': n.published_at.isoformat() if n.published_at else None
    } for n in news.items]
    return jsonify({
        'items': data,
        'total': news.total,
        'pages': news.pages,
        'current_page': news.page
    })

@bp.route('/editions')
def api_editions():
    """API pour les éditions"""
    editions = Edition.query.all()
    data = [{
        'id': e.id,
        'year': e.year,
        'theme': e.theme,
        'start_date': e.start_date.isoformat() if e.start_date else None,
        'end_date': e.end_date.isoformat() if e.end_date else None,
        'venue': e.venue,
        'city': e.city,
        'country': e.country
    } for e in editions]
    return jsonify(data)
