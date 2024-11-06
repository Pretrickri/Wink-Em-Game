"""
PROF ELIOTT'S VERSION OF WINK 'EM
    - Tappers and Sitters do not ever switch places
    - Extra Chair: Tapper present at extra chair does the winking

Data Structure Used:
    - Hash Maps/Dictionary: Key -> Value Mapping
"""

import random

class Sitter:
    def __init__(self, sitter_id):
        self.sitter_id = sitter_id
        self.escapes = 0 # Variable
        self.taps = 0 # Variable

    def escape(self):
        self.escapes += 1

    def tapped(self):
        self.taps += 1

    #Print Function essentially
    def __repr__(self):
        return f"Sitter {self.sitter_id} | Escapes: {self.escapes}, Taps: {self.taps}" 


class Tapper:
    def __init__(self, tapper_id):
        self.tapper_id = tapper_id
        self.successful_taps = 0 # Variable
        self.failed_taps = 0 # Variable

    def successful_tap(self):
        self.successful_taps += 1

    def failed_tap(self):
        self.failed_taps += 1

    # Tapper's print function
    def __repr__(self):
        return f"Tapper {self.tapper_id} | Successful Taps: {self.successful_taps}, Failed Taps: {self.failed_taps}"

# Define the Game class
class WinkEmGame:
    def __init__(self, num_sitters, num_iterations):
        self.num_sitters = num_sitters
        self.num_tappers = num_sitters + 1  # One extra tapper
        self.num_iterations = num_iterations
        self.sitters = [Sitter(i) for i in range(1, num_sitters + 1)]  # This and line below use List Comprehension
        self.tappers = [Tapper(i) for i in range(1, num_sitters + 2)]  # One more tapper than sitters
        self.tapper_sitter_map = self.assign_tappers_to_sitters() # Init hash map/dictionary

    def assign_tappers_to_sitters(self):
        """
        Assign tappers to sitters in a 1-to-1 mapping. One tapper will be mapped to None (the empty chair).
        """
        tapper_sitter_map = {}
        for i, tapper in enumerate(self.tappers):
            if i < self.num_sitters:
                tapper_sitter_map[tapper] = self.sitters[i]
            else:
                tapper_sitter_map[tapper] = None  # One tapper mapped to the empty chair (None)
        return tapper_sitter_map

    def random_wink(self):
        """
        The tapper assigned to the empty chair winks at a random sitter.
        """
        empty_chair_tapper = next(tapper for tapper, sitter in self.tapper_sitter_map.items() if sitter is None) # This finds tapper that's mapped to the empty chair
        winked_sitter = random.choice([sitter for sitter in self.sitters if sitter in self.tapper_sitter_map.values()]) #randomly pick a sitter to wink at
        return empty_chair_tapper, winked_sitter

    def random_escape_attempt(self, winked_sitter, winker_tapper):
        """
        Randomly decide if the sitter can escape before being tapped.
        """
        # I believe this is 50/50. We can later add a weighted calculation here to determine % chance of escaping.
        escape_successful = random.choice([True, False]) 

        if escape_successful:
            winked_sitter.escape()
            # Find the tapper of the winked sitter and update them to have the empty chair
            old_tapper = next(tapper for tapper, sitter in self.tapper_sitter_map.items() if sitter == winked_sitter)
            self.tapper_sitter_map[old_tapper] = None
            self.tapper_sitter_map[winker_tapper] = winked_sitter
            winker_tapper.failed_tap()
            return True
        else:
            winked_sitter.tapped()
            winker_tapper.successful_tap()
            return False

    def run(self):
        """
        Run the game for the designated number of iterations.
        One iteration means one attempt at winking and escaping/tapping.
        Events are outputted in txt to console along in this order: Event -> Event Result -> Sitters Status -> Tappers Status
        """
        for iteration in range(1, self.num_iterations + 1):
            print(f"\n--- Iteration {iteration} ---")

            # 1. Wink at a random sitter
            winker, winked_sitter = self.random_wink()
            print(f"Tapper {winker.tapper_id} winked at Sitter {winked_sitter.sitter_id}.")

            # 2. Determine if the sitter can escape
            if self.random_escape_attempt(winked_sitter, winker):
                print(f"Sitter {winked_sitter.sitter_id} escaped to the empty chair.")
            else:
                print(f"Sitter {winked_sitter.sitter_id} was tapped by Tapper {winker.tapper_id}.")

            # 3. Show the current game status after each iteration
            self.show_game_status()

    def show_game_status(self):
        """
        Display the current state of all sitters and tappers.
        """
        print("\nCurrent Sitters Status:")
        for sitter in self.sitters:
            print(sitter)

        print("\nCurrent Tappers Status:")
        for tapper in self.tappers:
            sitter = self.tapper_sitter_map[tapper]
            sitter_info = f"Sitter {sitter.sitter_id}" if sitter else "None (empty chair)"
            print(f"Tapper {tapper.tapper_id} is guarding {sitter_info} | Successful Taps: {tapper.successful_taps} | Failed Taps: {tapper.failed_taps}")

# We give the game init class just num of sitters bc num of tappers is just +1. 
wink_em_game = WinkEmGame(num_sitters=4, num_iterations=10)
wink_em_game.run()
