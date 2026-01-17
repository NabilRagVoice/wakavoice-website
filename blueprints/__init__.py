# =============================================================================
# BLUEPRINTS PACKAGE - Waka Com Website
# =============================================================================

from .home import home_bp
from .products import products_bp
from .demo import demo_bp
from .platform import platform_bp
from .benchmark import benchmark_bp
from .blog import blog_bp

__all__ = [
    'home_bp',
    'products_bp',
    'demo_bp',
    'platform_bp',
    'benchmark_bp',
    'blog_bp'
]
