class Beam:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self):
        if self.direction == "up":
            self.y -= 1
        elif self.direction == "down":
            self.y += 1
        elif self.direction == "left":
            self.x -= 1
        elif self.direction == "right":
            self.x += 1


class Tile:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.directions = set()
        self.symbol = symbol

    def add_direction(self, direction):
        self.directions.add(direction)


def read_input(filename):
    with open(filename) as f:
        return f.read().splitlines()


def prepare_input(input_list):
    tiles = []
    for y, line in enumerate(input_list):
        tiles_line = []
        for x, symbol in enumerate(line):
            tiles_line.append(Tile(x, y, symbol))
        tiles.append(tiles_line)
    return tiles


def show_tiles(tiles):
    for line in tiles:
        for tile in line:
            print(tile.symbol if len(tile.directions) == 0 else "#", end="")
        print()
    print()


def process_beam(beam, tiles):
    if beam.x < 0 or beam.y < 0:
        return None
    if beam.y >= len(tiles) or beam.x >= len(tiles[0]):
        return None
    current_tile = tiles[beam.y][beam.x]
    # Energize the tile
    if beam.direction in current_tile.directions:
        return None
    else:
        current_tile.add_direction(beam.direction)

    if current_tile.symbol == ".":
        beam.move()
        return beam
    elif current_tile.symbol == '|':
        if beam.direction == "up" or beam.direction == "down":
            beam.move()
            return beam
        else:
            beam_down = Beam(beam.x, beam.y + 1, "down")
            beam_up = Beam(beam.x, beam.y - 1, "up")
            return [beam_down, beam_up]
    elif current_tile.symbol == "-":
        if beam.direction == "left" or beam.direction == "right":
            beam.move()
            return beam
        else:
            beam_right = Beam(beam.x + 1, beam.y, "right")
            beam_left = Beam(beam.x - 1, beam.y, "left")
            return [beam_left, beam_right]
    elif current_tile.symbol == "/":
        if beam.direction == "up":
            return Beam(beam.x + 1, beam.y, "right")
        if beam.direction == "down":
            return Beam(beam.x - 1, beam.y, "left")
        if beam.direction == "left":
            return Beam(beam.x, beam.y + 1, "down")
        if beam.direction == "right":
            return Beam(beam.x, beam.y - 1, "up")
    elif current_tile.symbol == "\\":
        if beam.direction == "up":
            return Beam(beam.x - 1, beam.y, "left")
        if beam.direction == "down":
            return Beam(beam.x + 1, beam.y, "right")
        if beam.direction == "left":
            return Beam(beam.x, beam.y - 1, "up")
        if beam.direction == "right":
            return Beam(beam.x, beam.y + 1, "down")

    return None


def start_cycle(first_beam, tiles):
    beams = [first_beam]
    while len(beams) > 0:
        new_beams = []
        for beam in beams:
            new_beam = process_beam(beam, tiles)
            if new_beam is not None:
                if isinstance(new_beam, list):
                    new_beams.extend(new_beam)
                else:
                    new_beams.append(new_beam)
        beams = new_beams
    return tiles


def main():
    input_list = read_input("day16.txt")
    init_tiles = prepare_input(input_list)
    # Up
    upper_number = []
    for tile in init_tiles[0]:
        tiles = prepare_input(input_list)
        first_beam = Beam(tile.x, tile.y, "down")
        tiles = start_cycle(first_beam, tiles)
        upper_number.append(
            sum(map(lambda y: 1, filter(lambda x: len(x.directions) > 0, [tile for line in tiles for tile in line]))))

    print(max(upper_number))
    # Left
    left_number = []
    for tile in init_tiles:
        tiles = prepare_input(input_list)
        first_beam = Beam(tile[0].x, tile[0].y, "right")
        tiles = start_cycle(first_beam, tiles)
        left_number.append(
            sum(map(lambda y: 1, filter(lambda x: len(x.directions) > 0, [tile for line in tiles for tile in line]))))
    print(max(left_number))
    # Right
    right_number = []
    for tile in init_tiles:
        tiles = prepare_input(input_list)
        first_beam = Beam(tile[-1].x, tile[-1].y, "left")
        tiles = start_cycle(first_beam, tiles)
        right_number.append(
            sum(map(lambda y: 1, filter(lambda x: len(x.directions) > 0, [tile for line in tiles for tile in line]))))
    print(max(right_number))
    # Down
    down_number = []
    for tile in init_tiles[-1]:
        tiles = prepare_input(input_list)
        first_beam = Beam(tile.x, tile.y, "up")
        tiles = start_cycle(first_beam, tiles)
        down_number.append(
            sum(map(lambda y: 1, filter(lambda x: len(x.directions) > 0, [tile for line in tiles for tile in line]))))
    print(max(down_number))


if __name__ == "__main__":
    main()
