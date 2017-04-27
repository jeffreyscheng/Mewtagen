# Dialgarithm
Python script that generates optimally anti-metagame Pokemon teams using an evolutionary algorithmic approach.

Project requirements:

1) Dex.py, lines 99-115

The Format class uses the comparator magic methods (<, <=, ==, >=, >) in order to classify which formats are more restrictive.

2) I used functools for function wrapping (Metagame.py), os for file I/O(Writer.py), random for list and dict selection (Battle.py, Watchmaker.py, Team.py), pickle for storing objects in txt files (Writer.py), numpy for matrix exponentiation (Damage.py, Team.py), and pandas to keep track of team metrics (Metagame.py).

3) I used time_function() as a decorator of precomputation() in Metagame.py in order to time how long precomputation() took.

How to use the app:

Run Watchmaker.py.  Pick how many Pokemon you want to include in the "core" of your team and name them when prompted.  Select arbitrary population sizes and duration of computation for an evoluationary algorithm.  Wait under the program finishes computing  -- the user should see 3 suggested full teams that complete the initial "core".  The program should also print performance statistics for the full teams.




