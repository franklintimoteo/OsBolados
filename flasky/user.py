from flask import (Blueprint, render_template, request, redirect, abort)
from markupsafe import escape
from flasky.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def character_arg():
    character = request.args.get('character')
    if character:
        return redirect(f'/user/{character}')
    abort(404)

@bp.route('/<character>')
def character(character):
    character = escape(character)

    db = get_db()
    exp_total = db.execute(f"""
    select sum(amount), min(level), max(level), max(level)-min(level)
    from experience
    inner join player on experience.player = player.id
    where name='{character}' COLLATE NOCASE
    """).fetchone()

    exp_month = db.execute(f"""
    select sum(amount), min(level), max(level), max(level)-min(level)
    from experience
    inner join player on experience.player = player.id
    where name='{character}' COLLATE NOCASE and
    date >= date('now', 'start of month')

    """).fetchone()

    history_exp = db.execute(f"""
    select STRFTIME('%d/%m/%Y, %H:%M', date), level, amount from Experience
    inner join Player on Experience.player = Player.id
    where name='{character}' COLLATE NOCASE order by level desc;
    """)

    deaths = db.execute(f"""
    select STRFTIME('%d/%m/%Y, %H:%M', time), level, group_concat(Monster.name)
    from Death
    inner join Player on Death.player = player.id
    inner join Death_monster on Death.id = Death_monster.death
    inner join Monster on Death_Monster.monster = Monster.id
    where player.name='{character}' COLLATE NOCASE
    group by Player,time
    order by death.level desc
    """)

    return render_template('user.html',
                           name=character,
                           exp_total=exp_total,
                           exp_month=exp_month,
                           history_exp=history_exp,
                           deaths=deaths)
