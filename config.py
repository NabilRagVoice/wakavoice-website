# =============================================================================
# WAKA COM WEBSITE - Configuration
# =============================================================================
# Configuration centralisée pour l'application Flask
# =============================================================================

import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'waka-voice-secret-key-2025'
    
    # Azure Cosmos DB
    COSMOS_ENDPOINT = os.environ.get('COSMOS_ENDPOINT', '')
    COSMOS_KEY = os.environ.get('COSMOS_KEY', '')
    COSMOS_DATABASE = os.environ.get('COSMOS_DATABASE', 'WakaVoiceWebsite')
    
    # Containers Cosmos DB
    COSMOS_CONTAINER_DEMOS = 'demo_requests'
    COSMOS_CONTAINER_BLOG = 'blog_articles'
    COSMOS_CONTAINER_CONTACTS = 'contacts'
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    
    # Langues supportées
    LANGUAGES = ['fr', 'en', 'es']
    DEFAULT_LANGUAGE = 'fr'


class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configuration de test"""
    DEBUG = True
    TESTING = True


# Sélection de la configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
