# =============================================================================
# BLUEPRINT: HOME - Page d'Accueil
# =============================================================================

from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, template_folder='../templates/home')


@home_bp.route('/')
def index():
    """Page d'accueil principale"""
    return render_template('home/index.html')


@home_bp.route('/a-propos')
def about():
    """Page À propos"""
    
    team = [
        {
            'name': 'Équipe Fondatrice',
            'role': 'Direction',
            'description': 'Experts en IA conversationnelle et télécommunications.',
            'icon': 'bi-people'
        },
        {
            'name': 'Ingénierie IA',
            'role': 'Développement',
            'description': 'Spécialistes des modèles de langage et voix.',
            'icon': 'bi-cpu'
        },
        {
            'name': 'Service Client',
            'role': 'Support',
            'description': 'Accompagnement personnalisé pour chaque projet.',
            'icon': 'bi-headset'
        }
    ]
    
    return render_template('home/about.html', team=team)
