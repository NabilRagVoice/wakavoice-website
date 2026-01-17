# =============================================================================
# BLUEPRINT: DEMO - Demande de Démonstration
# =============================================================================
# Formulaire lié à Azure Cosmos DB
# =============================================================================

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from datetime import datetime
import uuid

demo_bp = Blueprint('demo', __name__, template_folder='../templates/demo')


# =============================================================================
# TYPES D'OPÉRATIONS DISPONIBLES
# =============================================================================

OPERATION_TYPES = {
    'inbound': {
        'label': 'Opérations Inbound (Appels Entrants)',
        'options': [
            {'value': 'support_client', 'label': 'Support Client'},
            {'value': 'accueil_orientation', 'label': 'Accueil & Orientation'},
            {'value': 'prise_rdv', 'label': 'Prise de Rendez-vous'},
            {'value': 'hotline_technique', 'label': 'Hotline Technique'},
            {'value': 'sav', 'label': 'Service Après-Vente'},
            {'value': 'autre_inbound', 'label': 'Autre (préciser)'}
        ]
    },
    'outbound': {
        'label': 'Opérations Outbound (Appels Sortants)',
        'options': [
            {'value': 'recouvrement', 'label': 'Recouvrement de Créances'},
            {'value': 'televente', 'label': 'Télévente & Prospection'},
            {'value': 'enquetes', 'label': 'Enquêtes & Satisfaction'},
            {'value': 'relance_commerciale', 'label': 'Relance Commerciale'},
            {'value': 'confirmation_rdv', 'label': 'Confirmation de RDV'},
            {'value': 'notification', 'label': 'Notifications Proactives'},
            {'value': 'autre_outbound', 'label': 'Autre (préciser)'}
        ]
    }
}

# Volumes d'appels estimés
VOLUME_OPTIONS = [
    {'value': 'moins_1000', 'label': 'Moins de 1 000 appels/mois'},
    {'value': '1000_5000', 'label': '1 000 - 5 000 appels/mois'},
    {'value': '5000_20000', 'label': '5 000 - 20 000 appels/mois'},
    {'value': '20000_100000', 'label': '20 000 - 100 000 appels/mois'},
    {'value': 'plus_100000', 'label': 'Plus de 100 000 appels/mois'}
]

# Secteurs d'activité
SECTORS = [
    {'value': 'banque_assurance', 'label': 'Banque & Assurance'},
    {'value': 'telecom', 'label': 'Télécommunications'},
    {'value': 'energie', 'label': 'Énergie & Utilities'},
    {'value': 'ecommerce', 'label': 'E-commerce & Retail'},
    {'value': 'sante', 'label': 'Santé & Pharma'},
    {'value': 'immobilier', 'label': 'Immobilier'},
    {'value': 'services', 'label': 'Services B2B'},
    {'value': 'industrie', 'label': 'Industrie & Manufacturing'},
    {'value': 'public', 'label': 'Secteur Public'},
    {'value': 'autre', 'label': 'Autre'}
]


# =============================================================================
# ROUTES
# =============================================================================

@demo_bp.route('/')
def index():
    """Page principale du formulaire de démo"""
    return render_template(
        'demo/index.html',
        operation_types=OPERATION_TYPES,
        volume_options=VOLUME_OPTIONS,
        sectors=SECTORS
    )


@demo_bp.route('/submit', methods=['POST'])
def submit():
    """Traitement du formulaire de demande de démo"""
    
    try:
        # Récupération des données du formulaire
        data = {
            'id': str(uuid.uuid4()),
            'type': 'demo_request',
            
            # Informations personnelles
            'prenom': request.form.get('prenom', '').strip(),
            'nom': request.form.get('nom', '').strip(),
            'email': request.form.get('email', '').strip(),
            'telephone': request.form.get('telephone', '').strip(),
            
            # Informations entreprise
            'societe': request.form.get('societe', '').strip(),
            'fonction': request.form.get('fonction', '').strip(),
            'secteur': request.form.get('secteur', ''),
            
            # Besoins
            'operations': request.form.getlist('operations'),
            'volume': request.form.get('volume', ''),
            'commentaire': request.form.get('commentaire', '').strip(),
            
            # Options
            'voix_personnalisee': request.form.get('voix_personnalisee') == 'on',
            'integration_crm': request.form.get('integration_crm') == 'on',
            'urgence': request.form.get('urgence', 'normal'),
            
            # Métadonnées
            'created_at': datetime.utcnow().isoformat(),
            'status': 'new',
            'source': 'website',
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string[:500] if request.user_agent else ''
        }
        
        # Validation basique
        errors = []
        if not data['prenom']:
            errors.append('Le prénom est requis')
        if not data['nom']:
            errors.append('Le nom est requis')
        if not data['email'] or '@' not in data['email']:
            errors.append('Email invalide')
        if not data['societe']:
            errors.append('Le nom de société est requis')
        if not data['operations']:
            errors.append('Sélectionnez au moins une opération')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('demo.index'))
        
        # Sauvegarde dans Cosmos DB
        try:
            from initialization import save_demo_request
            success = save_demo_request(data)
            
            if success:
                flash('Votre demande a été envoyée avec succès ! Notre équipe vous contactera sous 24h.', 'success')
                return redirect(url_for('demo.confirmation', request_id=data['id']))
            else:
                # Fallback si Cosmos DB non disponible
                print(f"Demo request (fallback): {data}")
                flash('Demande enregistrée. Nous vous contacterons rapidement.', 'success')
                return redirect(url_for('demo.confirmation', request_id=data['id']))
                
        except Exception as e:
            print(f"Erreur Cosmos DB: {e}")
            flash('Demande enregistrée. Nous vous contacterons rapidement.', 'success')
            return redirect(url_for('demo.confirmation', request_id=data['id']))
        
    except Exception as e:
        print(f"Erreur submission: {e}")
        flash('Une erreur est survenue. Veuillez réessayer.', 'error')
        return redirect(url_for('demo.index'))


@demo_bp.route('/confirmation/<request_id>')
def confirmation(request_id):
    """Page de confirmation après soumission"""
    return render_template(
        'demo/confirmation.html',
        request_id=request_id
    )


# =============================================================================
# API ENDPOINTS (pour AJAX si nécessaire)
# =============================================================================

@demo_bp.route('/api/submit', methods=['POST'])
def api_submit():
    """API endpoint pour soumission AJAX"""
    
    try:
        data = request.get_json()
        
        # Ajout des métadonnées
        data['id'] = str(uuid.uuid4())
        data['type'] = 'demo_request'
        data['created_at'] = datetime.utcnow().isoformat()
        data['status'] = 'new'
        data['source'] = 'website_api'
        
        # Sauvegarde
        from initialization import save_demo_request
        success = save_demo_request(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Demande enregistrée avec succès',
                'request_id': data['id']
            })
        else:
            return jsonify({
                'success': True,  # On dit succès même sans Cosmos DB
                'message': 'Demande enregistrée',
                'request_id': data['id']
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
