import bottle
import json


SNAKE_NAME = 'Liam Neeson'
SNAKE_COLOUR = '#FE2EF7'
SNAKE_HEAD_URL = 'http://cdn.movieweb.com/img.news/NE8T7skxguIwbe_1_1.jpg'

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
        'taunt': None
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
        if data['board'][head[0]][head[1]-1]['state'] in GOOD_STUFF and head[1] != 0:
            move = 'up'
        if data['board'][head[0]][head[1]+1]['state'] in GOOD_STUFF and head[1] != len(data['board'][0]):
            move = 'down'
        if data['board'][head[0]-1][head[1]]['state'] in GOOD_STUFF and head[0] != 0:
            move = 'left'
        if data['board'][head[0]+1][head[1]]['state'] in GOOD_STUFF and head[1] != len(data['board']):
            move = 'right'

    taunt = None
    if data['turn'] % 100 == 10:
        taunt = 'I dont know who you are. I dont know what you want.'
    if data['turn'] % 100 == 20:
        taunt = 'If you are looking for ransom, I can tell you I dont have money.'
    if data['turn'] % 100 == 30:
        taunt = 'But what I do have are a very particular set of skills, skills I have acquired over a very long career.'
    if data['turn'] % 100 == 40:
        taunt = 'Skills that make me a nightmare for snakes like you.'
    if data['turn'] % 100 == 50:
        taunt = 'If you let my daughter go now, thatll be the end of it.'
    if data['turn'] % 100 == 60:
        taunt = 'I will not look for you, I will not pursue you.'
    if data['turn'] % 100 == 70:
        taunt = 'But if you dont, I will look for you, I will find you, and I will kill you.'

    return json.dumps({
        'move': move,
        'taunt': taunt
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
