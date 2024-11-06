from flask import (Blueprint, render_template, request, redirect, abort)
from markupsafe import escape
from flasky.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def character_arg():
    character = request.args.get('character')
    if character:
        character = character.title()
        return redirect(f'/user/{character}')
    abort(404)

@bp.route('/<character>')
def character(character):
    character = escape(character)

    db = get_db()
    outfit = db.execute(f"""select outfit from player where name='{character}' COLLATE NOCASE""").fetchone()
    outfit = outfit[0]
    player_id = db.execute(f"""select id from player where name='{character}'""").fetchone()

    exp_total = db.execute(f"""
    select printf("%,d", sum(amount)), min(level), max(level), max(level)-min(level)
    from experience
    inner join player on experience.player = player.id
    where name='{character}' COLLATE NOCASE
    """).fetchone()

    exp_month = db.execute(f"""
    select printf("%,d", sum(amount)), min(level), max(level), max(level)-min(level)
    from experience
    inner join player on experience.player = player.id
    where name='{character}' COLLATE NOCASE and
    date >= date('now', 'start of month')

    """).fetchone()

    history_exp = db.execute(f"""
    select STRFTIME('%d/%m/%Y', date), level, amount from Experience
    inner join Player on Experience.player = Player.id
    where name='{character}' COLLATE NOCASE order by date desc;
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

    achievements_obtained = db.execute(f"""
    select points, name, description, link from Achievement_Player as A
    inner join Achievement on Achievement.id = A.achievement
    where player='{player_id[0]}';""")

    
    achievements_pendent = db.execute(f"""
    select points, name, description,link from Achievement as A
    left join Achievement_Player as B on A.id = B.achievement
    and player={player_id[0]}
    where B.achievement is null
    """)
    
    total_achievements = db.execute(f"""
    select sum(points) from Achievement_Player as A
    inner join Achievement on Achievement.id = A.achievement
    where player={player_id[0]};    
    """).fetchone()[0]

    
    return render_template('user.html',
                           outfit=outfit,
                           name=character,
                           exp_total=exp_total,
                           exp_month=exp_month,
                           history_exp=history_exp,
                           deaths=deaths,
                           achievob=achievements_obtained,
                           achievpd=achievements_pendent,
                           achievtotal=total_achievements)
