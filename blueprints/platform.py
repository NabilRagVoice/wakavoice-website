# =============================================================================
# BLUEPRINT: PLATFORM - Présentation de la Plateforme
# =============================================================================

from flask import Blueprint, render_template

platform_bp = Blueprint('platform', __name__, template_folder='../templates/platform')


@platform_bp.route('/')
def index():
    """Page principale de la plateforme"""
    return render_template('platform/index.html')
