from flask import (Blueprint, g, render_template, url_for)
from flasky.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/exp-geral/')
def exp_geral():
    db = get_db()

    results = db.execute("""
    select name, sum(amount), min(level), max(level), max(level)-min(level)
    from Experience
    inner join player on experience.player = player.id
    where date >= date('now', 'start of month')
    group by player
    order by sum(amount) desc
    """)

    return render_template('exp-geral.html', data=results)


@bp.route('/')
def index():
    return render_template('index.html')
