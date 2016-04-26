_world = {}
starting_position = (0, 0)

def load_tiles(): #adds a dictionary & parses the map text file
    """Parses a file that describes the world space into the _world object"""
    with open('resources/map.txt', 'r') as f:
        rows = f.readlines()
    x_max = len(rows[0].split('\t')) #assumes all rows contain the same number of tabs
    for y in range(len(rows)):
        cols = rows[y].split('\t')
        for x in range(x_max):
            tile_name = cols[x].replace('\n', '') #windows - replace \r\n
            if tile_name == 'StartingRoom':
                global starting_position
                starting_position = (x, y)
            _world[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)

def tile_exists(x, y): #returns tile at given coordinates or None if there's no tile there
    return _world.get((x, y))
