import random
import numpy as np
import sys
import math

# Redirect output to a file to save the game log
sys.stdout = open("wink_em_output.txt", "w")

# Define the Sitter class
class Sitter:
    def __init__(self, sitter_id):
        self.sitter_id = sitter_id
        self.escapes = 0
        self.taps = 0
        self.escapability = np.random.normal(loc=5, scale=1.0)  # Ability to escape
        self.escapability = np.clip(self.escapability, 1.01, 9.99)  # Limit escapability between 1 and 10
        self.consistency = random.uniform(0.5, 1.0)  # How consistent the sitter is
        self.fun = 0  # Fun metric, influenced by interactions
        self.winkability = 1

    def escape(self):
        self.escapes += 1  # Increment escapes on a successful escape

    def tapped(self):
        self.taps += 1  # Increment taps when the sitter is tapped

    def __repr__(self):
        # String representation for the Sitter's status
        return f"Sitter {self.sitter_id} | Escapes: {self.escapes} | Taps: {self.taps} | Escapability: {self.escapability} | Consistency: {self.consistency} | Fun: {self.fun}"


# Define the Tapper class
class Tapper:
    def __init__(self, tapper_id):
        self.tapper_id = tapper_id
        self.successful_taps = 0
        self.failed_taps = 0
        self.tapability = np.random.normal(loc=5, scale=1.0)  # Ability to tap
        self.tapability = np.clip(self.tapability, 1.01, 9.99)  # Limit tapability between 1 and 10
        self.consistency = random.uniform(0.5, 1.0)  # How consistent the tapper is
        self.fun = 0  # Fun metric, influenced by interactions

    def successful_tap(self):
        self.successful_taps += 1  # Increment successful taps

    def failed_tap(self):
        self.failed_taps += 1  # Increment failed taps

    def __repr__(self):
        # String representation for the Tapper's status
        return f"Tapper {self.tapper_id} | Successful Taps: {self.successful_taps}, Failed Taps: {self.failed_taps}, Tapability: {self.tapability}, Consistency: {self.consistency}, Fun: {self.fun}"


# Define the WinkEmGame class
class WinkEmGame:
    def __init__(self, num_sitters, num_iterations):
        self.num_sitters = num_sitters
        self.num_tappers = num_sitters + 1  # One extra tapper for the empty chair
        self.tot_players = self.num_sitters + self.num_tappers
        self.minus_fun = 1 / self.tot_players  # Fun decrement per turn
        self.num_iterations = num_iterations
        self.sitters = [Sitter(i) for i in range(1, num_sitters + 1)]
        self.tappers = [Tapper(i) for i in range(1, num_sitters + 2)]
        self.tapper_sitter_map = self.assign_tappers_to_sitters()

    def remove_fun(self):
        """Reduce fun for all players by a fixed amount each turn."""
        for sitter in self.sitters:
            sitter.fun -= self.minus_fun
        for tapper in self.tappers:
            tapper.fun -= self.minus_fun

    def assign_tapprandom_winker_for_sitter(self, sitter):
        """Find the tapper assigned to a specific sitter."""
        for tapper, mapped_sitter in self.tapper_sitter_map.items():
            if mapped_sitter == sitter:
                return tapper
        return None

    def find_winker(self):
        """Randomly select a sitter for the empty chair tapper to wink at."""
        empty_chair_tapper = next(tapper for tapper, sitter in self.tapper_sitter_map.items() if sitter is None)
        #winked_sitter = random.choice(self.sitters) To be removed
        return empty_chair_tapper
    
    def reset_winkability(self):
        for sitter in self.sitters:
            sitter.winkability = 1
    
    def position_based_probability_enhancer(self, winker):
        position = winker.tapper_id
        halfway = self.num_tappers // 2
        range = math.trunc(0.1 * self.num_tappers)
        player_across = (position + halfway) % self.num_tappers # position +/- the number of tappers/2 

        player_across_temp1 = player_across
        player_across_temp2 = player_across
        winkability_boost = 0.1

        for tapper in self.tappers:
            if tapper.tapper_id == player_across:
                tapper_across = tapper
        sitter_across1 = self.tapper_sitter_map[tapper_across]
        sitter_across2 = self.tapper_sitter_map[tapper_across]
        sitter_across1.winkability = sitter_across1.winkability * (1+winkability_boost)

        for i in range(range):
            winkability_boost = winkability_boost/2
            player_across_temp1 = (player_across_temp1 + 1) % self.num_tappers
            for tapper in self.tappers:
                if tapper.tapper_id == player_across_temp1:
                        tapper_temp1 = tapper

            player_across_temp2 = (player_across_temp2 + 1) % self.num_tappers
            for tapper in self.tappers:
                if tapper.tapper_id == player_across_temp2:
                        tapper_temp2 = tapper

            sitter_temp1 = self.tapper_sitter_map[tapper_temp1]
            sitter_temp1.winkability = sitter_temp1.winkability * (1+ winkability_boost)

            sitter_temp2 = self.tapper_sitter_map[tapper_temp2]
            sitter_temp2.winkability = sitter_temp2.winkability * (1+ winkability_boost)
        
        winkability_boost = .1
    '''
    def choose_sitter(self, winker):
    '''
    


    def random_escape_attempt(self, winked_sitter, sitter_tapper, winker):
        """Determine if the sitter can escape or is tapped."""
        temp1 = winked_sitter.escapability * winked_sitter.consistency
        temp2 = sitter_tapper.tapability * sitter_tapper.consistency
        total = temp1 + temp2
        random_value = random.uniform(0, total)

        print(f"Sitter Value: {temp1}, Tapper Value: {temp2}, Total: {total}, Random: {random_value}")

        # Fun metrics
        winker.fun += 1 + self.minus_fun
        winked_sitter.fun += 1 + self.minus_fun
        sitter_tapper.fun += 1 + self.minus_fun
        self.remove_fun()

        if random_value < temp1:
            # Successful escape
            winked_sitter.escape()
            self.tapper_sitter_map[sitter_tapper] = None  # Previous tapper moves to the empty chair
            self.tapper_sitter_map[winker] = winked_sitter  # Winker takes the sitter's position
            sitter_tapper.failed_tap()
            return True
        else:
            # Sitter is tapped
            winked_sitter.tapped()
            sitter_tapper.successful_tap()
            return False

    def run(self):
        """Run the game for the specified number of iterations."""
        for iteration in range(1, self.num_iterations + 1):
            print(f"\n--- Iteration {iteration} ---")
            empty_chair_tapper = self.find_winker()
            self.position_based_probability_enhancer(empty_chair_tapper)
            '''
            We need a function that returns winked_sitter using the winkability attribute
            reset winkability
            '''
            print(f"Tapper {empty_chair_tapper.tapper_id} winked at Sitter {winked_sitter.sitter_id}.")

            sitter_tapper = self.find_tapper_for_sitter(winked_sitter)
            print(f"Tapper {sitter_tapper.tapper_id} is assigned to Sitter {winked_sitter.sitter_id}.")

            if self.random_etapper_idscape_attempt(winked_sitter, sitter_tapper, empty_chair_tapper):
                print(f"Sitter {winked_sitter.sitter_id} escaped successfully!")
            else:
                print(f"Sitter {winked_sitter.sitter_id} was tapped.")

            self.show_game_status()

    def show_game_status(self):
        """Display the current status of sitters and tappers."""
        print("\nCurrent Sitters Status:")
        for sitter in self.sitters:
            print(sitter)
        print("\nCurrent Tappers Status:")
        for tapper in self.tappers:
            sitter = self.tapper_sitter_map[tapper]
            sitter_info = f"Sitter {sitter.sitter_id}" if sitter else "None (empty chair)"
            print(f"Tapper {tapper.tapper_id} is guarding {sitter_info} | Successful Taps: {tapper.successful_taps} | Failed Taps: {tapper.failed_taps} | Tapability: {tapper.tapability} | Consistency: {tapper.consistency} | Fun: {tapper.fun}")


# Run the game
wink_em_game = WinkEmGame(num_sitters=9, num_iterations=25)
wink_em_game.run()

# Restore stdout
sys.stdout.close()
sys.stdout = sys.__stdout__