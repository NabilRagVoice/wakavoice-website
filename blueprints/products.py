# =============================================================================
# BLUEPRINT: PRODUCTS - Services du Centre d'Appel IA
# =============================================================================

from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='../templates/products')


# =============================================================================
# SERVICES DISPONIBLES
# =============================================================================

SERVICES = {
    'service_client': {
        'title': 'Service Client & Support',
        'description': 'Agents IA disponibles 24/7 pour répondre aux questions et résoudre les problèmes.',
        'icon': 'bi-headset',
        'features': [
            'Réponses instantanées',
            'Gestion des réclamations',
            'Escalade intelligente',
            'FAQ dynamique'
        ]
    },
    'televente': {
        'title': 'Télévente & Prospection',
        'description': 'Campagnes d\'appels sortants pour générer des leads et conclure des ventes.',
        'icon': 'bi-cart-check',
        'features': [
            'Scripts personnalisables',
            'Qualification automatique',
            'Gestion des objections',
            'Intégration CRM'
        ]
    },
    'prise_rdv': {
        'title': 'Prise de Rendez-vous',
        'description': 'Gestion complète des agendas : prise, modification, annulation et rappels.',
        'icon': 'bi-calendar-check',
        'features': [
            'Synchronisation calendrier',
            'Rappels automatiques',
            'Self-service client',
            'Confirmations multicanaux'
        ]
    },
    'enquetes': {
        'title': 'Enquêtes & Sondages',
        'description': 'Collecte de données qualitatives et quantitatives automatisée.',
        'icon': 'bi-clipboard-data',
        'features': [
            'Questionnaires personnalisés',
            'NPS, CSAT, CES',
            'Analyse de sentiment',
            'Rapports automatiques'
        ]
    }
}

# Canaux de communication
CHANNELS = [
    {'id': 'telephone', 'name': 'Téléphone', 'icon': 'bi-telephone-fill', 'description': 'Appels entrants et sortants'},
    {'id': 'sms', 'name': 'SMS', 'icon': 'bi-chat-dots-fill', 'description': 'Messages courts et ciblés'},
    {'id': 'whatsapp', 'name': 'WhatsApp', 'icon': 'bi-whatsapp', 'description': 'Conversations riches'},
    {'id': 'email', 'name': 'Email', 'icon': 'bi-envelope-fill', 'description': 'Communications formelles'},
    {'id': 'social', 'name': 'Réseaux Sociaux', 'icon': 'bi-share-fill', 'description': 'Facebook, Instagram, X'},
    {'id': 'webchat', 'name': 'Webchat', 'icon': 'bi-globe', 'description': 'Widget sur votre site'}
]


# =============================================================================
# ROUTES
# =============================================================================

@products_bp.route('/')
def index():
    """Page principale des services"""
    return render_template(
        'products/index.html',
        services=SERVICES,
        channels=CHANNELS
    )
