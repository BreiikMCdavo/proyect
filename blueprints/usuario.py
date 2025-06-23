from flask import Blueprint, render_template
from utils.decorators import usuario_required


usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('/')
@usuario_required
def dashboard():
    return render_template('usuario/welcome.html')
