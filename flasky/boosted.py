from flask import (Blueprint, render_template)
from flasky.db import get_db

bp = Blueprint('boosted', __name__, url_prefix='/boosted-history')

@bp.route('/')
def boosted_history():
    db = get_db()

    creatures_boosted = db.execute("""
    select STRFTIME('%d/%m/%Y', date), name from boostedcreature
    order by date desc;
    """)

    return render_template('boosted.html',
                           creatures=creatures_boosted)
