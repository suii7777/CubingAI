import random

class ScrambleGenerator:
    MOVES = ['U', 'D', 'R', 'L', 'F', 'B']
    MODIFIERS = ['', "'", '2']

    def __init__(self):
        self.last_move = None
        self.last_face = None

    def _is_opposite_face(self, face1, face2):
        opposites = {
            'U': 'D', 'D': 'U',
            'R': 'L', 'L': 'R',
            'F': 'B', 'B': 'F'
        }
        return opposites.get(face1) == face2

    def _is_valid_next_move(self, move):
        if self.last_face is None:
            return True
        
        face = move[0]  # Get the face of the move (U, D, R, L, F, B)
        
        # Don't allow moves on the same face or opposite face consecutively
        if face == self.last_face or self._is_opposite_face(face, self.last_face):
            return False
            
        return True

    def generate_scramble(self, length=20):
        scramble = []
        self.last_face = None

        while len(scramble) < length:
            # Generate a random move
            face = random.choice(self.MOVES)
            modifier = random.choice(self.MODIFIERS)
            move = face + modifier

            # Check if the move is valid
            if self._is_valid_next_move(move):
                scramble.append(move)
                self.last_face = face

        return ' '.join(scramble)

    def get_scramble_with_explanation(self):
        """Generate a scramble with move explanations."""
        scramble = self.generate_scramble()
        moves = scramble.split()
        
        explanations = []
        for move in moves:
            base_move = move[0]
            modifier = move[1] if len(move) > 1 else ''
            
            explanation = {
                'U': 'Upper face',
                'D': 'Down face',
                'R': 'Right face',
                'L': 'Left face',
                'F': 'Front face',
                'B': 'Back face'
            }[base_move]
            
            if modifier == "'":
                explanation += " counterclockwise"
            elif modifier == '2':
                explanation += " 180 degrees"
            else:
                explanation += " clockwise"
                
            explanations.append(explanation)
            
        return scramble, explanations
