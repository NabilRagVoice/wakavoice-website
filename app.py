# =============================================================================
# WAKA COM WEBSITE - Application Principale
# =============================================================================
# Site vitrine multipage pour la plateforme Waka Com
# Framework: Flask avec Blueprints
# =============================================================================

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

# Import des configurations
from config import config

# Import des Blueprints
from blueprints.home import home_bp
from blueprints.products import products_bp
from blueprints.demo import demo_bp
from blueprints.platform import platform_bp
from blueprints.benchmark import benchmark_bp
from blueprints.blog import blog_bp

# =============================================================================
# CRÉATION DE L'APPLICATION
# =============================================================================

def create_app(config_name='default'):
    """Factory function pour créer l'application Flask"""
    
    app = Flask(__name__)
    
    # Chargement de la configuration
    app.config.from_object(config[config_name])
    
    # ==========================================================================
    # ENREGISTREMENT DES BLUEPRINTS
    # ==========================================================================
    
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(products_bp, url_prefix='/produits')
    app.register_blueprint(demo_bp, url_prefix='/demo')
    app.register_blueprint(platform_bp, url_prefix='/plateforme')
    app.register_blueprint(benchmark_bp, url_prefix='/benchmark')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    
    # ==========================================================================
    # CONTEXT PROCESSORS
    # ==========================================================================
    
    @app.context_processor
    def inject_globals():
        """Variables globales disponibles dans tous les templates"""
        return {
            'current_year': datetime.now().year,
            'company_name': 'Waka Com',
            'site_name': 'Waka Com',
            'site_tagline': 'Centre de Contact Multicanal 100% IA',
            'current_lang': session.get('lang', 'fr')
        }
    
    # ==========================================================================
    # GESTION DES LANGUES
    # ==========================================================================
    
    @app.route('/set-language/<lang>')
    def set_language(lang):
        """Change la langue de l'interface"""
        if lang in app.config.get('LANGUAGES', ['fr', 'en']):
            session['lang'] = lang
        return redirect(request.referrer or url_for('home.index'))
    
    # ==========================================================================
    # GESTIONNAIRES D'ERREURS
    # ==========================================================================
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500
    
    # ==========================================================================
    # INITIALISATION DES RESSOURCES
    # ==========================================================================
    
    with app.app_context():
        try:
            from initialization import init_resources
            init_resources()
        except Exception as e:
            print(f"⚠️ Initialisation partielle: {e}")
    
    return app


# =============================================================================
# POINT D'ENTRÉE
# =============================================================================

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
