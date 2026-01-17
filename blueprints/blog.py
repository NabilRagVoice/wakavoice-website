# =============================================================================
# BLUEPRINT: BLOG - Actualités & Articles
# =============================================================================

from flask import Blueprint, render_template, abort

blog_bp = Blueprint('blog', __name__, template_folder='../templates/blog')


# =============================================================================
# ARTICLES DE DÉMONSTRATION
# =============================================================================

ARTICLES = [
    {
        'id': 'article-001',
        'slug': 'ia-conversationnelle-2026',
        'title': 'L\'IA Conversationnelle en 2026 : État des Lieux',
        'excerpt': 'Comment les centres de contact IA transforment la relation client et quelles sont les tendances à suivre cette année.',
        'category': 'Tendances',
        'read_time': 5
    },
    {
        'id': 'article-002',
        'slug': 'transition-centre-contact-ia',
        'title': 'Comment Réussir sa Transition vers un Centre de Contact IA',
        'excerpt': 'Les étapes clés pour passer d\'un centre de contact traditionnel à une solution 100% IA.',
        'category': 'Guide',
        'read_time': 8
    },
    {
        'id': 'article-003',
        'slug': 'retour-experience-waka-voice',
        'title': 'Retour d\'Expérience : 6 Mois avec Waka Com',
        'excerpt': 'Un directeur de service client partage son expérience et les résultats obtenus.',
        'category': 'Cas Client',
        'read_time': 6
    }
]


@blog_bp.route('/')
def index():
    """Liste des articles"""
    return render_template('blog/index.html', articles=ARTICLES)


@blog_bp.route('/<slug>')
def article(slug):
    """Affichage d'un article"""
    article = next((a for a in ARTICLES if a['slug'] == slug), None)
    if not article:
        abort(404)
    return render_template('blog/article.html', article=article)
