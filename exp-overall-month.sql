SELECT date, name, amount, level
    FROM Experience
    INNER JOIN player ON experience.player = player.id
    WHERE date >= date('now', 'start of month', '-1 month')
    ORDER BY name ASC;

