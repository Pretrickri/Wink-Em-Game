# Wink-Em-Game
For our CSC324 group project

main.py is V2.0

Changes from V1 (winkem.py):
1) Fun added
      - Those who play (so three at each interval) get +1
      - Rest get -(1/tot_players)

2) Bug Fixed
      - Bug was that random_escape_attempt didn't do calculations for sitter and sitter's tapper. Previously, it would do calculations for sitter and the winker. This is now fixed

3) Escapability and Tapability is now determined with a Normal Distribution
      - the scale in np.random.normal(loc=5, scale=1) determines variability. I have left it as 1 for now.

4) Prints console outputs to a file
      - I have traced the outputs. Everything seems to be okay.
