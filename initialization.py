# =============================================================================
# WAKA COM WEBSITE - Initialisation des Ressources
# =============================================================================
# Gestion des connexions Azure Cosmos DB et autres services
# =============================================================================

import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from config import Config

# =============================================================================
# COSMOS DB CLIENT
# =============================================================================

_cosmos_client = None
_database = None
_containers = {}


def get_cosmos_client():
    """Retourne le client Cosmos DB (singleton)"""
    global _cosmos_client
    
    if _cosmos_client is None:
        endpoint = Config.COSMOS_ENDPOINT
        key = Config.COSMOS_KEY
        
        if endpoint and key:
            try:
                _cosmos_client = CosmosClient(endpoint, key)
                print("✅ Cosmos DB Client initialisé")
            except Exception as e:
                print(f"⚠️ Erreur connexion Cosmos DB: {e}")
                _cosmos_client = None
        else:
            print("⚠️ Cosmos DB non configuré (variables d'environnement manquantes)")
    
    return _cosmos_client


def get_database():
    """Retourne la base de données Cosmos DB"""
    global _database
    
    if _database is None:
        client = get_cosmos_client()
        if client:
            try:
                _database = client.create_database_if_not_exists(
                    id=Config.COSMOS_DATABASE
                )
                print(f"✅ Database '{Config.COSMOS_DATABASE}' prête")
            except Exception as e:
                print(f"⚠️ Erreur database: {e}")
    
    return _database


def get_container(container_name: str):
    """Retourne un container Cosmos DB (avec cache)"""
    global _containers
    
    if container_name not in _containers:
        database = get_database()
        if database:
            try:
                _containers[container_name] = database.create_container_if_not_exists(
                    id=container_name,
                    partition_key=PartitionKey(path="/id"),
                    offer_throughput=400
                )
                print(f"✅ Container '{container_name}' prêt")
            except Exception as e:
                print(f"⚠️ Erreur container {container_name}: {e}")
                return None
    
    return _containers.get(container_name)


# =============================================================================
# FONCTIONS UTILITAIRES COSMOS DB
# =============================================================================

def save_demo_request(data: dict) -> bool:
    """Sauvegarde une demande de démo"""
    container = get_container(Config.COSMOS_CONTAINER_DEMOS)
    if container:
        try:
            container.create_item(body=data)
            return True
        except Exception as e:
            print(f"Erreur sauvegarde démo: {e}")
    return False


def get_blog_articles(limit: int = 10):
    """Récupère les articles de blog"""
    container = get_container(Config.COSMOS_CONTAINER_BLOG)
    if container:
        try:
            query = "SELECT * FROM c WHERE c.published = true ORDER BY c.published_at DESC"
            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True,
                max_item_count=limit
            ))
            return items
        except Exception as e:
            print(f"Erreur récupération blog: {e}")
    return []


def get_blog_article(article_id: str):
    """Récupère un article de blog par ID"""
    container = get_container(Config.COSMOS_CONTAINER_BLOG)
    if container:
        try:
            item = container.read_item(item=article_id, partition_key=article_id)
            return item
        except exceptions.CosmosResourceNotFoundError:
            return None
        except Exception as e:
            print(f"Erreur récupération article: {e}")
    return None


def save_contact(data: dict) -> bool:
    """Sauvegarde un contact"""
    container = get_container(Config.COSMOS_CONTAINER_CONTACTS)
    if container:
        try:
            container.create_item(body=data)
            return True
        except Exception as e:
            print(f"Erreur sauvegarde contact: {e}")
    return False


# =============================================================================
# INITIALISATION AU DÉMARRAGE
# =============================================================================

def init_resources():
    """Initialise toutes les ressources au démarrage de l'application"""
    print("\n" + "="*60)
    print("🚀 INITIALISATION DES RESSOURCES WAKA COM")
    print("="*60)
    
    # Cosmos DB
    get_cosmos_client()
    get_database()
    
    # Pré-création des containers
    containers = [
        Config.COSMOS_CONTAINER_DEMOS,
        Config.COSMOS_CONTAINER_BLOG,
        Config.COSMOS_CONTAINER_CONTACTS
    ]
    
    for container_name in containers:
        get_container(container_name)
    
    print("="*60 + "\n")


# Mode simulation si Cosmos DB non configuré
class MockContainer:
    """Container simulé pour le développement sans Azure"""
    
    def __init__(self, name):
        self.name = name
        self._items = []
    
    def create_item(self, body):
        self._items.append(body)
        print(f"📝 [MOCK] Item sauvegardé dans {self.name}")
        return body
    
    def query_items(self, **kwargs):
        return iter(self._items)
    
    def read_item(self, item, partition_key):
        for i in self._items:
            if i.get('id') == item:
                return i
        raise exceptions.CosmosResourceNotFoundError()


def get_mock_container(name):
    """Retourne un container simulé"""
    if name not in _containers:
        _containers[name] = MockContainer(name)
    return _containers[name]
