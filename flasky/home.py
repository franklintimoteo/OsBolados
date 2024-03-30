from flask import (Blueprint, g, render_template, url_for)
from flask import current_app
from os import listdir
from datetime import date
from flasky.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/exp-geral/')
def exp_geral():
    db = get_db()

#    results = db.execute("""
#    select name, printf("%,d", sum(amount)), min(level), max(level), max(level)-min(level)
#    from Experience
#    inner join player on experience.player = player.id
#    where date >= date('now', 'start of month')
#    group by player
#    order by sum(amount) desc
#    """)
    if date.today().day == 1 : 
        results = db.execute("""
        select name, REPLACE(printf("%,d", sum(amount)), ',', '.'), min(level), max(level), max(level)-min(level)
        from Experience
        inner join player on experience.player = player.id
        where date >= date('now', 'start of month', '-1 month')
        group by player
        order by sum(amount) desc
        """)
    else:
        results = db.execute("""
        select name, REPLACE(printf("%,d", sum(amount)), ',', '.'), min(level), max(level), max(level)-min(level)
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

@bp.route('/download-old-exp/')
def download_old_exp():
    files = listdir(current_app.static_folder+'/downloads-old-exp')

    return render_template('download-old-exp.html', files=files)
