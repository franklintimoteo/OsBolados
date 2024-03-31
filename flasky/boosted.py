from flask import (Blueprint, render_template)
from flasky.db import get_db
from json import load

bp = Blueprint('boosted', __name__, url_prefix='/boosted-history')

@bp.route('/')
def boosted_history():
    db = get_db()

    creatures_boosted = db.execute("""
    select STRFTIME('%d/%m/%Y', date), GROUP_CONCAT(name) from boostedcreature
    group by date
    order by date,isBoss desc limit 30;
    """)

    creatures_boosted = [(date, *monster.split(',')) for date, monster in creatures_boosted]

    with open('/tmp/boosted-bosses.json') as file:
        bosses_today = load(file)
        
    return render_template('boosted.html',
                           creatures=creatures_boosted, bosses=bosses_today)
