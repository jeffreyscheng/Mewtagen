# Dialgarithm

## How to use the app:
    `python run.py`

## What it does:

Dialgarithm is a "smart" algorithm that takes in an incomplete Pokemon team (<6 team members) and gives suggestions for the remaining teammates.

## How it works (short version):

You tell the algorithm 2 things:
1. Which metagame you're playing
2. Which Pokemon you want to use

Dialgarithm then crawls Smogon's to grab all of the rules, allowed Pokemon, items, moves, etc. for your metagame.
It then grabs the current month's usage statistics in that metagame.
Finally, it crawls all of Smogon's analyses for movesets in your metagame.

The algorithm then initiates a lot of candidate teams (i.e. teams with your specified Pokemon, with all the empty slots filled with random Pokemon) and representative teams (teams randomly sampled from the usage statistics).
The candidate teams battle the representative teams until the algorithm has a good sense of the skill level of each team.  Some teams get chosen for survival, where the likelihood of surviving is dependent on skill.
Then, the algorithm creates the next generation of teams by having the surviving teams reproduce with each other.

Rinse, and repeat.  After time runs out, the algorithm spits out the most recent generation of teams, which should be much better than the initial population.

## How it works (long version):

### User Input
You tell the algorithm 2 things:
1. Which metagame you're playing
2. Which Pokemon you want to use

### Automated Input
Dialgarithm then crawls Smogon's to grab all of the rules, allowed Pokemon, items, moves, etc. for your metagame.
It then grabs the current month's usage statistics in that metagame.
Finally, it crawls all of Smogon's analyses for movesets in your metagame.


### Genetic Algorithm

#### Overview

The goal is to get the team (chromosome) with the highest probability of winning against an arbitrary team in the metagame.

#### Definitions
..* Pokemon = dex number
..* moveset = combination of Pokemon, list of moves, ev assignments, and iv assignments
..* counter (of moveset A) = some moveset that can switch into an attack from moveset A and still beat A in an attrition battle
..* arbitrary team (of metagame M) = a team whose members are randomly sampled from the usage stats of metagame M

#### Precomputation

..* a list of counters for every moveset
..* extremely accurate Elos of arbitrary teams
..* similarity indices between Pokemon (explained in reproduction)

#### Population Initialization

<Some number> teams are initialized by beginning with the user-inputted core and sampling the remaining teammates from the metagame.

#### Fitness Score

The fitness of a team is its estimated probability of beating an arbitrary team in the metagame.

The algorithm estimates the fitness of each team by battling it against 25 arbitrary and pre-rated teams using the Glicko system (a modified Elo skill rating system that also measures ratings deviation).  The battling system is a simple heurstic-based simulator: for every turn, both movesets attack each other with the move that will deal the most damage unless one moveset counters the other.  If moveset A counters moveset B, B will switch into a teammate that A does not counter if such a teammate exists.

Once the Glicko rating stabilizes, the algorithm computes the win probability for each team.

#### Reproduction

Elitism accounts for 10% of the the next generation -- any teams in the 90th percentile or above are copied into the next generation without any changes.

The algorithm produces the remaining 90% of candidate chromosomes in the next generation by sampling 2 parents for each from the previous generation, weighted by win probability.

#### Crossover

The child is guaranteed to have any genes (individual moveset) shared by both parents.  This trivially includes the user-inputted core.

The remaining genes in the chromosome are determined by via single-point crossover -- a random gene is selected as a crossover point.  The child inherits all genes before the crossover point from one parent and the remaining genes from the other.

##### Mutation

The non-core genes are then subjected to the potential of mutation.

The probability of mutating from moveset A to moveset B (given that a mutation happens) is weighted by the similarity of A and B.

I defined similarity as the product (J~s~A~,s~B~~)^7^ * (J~t~A~,t~B~~)^4^,

where J~s~A~,s~B~~ is the Jaccard similarity index of the post-ev statistics vectors of A and B
and J~t~A~,t~B~~ is the Jaccard similarity index of the defensive type effectiveness vectors of A and B.

This definition has no theoretical basis.  I created 9 tiers of similarity on two axes [same defensive type, similar defensive type, different defensive type] X [same build, similar build, different build], and arbitrarily said that movesets from one tier should be twice as likely as movesets from the tier below.
I then optimized the exponents to force-fit this arbitrary definition.

#### Output

The algorithm outputs the best 10 teams once the elite teams have remained unchanged for 10 generations or once the time threshold runs out.

I included some other analytical tools: (1) a listing of the most popular combinations of n Pokemon, and (2) a rough expectation of the damage output and # turns lasted for each moveset on a given team.

