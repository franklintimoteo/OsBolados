SELECT name, printf("%,d", sum(amount)), min(level), max(level), max(level)-min(level)
    FROM Experience
    INNER JOIN player ON experience.player = player.id
    WHERE date >= date('now', 'start of month')
    GROUP BY player
    ORDER BY sum(amount) DESC;
