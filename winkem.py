import random
import numpy as np
import sys

# Redirect output to a file
sys.stdout = open("wink_em_output.txt", "w")

class Sitter:
    def __init__(self, sitter_id):
        self.sitter_id = sitter_id
        self.escapes = 0
        self.taps = 0
        self.escapability = np.random.normal(loc=5, scale=1)
        self.escapability = np.clip(self.escapability, 1, 10)
        self.consistency = random.uniform(0.5, 1.0)

    def escape(self):
        self.escapes += 1

    def tapped(self):
        self.taps += 1

    def __repr__(self):
        return f"Sitter {self.sitter_id} | Escapes: {self.escapes}, Taps: {self.taps}, Var: {self.escapability}, {self.consistency}"


class Tapper:
    def __init__(self, tapper_id):
        self.tapper_id = tapper_id
        self.successful_taps = 0
        self.failed_taps = 0
        self.tapability = np.random.normal(loc=5, scale=2)
        self.tapability = np.clip(self.tapability, 1, 10)
        self.consistency = random.uniform(0.5, 1.0)

    def successful_tap(self):
        self.successful_taps += 1

    def failed_tap(self):
        self.failed_taps += 1

    def __repr__(self):
        return f"Tapper {self.tapper_id} | Successful Taps: {self.successful_taps}, Failed Taps: {self.failed_taps}, Var: {self.tapability}, {self.consistency}"


class WinkEmGame:
    def __init__(self, num_sitters, num_iterations):
        self.num_sitters = num_sitters
        self.num_tappers = num_sitters + 1
        self.num_iterations = num_iterations
        self.sitters = [Sitter(i) for i in range(1, num_sitters + 1)]
        self.tappers = [Tapper(i) for i in range(1, num_sitters + 2)]
        self.tapper_sitter_map = self.assign_tappers_to_sitters()

    def assign_tappers_to_sitters(self):
        tapper_sitter_map = {}
        for i, tapper in enumerate(self.tappers):
            if i < self.num_sitters:
                tapper_sitter_map[tapper] = self.sitters[i]
            else:
                tapper_sitter_map[tapper] = None
        return tapper_sitter_map

    def random_wink(self):
        empty_chair_tapper = next(tapper for tapper, sitter in self.tapper_sitter_map.items() if sitter is None)
        winked_sitter = random.choice([sitter for sitter in self.sitters])
        return empty_chair_tapper, winked_sitter

    def random_escape_attempt(self, winked_sitter, winker_tapper):
        temp1 = winked_sitter.escapability * winked_sitter.consistency
        temp2 = winker_tapper.tapability * winker_tapper.consistency
        total = temp1 + temp2
        random_value = random.uniform(0, total)

        print(f"Sitter Value: {temp1}, Tapper Value: {temp2}, Total: {total}, Random: {random_value}")

        if random_value < temp1:
            winked_sitter.escape()
            winker_tapper.failed_tap()
            return True
        else:
            winked_sitter.tapped()
            winker_tapper.successful_tap()
            return False

    def run(self):
        for iteration in range(1, self.num_iterations + 1):
            print(f"\n--- Iteration {iteration} ---")
            winker, winked_sitter = self.random_wink()
            print(f"Tapper {winker.tapper_id} winked at Sitter {winked_sitter.sitter_id}.")
            if self.random_escape_attempt(winked_sitter, winker):
                print(f"Sitter {winked_sitter.sitter_id} escaped successfully!")
            else:
                print(f"Sitter {winked_sitter.sitter_id} was tapped.")

            self.show_game_status()

    def show_game_status(self):
        print("\nCurrent Sitters Status:")
        for sitter in self.sitters:
            print(sitter)
        print("\nCurrent Tappers Status:")
        for tapper in self.tappers:
            print(tapper)


# Run the game
wink_em_game = WinkEmGame(num_sitters=19, num_iterations=1)
wink_em_game.run()

# Close the output file and restore stdout
sys.stdout.close()
sys.stdout = sys.__stdout__
