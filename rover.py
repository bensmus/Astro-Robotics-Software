class Rover:
    def __init__(self, start, dest):
        self.pos = start
        self.dest = dest
        self.scanned_pts = []
    
    def scan(self, wall_pts):
        """Grows scanned_pts"""
        ...
    
    def move(self):
        # Dummy function
        self.pos.y += 1
