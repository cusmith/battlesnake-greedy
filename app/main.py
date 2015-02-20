import bottle
import json


SNAKE_NAME = 'snaken'
SNAKE_TAUNT = 'I will find you, and I will kill you...'
SNAKE_COLOUR = '#FE2EF7'
SNAKE_HEAD_URL = 'http://battlesnake-snaken.herokuapp.com'

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

    print 'watafuq'

    return json.dumps({
        'name': SNAKE_NAME,
        'color': SNAKE_COLOUR,
        'head_url': SNAKE_HEAD_URL,
        'taunt': SNAKE_TAUNT
    })


@bottle.post('/move')
def move():
    data = bottle.request.json

    board_width = len(data['board'])
    board_height = len(data['board'][0])

    for snake in data['snakes']:
        if snake['name'] == SNAKE_NAME:
            head = snake['coords'][0]
    print "Head: " + str(head)

    smallest = 999
    target = [0, 0]
    for food in data['food']:
        x_dis = abs(food[0] - head[0])
        y_dis = abs(food[1] - head[1])
        distance = x_dis + y_dis
        if distance < smallest:
            smallest = distance
            target = food

    print 'Target: ' + str(target)

    move = None
    if target[1] < head[1]:
        print 'Try up'
        if data['board'][head[0]][head[1]-1]['state'] == 'empty':
            move = 'up'
            print 'Succeed up'
    if target[1] > head[1]:
        print 'Try down'
        if data['board'][head[0]][head[1]+1]['state'] == 'empty':
            move = 'down'
            print 'Succeed down'
    if target[0] < head[0]:
        print 'Try left'
        if data['board'][head[0]-1][head[1]]['state'] == 'empty':
            move = 'left'
            print 'Succeed left'
    if target[0] > head[0]:
        print 'Try right'
        if data['board'][head[0]+1][head[1]]['state'] == 'empty':
            move = 'right'
            print 'Succeed right'

    if not move:
        if data['board'][head[0]][head[1]-1]['state'] == 'empty':
            move = 'up'
            print 'Fallback up'
        if data['board'][head[0]][head[1]+1]['state'] == 'empty':
            move = 'down'
            print 'Fallback up'
        if data['board'][head[0]-1][head[1]]['state'] == 'empty':
            move = 'left'
            print 'Fallback up'
        if data['board'][head[0]+1][head[1]]['state'] == 'empty':
            move = 'right'
            print 'Fallback up'
    print move
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
