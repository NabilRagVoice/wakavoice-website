# =============================================================================
# BLUEPRINT: BENCHMARK - Tarifs et Comparaison
# =============================================================================

from flask import Blueprint, render_template

benchmark_bp = Blueprint('benchmark', __name__, template_folder='../templates/benchmark')


@benchmark_bp.route('/')
def index():
    """Page des tarifs et comparatifs"""
    return render_template('benchmark/index.html')
