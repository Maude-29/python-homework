"""T1 – Snake procédural : le code de départ (étape 1).

D'après le TP « Snake » de Thierry Parmentelat et Aurélien Noce
(github.com/flotpython/exos-python), réécrit pour le cours AP Python.

Lancez-le avec :  uv run snake.py
Testez-le avec :  uv run pytest
"""

from random import randint

import pygame as pg

# Le plateau : X × Y cases de W × H pixels (étape 3).
X, Y = 30, 30
W, H = 20, 20

UP, DOWN, LEFT, RIGHT = (0, -1), (0, +1), (-1, 0), (+1, 0)


# --- logique du jeu : aucune fonction ici ne dessine -------------------------
# Ces fonctions sont vérifiées par les tests (tests/test_snake.py) :
# gardez leur nom et leurs paramètres.


def in_scope(snake, tile):
    """Vrai si la case `tile` = (x, y) est sur le plateau."""
    x, y = tile
    return ( (0 <= x < X) and (0 <= y < Y) )
    # append modifie la liste sur place, et renvoie None

def next_head(snake, direction):
    """La case où arrive la tête (le dernier élément de `snake`)."""
    x, y = snake[-1] 
    dx, dy = direction 
    return (x + dx, y + dy)

def turn(direction, key):
    """La nouvelle direction après l'appui sur la touche `key` (ex. pg.K_UP)."""
    KEYS = {pg.K_UP: UP, pg.K_DOWN: DOWN,
            pg.K_LEFT: LEFT, pg.K_RIGHT: RIGHT}
    return KEYS.get(key, direction)
    # deuxième argument = valeur par défaut 


def move(snake, direction, fruit):
    """Avance le serpent d'une case, en modifiant la liste `snake` sur place.

    Renvoie ce qui s'est passé : "ate", "moved", "self-bite" ou "out-of-board".
    """
    new_head = next_head(snake, direction)

    if not in_scope(snake, new_head):
        return "out-of-board"
    if new_head in snake:
        return "self-bite"

    snake.append(new_head)
    if new_head == fruit:
        return "ate"

    snake.pop(0) # on retire sa queue 
    return "moved"
    
def random_fruit(snake):
    """Une case libre du plateau, tirée au hasard."""
    case = (randint(0, X - 1), randint(0, Y - 1)) # initialisation
    while case in snake:
        case = (randint(0, X - 1), randint(0, Y - 1)) # s'assurer que la case n'est pas sur le serpent
    return case 

# --- la boucle de jeu --------------------------------------------------------

def draw_tile(screen, tile, color):
    x, y = tile
    rect = pg.Rect(x*W, y*H, W, H)
    pg.draw.rect(screen, color, rect)

def draw(screen, snake, fruit): 
    for x in range(X):
        for y in range(Y):
            if (x + y) % 2:
                draw_tile(screen, (x, y), (0, 0, 0))
    for tile in snake:
        draw_tile(screen, tile, (0,255,0))
    draw_tile(screen, fruit, (255, 0, 0))

def main():
    running = True
    pg.init()
    screen = pg.display.set_mode((X * W, Y * H))
    clock = pg.time.Clock()

    snake=[(10,15), (11,15), (12,15)]
    direction = RIGHT
    fruit = random_fruit(snake)

    # while True:
    while running:
        # au plus 1 image par seconde
        clock.tick(1)

        # 1. les événements : il faut les lire, sinon la fenêtre ne répond pas
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False 
                direction = turn(direction, event.key)
            
            # pass

        # 2. l'état (rien pour l'instant)
        result = move(snake, direction, fruit)
        if result == "ate":
            fruit = random_fruit(snake)
        elif result in ("self-bite", "out-of-board"):
            running = False   # partie perdue

        # 3. l'affichage : on prépare l'image en mémoire...
        screen.fill((255,255,255))
        draw(screen, snake, fruit)

        pg.display.update()
        # ... puis on l'envoie à l'écran, une seule fois par tour de boucle
    pg.quit()


# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run snake.py),
# pas quand un autre fichier fait `import snake` (les tests, par ex.).
if __name__ == "__main__":
    main()
