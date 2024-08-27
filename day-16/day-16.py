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
    def __init__(self, x, y, value, symbol):
        self.x = x
        self.y = y
        self.value = value
        self.symbol = symbol


def read_input(filename):
    with open(filename) as f:
        return f.read().splitlines()


def prepare_input(input_list):
    tiles = []
    for y, line in enumerate(input_list):
        tiles_line = []
        for x, symbol in enumerate(line):
            tiles_line.append(Tile(x, y, 0, symbol))
        tiles.append(tiles_line)
    return tiles


def show_tiles(tiles):
    for line in tiles:
        for tile in line:
            print(tile.symbol if tile.value == 0 else "#", end="")
        print()
    print()

def process_beam(beam, tiles, beams):
    if beam.x < 0 or beam.y < 0:
        return None
    if beam.y >= len(tiles) or beam.x >= len(tiles[0]):
        return None
    current_tile = tiles[beam.y][beam.x]
    # Energize the tile
    current_tile.value += 1

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


def main():
    input_list = read_input("day16.txt")
    tiles = prepare_input(input_list)

    first_beam = Beam(0, 0, "right")
    beams = [first_beam]
    for _ in range(1000):
        new_beams = []
        for beam in beams:
            new_beam = process_beam(beam, tiles, beams)
            if new_beam is not None:
                if isinstance(new_beam, list):
                    new_beams.extend(new_beam)
                else:
                    new_beams.append(new_beam)
        beams = new_beams

    print(sum(map(lambda y: 1, filter(lambda x: x.value > 0, [tile for line in tiles for tile in line]))))


if __name__ == "__main__":
    main()
