
# rng.py

from __future__ import annotations

RANDOM_A = 0x19660D
RANDOM_B = 0x3C6EF35F

def increment_seed(seed:int, times:int) -> int:
    for _ in range(times):
        calc = (seed * RANDOM_A) + RANDOM_B
        calc += calc >> 32
        seed = calc & 0xFFFFFFFF

    return seed

def get_uint32(seed:int, max:int) -> int:
    calc = (seed * RANDOM_A) + RANDOM_B
    calc += calc >> 32
    calc = calc & 0xFFFFFFFF

    randint = (calc * max) >> 32
    return randint

def attempt_randint_sequence(seed:int, sequence:list) -> int | None:
    i = 0
    for entry in sequence:
        pre_increment = entry[0]
        randint_max = entry[1][0]
        randint_expected = entry[1][1]

        seed = increment_seed(seed, pre_increment)
        randint = get_uint32(seed, randint_max)
        seed = increment_seed(seed, 1)

        if randint not in randint_expected:
            return

        i += pre_increment + 1

    return seed

class Batch:
    def __init__(self, rng_seeds:list[int] = [],
                 rng_seed_weights:list[float] = []):
        self.rng_seeds = [seed for seed in rng_seeds]
        self.rng_seed_weights = [weight for weight in rng_seed_weights]

    def set_seed_weights(self, new_seed_weights:list[float]) -> bool:
        if len(new_seed_weights) != len(self.rng_seed_weights): return False

        self.rng_seed_weights = new_seed_weights
        return True

    def add_rng_seeds(self, new_rng_seeds:list[int]) -> None:
        self.rng_seeds += new_rng_seeds

    def prune_rng_seeds(self, sequence:list) -> Batch:
        new_rng_seeds = []
        new_rng_seed_weights = []
        for s in range(len(self.rng_seeds)):
            seed = self.rng_seeds[s]
            weight = self.rng_seed_weights[s]

            new_seed = attempt_randint_sequence(seed, sequence)
            if new_seed == None: continue

            new_rng_seeds.append(new_seed)
            new_rng_seed_weights.append(weight)

        new_batch = Batch(new_rng_seeds, new_rng_seed_weights)
        return new_batch

    def get_sequence_probability(self, sequence:list) -> float:
        if len(self.rng_seeds) == 0: return 0.

        res = 0
        amount = 0
        for s in range(len(self.rng_seeds)):
            seed = self.rng_seeds[s]
            weight = self.rng_seed_weights[s]

            amount += weight
            if attempt_randint_sequence(seed, sequence) == None: continue
            res += weight

        if amount == 0: return 0.
        return res / amount
