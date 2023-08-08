import pygame

class PhysicsEntity:

    def __init__ (self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.action = ''
        self.set_action('idle')
        self.flip = False
        self.anim_offset = (-2, -2)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0)): # Add back tilemap
        self.collisions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }

        # Move the entity, check for collisions
        frame_movement = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])

        if frame_movement[0] < 0:
            self.flip = True
        elif frame_movement[0] > 0:
            self.flip = False

        # Handle movement and collisions for x and y axis separately
        #
        # An interesting problem: If the player rect is much bigger than a tile (in the case I had a problem with, tiles are 16x16
        # and the player rect was 32x32), then the "tiles around" won't be calculated correctly because the nearby tiles are only
        # found around a rect with a size the same as the tile size
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for tile in tilemap.tile_rects_around(entity_rect.center): # Check left/right collisions
            if entity_rect.colliderect(tile):
                if frame_movement[0] < 0:
                    self.collisions['left'] = True
                    entity_rect.left = tile.right
                if frame_movement[0] > 0:
                    self.collisions['right'] = True
                    entity_rect.right = tile.left
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for tile in tilemap.tile_rects_around(entity_rect.center): # Check top/bottom collisions
            if entity_rect.colliderect(tile):
                if frame_movement[1] < 0:
                    self.collisions['up'] = True
                    entity_rect.top = tile.bottom
                if frame_movement[1] > 0:
                    self.collisions['down'] = True
                    entity_rect.bottom = tile.top
                self.pos[1] = entity_rect.y

        self.last_movement = list(movement)

        # Enforce gravity
        self.velocity[1] = min(5, self.velocity[1] + 0.2)

        # If on ground or bump into something above, set vertical velocity to 0
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()
        
    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Player(PhysicsEntity):

    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)

        self.air_time = 0
        self.jumps = 1
        self.x_accel = 0 # Tracking variable for speedup/slowdown
        self.last_accel = 0 # Tracking variable for acceleration and turning
        self.speed = 2 # Max player speed

    def jump(self):
        if self.jumps and self.air_time < 5:
            self.velocity[1] -= 5.5
            self.jumps -= 1
            self.air_time = 5
            return True
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=(self.x_accel, movement[1]))
        
        # Handle air time and the number of jumps
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1

        # Speed up and slow down, with turn animation
        if movement[0] < 0:
            self.x_accel = max(self.x_accel - 0.1, -self.speed)
            #if (not self.flip) and self.collisions['down']:
            #    self.set_action('turn')
        elif movement[0] > 0:
            self.x_accel = min(self.x_accel + 0.1, self.speed)
            #if self.flip and self.collisions['down']:
            #    self.set_action('turn')
        else:
            if self.flip:
                self.x_accel = min(self.x_accel + 0.1, 0)
            else:
                self.x_accel = max(self.x_accel - 0.1, 0)

        # Set the proper action
        if self.air_time > 4:
            self.set_action('jump')
        else:
            if movement[0] != 0:
                if (self.flip) and (self.x_accel > self.last_accel): # If facing left, turning right
                    self.set_action('turn')
                elif (not self.flip) and (self.x_accel < self.last_accel): # If facing right, turning left
                    self.set_action('turn')
                else:
                    self.set_action('run')
            else:
                self.set_action('idle')
        
        self.last_accel = self.x_accel # Tracking variable for turning 
        
    def render(self, surface, offset=(0, 0)):
        if self.action == 'idle':
            super().render(surface, offset=offset)
        else:
            surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1]))
