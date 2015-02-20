import bottle
import json


SNAKE_NAME = 'snaken'
SNAKE_TAUNT = 'I will find you, and I will kill you...'
SNAKE_COLOUR = '#FE2EF7'
SNAKE_HEAD_URL = 'http://battlesnake-snaken.herokuapp.com'

GOOD_STUFF = ['food', 'empty']

@bottle.get('/')
def index():
    return """
        <a href="https://github.com/sendwithus/battlesnake-python">
            battlesnake-python
        </a>
    """


@bottle.post('/start')
def start():
    data = bottle.request.json

    return json.dumps({
        'name': SNAKE_NAME,
        'color': SNAKE_COLOUR,
        'head_url': SNAKE_HEAD_URL,
        'taunt': SNAKE_TAUNT
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    for snake in data['snakes']:
        if snake['name'] == SNAKE_NAME:
            head = snake['coords'][0]

    smallest = 999
    target = [0, 0]
    for food in data['food']:
        x_dis = abs(food[0] - head[0])
        y_dis = abs(food[1] - head[1])
        distance = x_dis + y_dis
        if distance < smallest:
            smallest = distance
            target = food

    move = None
    if target[1] < head[1]:
        if data['board'][head[0]][head[1]-1]['state'] in GOOD_STUFF:
            move = 'up'
    if target[1] > head[1]:
        if data['board'][head[0]][head[1]+1]['state'] in GOOD_STUFF:
            move = 'down'
    if target[0] < head[0]:
        if data['board'][head[0]-1][head[1]]['state'] in GOOD_STUFF:
            move = 'left'
    if target[0] > head[0]:
        if data['board'][head[0]+1][head[1]]['state'] in GOOD_STUFF:
            move = 'right'

    if not move:
        if data['board'][head[0]][head[1]-1]['state'] in GOOD_STUFF:
            move = 'up'
        if data['board'][head[0]][head[1]+1]['state'] in GOOD_STUFF:
            move = 'down'
        if data['board'][head[0]-1][head[1]]['state'] in GOOD_STUFF:
            move = 'left'
        if data['board'][head[0]+1][head[1]]['state'] in GOOD_STUFF:
            move = 'right'

    return json.dumps({
        'move': move,
        'taunt': SNAKE_TAUNT
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
