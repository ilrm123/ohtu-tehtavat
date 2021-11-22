class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
        self.players = reader.players
    
    def top_scorers_by_nationality(self, nationality):
        new = sorted(self.players, key=lambda x: x.points, reverse=True)
        newer = []
        
        for player in new:
            if player.nationality == nationality:
                newer.append(player)
        
        return newer
