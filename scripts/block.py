import pygame

BLOCKS = {
    'break': 1,
    'fixed': 2,
    'mystery': 3
} # Images 01, 02, and 03 in the block tiles

class Block:

    def __init__(self, game, pos, type):
        """
        Args: pos - x, y position
              type - string for the block types
        """
        self.game = game
        self.pos = list(pos)
        self.type = BLOCKS[type] # This is the "variant" number in the assets

    # Update the block position and type
    def update(self, new_type=None, movement=(0, 0)):
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
        self.type = new_type

    # Render the block and adjust it's type if necessary
    def render(self, surface, offset=(0, 0)):
        surface.blit(self.game.assets['block'][type], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
