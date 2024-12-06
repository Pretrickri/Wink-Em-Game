import random
import numpy as np
import sys
import math
import copy


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
        # return f"Sitter {self.sitter_id} | Escapes: {self.escapes} | Taps: {self.taps} | Escapability: {self.escapability} | Consistency: {self.consistency} | Winkability: {self.winkability} | Fun: {self.fun} | Patience: {self.patience}"
        return f"[{self.sitter_id}, {self.escapes}, {self.taps}, {self.escapability}, {self.consistency}, {self.winkability}, {self.fun}, {self.patience}],"


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
        return f"Tapper {self.tapper_id} | Successful Taps: {self.successful_taps} | Failed Taps: {self.failed_taps} | Tapability: {self.tapability} | Consistency: {self.consistency} | Fun: {self.fun} | Patience: {self.patience},"

# Define the WinkEmGame class
class WinkEmGame:
    def __init__(self, num_sitters, num_iterations, num_favourites, num_hated):
        self.num_sitters = num_sitters
        self.num_tappers = num_sitters + 1  # One extra tapper for the empty chair
        self.tot_players = self.num_sitters + self.num_tappers
        self.minus_fun = 1 / self.tot_players  # Fun decrement per turn
        self.num_iterations = num_iterations
        self.sitters = [Sitter(i) for i in range(1, num_sitters + 1)]
        self.tappers = [Tapper(i) for i in range(1, num_sitters + 2)]
        self.tapper_sitter_map = self.assign_tappers_to_sitters()
        self.num_favourites = num_favourites
        self.favourites = self.determine_favourites()
        self.num_hated = num_hated
        self.hated = self.determine_hated()

    def remove_fun(self): 
        """Reduce fun for all players by a fixed amount each turn."""
        for sitter in self.sitters:
            if sitter.patience == 0:
                sitter.loseFun()
        for tapper in self.tappers:
            if tapper.patience == 0:
                tapper.loseFun()

    def determine_favourites(self):
        favourites = random.sample(self.sitters, self.num_favourites)  # Select unique favourites

        for sitter in favourites:
            sitter.winkability += 0.2
            print(f"Sitter ID: {sitter.sitter_id} is now a favourite with winkability {sitter.winkability}")

        return favourites
    
    def determine_hated(self):
        non_favourites = [sitter for sitter in self.sitters if sitter not in self.favourites]

        # Ensure there are enough non-favourites to select from
        if self.num_hated > len(non_favourites):
            raise ValueError("Number of hated sitters cannot exceed the number of non-favourite sitters.")

        # Randomly select hated sitters from the non-favourites
        hated = random.sample(non_favourites, self.num_hated)

        # Decrease winkability for each hated sitter
        for sitter in hated:
            sitter.winkability -= 0.2
            print(f"Sitter ID: {sitter.sitter_id} is now hated with winkability {sitter.winkability}")

        return hated
    

    def assign_tappers_to_sitters(self):
        """Assign each tapper to a sitter, leaving one tapper for the empty chair."""
        tapper_sitter_map = {}
        for i, tapper in enumerate(self.tappers):
            if i < self.num_sitters:
                tapper_sitter_map[tapper] = self.sitters[i]
            else:
                tapper_sitter_map[tapper] = None  # Empty chair assignment
        return tapper_sitter_map

    """
    Updated above

    def remove_fun(self):
        for sitter in self.sitters:
            sitter.fun -= self.minus_fun
        for tapper in self.tappers:
            tapper.fun -= self.minus_fun
    """

    def find_tapper_for_sitter(self, sitter):
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
    
    
    def position_based_probability_enhancer(self, winker):
        """
        Enhances the winkability of sitters based on their positions relative to the winker.
        """
        position = winker.tapper_id  # Position of the winker
        halfway = self.num_tappers // 2  # Halfway point around the circle of tappers
        range_boost = math.trunc(0.1 * self.num_tappers)  # Range for enhancing winkability
        winkability_boost = 0.2  # Initial boost factor

        # Find the tapper directly across the winker
        player_across = (position + halfway) % self.num_tappers

        # Locate the tapper and sitter directly across
        tapper_across = next((tapper for tapper in self.tappers if tapper.tapper_id == player_across), None)
        if tapper_across and self.tapper_sitter_map[tapper_across]:
            sitter_across = self.tapper_sitter_map[tapper_across]
            sitter_across.winkability *= (1 + winkability_boost)

        # Enhance winkability for sitters near the player across
        for i in range(1, range_boost + 1):  # Add 1 to include the range_boost boundary
            winkability_boost /= 2  # Halve the boost for each step away

            # Find sitters on either side of the player across
            player_across_temp1 = (player_across + i) % self.num_tappers
            player_across_temp2 = (player_across - i) % self.num_tappers

            tapper_temp1 = next((tapper for tapper in self.tappers if tapper.tapper_id == player_across_temp1), None)
            tapper_temp2 = next((tapper for tapper in self.tappers if tapper.tapper_id == player_across_temp2), None)

            if tapper_temp1 and self.tapper_sitter_map[tapper_temp1]:
                sitter_temp1 = self.tapper_sitter_map[tapper_temp1]
                sitter_temp1.winkability *= (1 + winkability_boost)

            if tapper_temp2 and self.tapper_sitter_map[tapper_temp2]:
                sitter_temp2 = self.tapper_sitter_map[tapper_temp2]
                sitter_temp2.winkability *= (1 + winkability_boost)

    def choose_sitter(self):
        sitters = self.sitters
        winkabilities = [sitter.winkability for sitter in sitters]
        winked_sitter = random.choices(sitters, weights=winkabilities,k=1)[0]
        return winked_sitter
    
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

    def reset_winkability(self):
        for sitter in self.sitters:
            sitter.winkability = 1
        for sitter in self.favourites:
            sitter.winkability += 0.2
        for sitter in self.hated:
            sitter.winkability -= 0.2
            

    def random_escape_attempt(self, winked_sitter, sitter_tapper, winker):
        """Determine if the sitter can escape or is tapped."""
        temp1 = winked_sitter.escapability * winked_sitter.consistency
        temp2 = sitter_tapper.tapability * sitter_tapper.consistency
        total = temp1 + temp2
        random_value = random.uniform(0, total)

        print(f"Sitter Value: {temp1}, Tapper Value: {temp2}, Total: {total}, Random: {random_value}")
        print(f"[{temp1},{temp2},{total},{random_value}]")

        # Fun metrics
        self.handlePatienceAndFun(winker, winked_sitter, sitter_tapper)
        #winker.fun += 1 + self.minus_fun
        #winked_sitter.fun += 1 + self.minus_fun
        #sitter_tapper.fun += 1 + self.minus_fun
        #self.remove_fun()

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
            winked_sitter = self.choose_sitter()
            print(f"Tapper {empty_chair_tapper.tapper_id} winked at Sitter {winked_sitter.sitter_id}.")
            print(f"[{empty_chair_tapper.tapper_id}, {winked_sitter.sitter_id}]")
            self.reset_winkability()

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
            #sitter_info = f"Sitter {sitter.sitter_id}" if sitter else "None (empty chair)"
            sitter_info = f"{sitter.sitter_id}" if sitter else "-1"
            # print(f"Tapper {tapper.tapper_id} is guarding {sitter_info} | Successful Taps: {tapper.successful_taps} | Failed Taps: {tapper.failed_taps} | Tapability: {tapper.tapability} | Consistency: {tapper.consistency} | Fun: {tapper.fun}")
            print(f"[{tapper.tapper_id}, {sitter_info}, {tapper.successful_taps}, {tapper.failed_taps}, {tapper.tapability}, {tapper.consistency}, {tapper.fun}],")

# Run the game
wink_em_game = WinkEmGame(num_sitters=10, num_iterations=20, num_favourites=2, num_hated=2)
wink_em_game.run()

# Restore stdout
sys.stdout.close()
sys.stdout = sys.__stdout__
