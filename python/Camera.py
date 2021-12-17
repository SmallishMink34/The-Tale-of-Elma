import pygame

class GameCamera(object):
    """A GameCamera captures a part of the given World object in the given
    position and produces a pygame.Surface object of the given size.
    
    You can design the World class yourself with these attributes:
        - rect - a pygame.Rect object
        - surface - a pygame.Surface object
        - objects - a list of objects the camera can follow (focus on)
    """
    
    def __init__(self, size, world, display_position, position=(0, 0), on=True):
        self.target = None
        
        self.world = world
        self.pos = position
        self.size = size
        self.zoomscale = 1
        self.size[0], self.size[1] = self.size[0]*self.zoomscale, self.size[1]*self.zoomscale
        self.rect = pygame.Rect(self.pos, self.size)
        self.surface = pygame.Surface(self.size)

        self.display_position = display_position
        self.display_rect = pygame.Rect(display_position, size)

        self.on = on
        

    def __str__(self):
        return 'GameCamera: %s, size: %s, tracking: %s' % \
            (self.world, self.rect.size, self.target)

    def track(self, target):
        """Give the camera a target object to track.
        The object must be present in the camera's World object.
        """
        if target in self.world.objects:
            self.target = target
            self.focus_on(self.target)
        else:
            msg = '%s is not in the %s.' % (target, self.world)
            raise(Exception(msg))

    def stop_tracking(self):
        """Stop tracking the target object."""
        self.target = None

    def focus_on(self, target_object):
        """Make the GameCamera jump to a specific object on the map."""
        if target_object in self.world.objects:
            self.rect.left = target_object.centerx - self.rect.width / 2
            self.rect.top = target_object.centery - self.rect.height / 2
        else:
            msg = '%s is not in the %s.' % (target, self.world)
            raise(Exception(msg))

    def focus(self):
        """Center the camera on the target object, if set."""
        if self.target:
            self.focus_on(self.target)
        else:
            pass

    def move(self, x, y):
        """Move the GameCamera by a number of pixels in x and y directions."""
        new_left = self.rect.left + x
        new_right = self.rect.right + x
        new_top = self.rect.top + y
        new_bottom = self.rect.bottom + y

        if new_left < 0:
            self.rect.left = 0
        elif new_right > self.world.rect.right:
            self.rect.right = self.world.rect.right
        else:
            self.rect.left = new_left

        if new_top < 0:
            self.rect.top = 0
        elif new_bottom > self.world.rect.bottom:
            self.rect.bottom = self.world.rect.bottom
        else:
            self.rect.top = new_top

    def mouseover(self, mouse_x, mouse_y):
        """Check if the cursor is positioned over the camera's display."""
        if self.display_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

    def get_frame(self):
        """Capture the current state of the world."""
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.world.surface, (0, 0), area=self.rect)
    
    def display(self, screen):
        """Prepare a frame pygame.Surface object and blit it to the given 
        pygame.display or pygame.Surface object.
        """
        if not self.on:
            return

        self.focus()
        self.get_frame()
        
        screen.blit(pygame.transform.scale(self.surface, (self.size[0]*self.zoomscale, self.size[1]*self.zoomscale)), (0, 0))

    def turn_on(self):
        """Turn the camera on."""
        self.on = True

    def turn_off(self):
        """Turn the camera off."""
        self.on = False

    def toggle(self):
        """Toggle the camera's state - on and off."""
        self.on = False if self.on else True

    def zoom(self, zoom):
        #self.world.rect = pygame.transform.scale(self.world.rect, (1280, 720))
        self.zoomscale = zoom
        

class World():
    def __init__(self, rect, surface, object):
        self.rect = rect
        self.surface = surface
        self.objects = object