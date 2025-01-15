class Board:
    def __init__(self, is_computer=False):
        self.size = 10
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []
        self.is_computer = is_computer

    def can_place_ship(self, ship_size, x, y, horizontal):
        if horizontal:
            if x + ship_size > self.size:
                return False
            return all(self.grid[y][x + i] == 0 for i in range(ship_size))
        else:
            if y + ship_size > self.size:
                return False
            return all(self.grid[y + i][x] == 0 for i in range(ship_size))

    def place_ship(self, ship, x, y, horizontal):
        if horizontal:
            for i in range(ship.size):
                self.grid[y][x + i] = 1
                ship.positions.append((y, x + i))
        else:
            for i in range(ship.size):
                self.grid[y + i][x] = 1
                ship.positions.append((y + i, x))
        self.ships.append(ship)