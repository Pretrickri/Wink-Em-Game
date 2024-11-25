import random
import copy
import numpy as np
import sys

# Redirect output to a file to save the game log
sys.stdout = open("wink_em_output.txt", "w")

# Define the Sitter class
class Sitter:
    def __init__(self, sitter_id):
        self.sitter_id = sitter_id
        self.escapes = 0
        self.taps = 0
        self.escapability = np.random.normal(loc=5, scale=1)  # Ability to escape
        self.escapability = np.clip(self.escapability, 1, 10)  # Limit escapability between 1 and 10
        self.consistency = random.uniform(0.5, 1.0)  # How consistent the sitter is
        self.fun = 0  # Fun metric, influenced by interactions
        self.patienceMax = random.randint(3, 6) # For the future : patience should reflect a normal distribution that depends on the amount of people playing. The more people playing, the more patient the players will likely be.
        self.patience = copy.copy(self.patienceMax)

    def losePatience(self):
        self.patience -= 1
        if self.patience <= 0:
            self.patience = 0

    def recoverPatience(self):
        self.patience = copy.copy(self.patienceMax)

    def addFun(self):
        self.fun += 2
    
    def loseFun(self):
        self.fun -= 1

    def escape(self):
        self.escapes += 1  # Increment escapes on a successful escape

    def tapped(self):
        self.taps += 1  # Increment taps when the sitter is tapped

    def __repr__(self):
        # String representation for the Sitter's status
        return f"Sitter {self.sitter_id} | Escapes: {self.escapes} | Taps: {self.taps} | Escapability: {self.escapability} | Consistency: {self.consistency} | Fun: {self.fun} | Patience: {self.patience}"


# Define the Tapper class
class Tapper:
    def __init__(self, tapper_id):
        self.tapper_id = tapper_id
        self.successful_taps = 0
        self.failed_taps = 0
        self.tapability = np.random.normal(loc=5, scale=2)  # Ability to tap
        self.tapability = np.clip(self.tapability, 1, 10)  # Limit tapability between 1 and 10
        self.consistency = random.uniform(0.5, 1.0)  # How consistent the tapper is
        self.fun = 0  # Fun metric, influenced by interactions
        self.patienceMax = random.randint(3, 6) # For the future : patience should reflect a normal distribution that depends on the amount of people playing. The more people playing, the more patient the players will likely be.
        self.patience = copy.copy(self.patienceMax)

    def losePatience(self):
        self.patience -= 1
        if self.patience <= 0:
            self.patience = 0

    def recoverPatience(self):
        self.patience = copy.copy(self.patienceMax)

    def addFun(self):
        self.fun += 2
    
    def loseFun(self):
        self.fun -= 1

    def successful_tap(self):
        self.successful_taps += 1  # Increment successful taps

    def failed_tap(self):
        self.failed_taps += 1  # Increment failed taps

    def __repr__(self):
        # String representation for the Tapper's status
        return f"Tapper {self.tapper_id} | Successful Taps: {self.successful_taps} | Failed Taps: {self.failed_taps} | Tapability: {self.tapability} | Consistency: {self.consistency} | Fun: {self.fun} | Patience: {self.patience}"


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
            if sitter.patience == 0:
                sitter.loseFun()
        for tapper in self.tappers:
            if tapper.patience == 0:
                tapper.loseFun()

    def assign_tappers_to_sitters(self):
        """Assign each tapper to a sitter, leaving one tapper for the empty chair."""
        tapper_sitter_map = {}
        for i, tapper in enumerate(self.tappers):
            if i < self.num_sitters:
                tapper_sitter_map[tapper] = self.sitters[i]
            else:
                tapper_sitter_map[tapper] = None  # Empty chair assignment
        return tapper_sitter_map

    def find_tapper_for_sitter(self, sitter):
        """Find the tapper assigned to a specific sitter."""
        for tapper, mapped_sitter in self.tapper_sitter_map.items():
            if mapped_sitter == sitter:
                return tapper
        return None

    def random_wink(self):
        """Randomly select a sitter for the empty chair tapper to wink at."""
        empty_chair_tapper = next(tapper for tapper, sitter in self.tapper_sitter_map.items() if sitter is None)
        winked_sitter = random.choice(self.sitters)
        return empty_chair_tapper, winked_sitter
    
    def handlePatienceAndFun(self, winker, winked_sitter, sitter_tapper):
        winker.recoverPatience()
        winked_sitter.recoverPatience()
        sitter_tapper.recoverPatience()
        winker.addFun()
        winked_sitter.addFun()
        sitter_tapper.addFun()
        
        for sitter in self.sitters:
            if sitter == winked_sitter : continue
            sitter.losePatience()
            if sitter.patience == 0:
                sitter.loseFun()
        for tapper in self.tappers:
            if tapper == winker or tapper == sitter_tapper : continue
            tapper.losePatience()
            if tapper.patience == 0:
                tapper.loseFun()




    def random_escape_attempt(self, winked_sitter, sitter_tapper, winker):
        """Determine if the sitter can escape or is tapped."""
        temp1 = winked_sitter.escapability * winked_sitter.consistency
        temp2 = sitter_tapper.tapability * sitter_tapper.consistency
        total = temp1 + temp2
        random_value = random.uniform(0, total)

        print(f"Sitter Value: {temp1}, Tapper Value: {temp2}, Total: {total}, Random: {random_value}")

        # Fun metrics
        self.handlePatienceAndFun(winker, winked_sitter, sitter_tapper)

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
            empty_chair_tapper, winked_sitter = self.random_wink()
            print(f"Tapper {empty_chair_tapper.tapper_id} winked at Sitter {winked_sitter.sitter_id}.")

            sitter_tapper = self.find_tapper_for_sitter(winked_sitter)
            print(f"Tapper {sitter_tapper.tapper_id} is assigned to Sitter {winked_sitter.sitter_id}.")

            if self.random_escape_attempt(winked_sitter, sitter_tapper, empty_chair_tapper):
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
