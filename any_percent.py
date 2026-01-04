
# any_percent.py

from rng import increment_seed, Batch

def get_frames_from_igts(start_igt:int | float, end_igt:float | int) -> int:
    frames = round((start_igt - end_igt) * 4096/92)
    return frames

class AnyPercentRNG:
    RNG_SEED = increment_seed(0xE61F8379, 298) # 1-2 Super Guide RNG seed

    def __init__(self):
        self.rng_batch = Batch([], [])
        self.rng_sequence = []
        self.potential_rng = Batch([], [])

    def _1_1(self, jumps:int, bricks_broken:int, checkpoint_igt:float,
             flagpole_igt:float, igt_error_margin:float,
             did_grab_prop:bool) -> Batch:
        """
        Generates and returns an RNG batch from gameplay in 1-1.

        -----

        Each cloud sprite in 1-1 calls RNG 75 times per frame when within 64
        units horizontally of the camera. These RNG calls start about a dozen
        tiles left of where the checkpoint flag is, or about a second before
        speedrunners hit the checkpoint flag. This means that RNG is called
        hundreds of thousands of times in 1-1.

        It's possible to estimate how many times the cloud sprites call RNG in
        1-1 by taking the time difference between the checkpoint and the
        flagpole. Throughout the second half of 1-1, there are an average of
        ~2.5 cloud sprites on screen on average, give or take depending on how
        the level is played.

        This RNG call estimation method assumes that between 2 and 3 cloud
        sprites are on-screen every frame for the second half of 1-1, and
        generates a list of plausible RNG values accordingly. In other words,
        the longer 1-1 is played, the more potential RNG values are generated.

        One limitation to this method is that both the lower and upper bounds
        are designed to be highly unrealistic for speedruns, leaving the
        realistic RNG values near the middle. This is useful for ensuring the
        correct RNG value is accounted for, but the unrealistic RNG values can
        overrepresent future RNG probabilities (e.g. the chance of spawning
        the World 5 piranha plants optimally). This limitation could probably
        be overcome by applying a bell curve to future RNG probabilities, but
        I'm not smart enough to implement that myself.
        """

        CONFIRMED_RNG_CALLS = 36_076 + jumps + (13 * bricks_broken)
        START_IGT = 500
        IGT_CONVERSION_FACTOR = 4096/92

        checkpoint_igts = [
            START_IGT - (checkpoint_igt + igt_error_margin),
            START_IGT - (checkpoint_igt - igt_error_margin)
        ]
        flagpole_igts = [
            START_IGT - (flagpole_igt + igt_error_margin),
            START_IGT - (flagpole_igt - igt_error_margin)
        ]

        second_half_igts = [
            flagpole_igts[1] - checkpoint_igts[0],
            flagpole_igts[0] - checkpoint_igts[1]
        ]
        second_half_frames = [
            round(second_half_igts[0] * IGT_CONVERSION_FACTOR),
            round(second_half_igts[1] * IGT_CONVERSION_FACTOR)
        ]
        second_half_rng_events = [
            2 * (second_half_frames[0] - (30 * (did_grab_prop + 1))),
            3 * (second_half_frames[1] - (30 * (did_grab_prop + 1)))
        ]

        rng_seed = increment_seed(
            self.RNG_SEED,
            CONFIRMED_RNG_CALLS + (75 * second_half_rng_events[0])
        )
        rng_diff = second_half_rng_events[1] - second_half_rng_events[0]

        batch_seeds = [
            rng_seed := increment_seed(rng_seed, 75) for _ in range(rng_diff)
        ]
        batch_weights = [
            (3 * n/rng_diff) * (((3 * n/rng_diff) - 3) ** 2) / 4
            for n in range(rng_diff)
        ]

        self.rng_batch = Batch(batch_seeds, batch_weights)
        return self.rng_batch

    def _1_2(self, jumps:int, bricks_broken:int,
             did_hit_ice_flower_block:bool) -> Batch:
        """
        Calculates and returns an updated RNG batch from gameplay in 1-2.

        -----

        The ? block at the start of the underground section of 1-2, with the
        Ice Flower in it, can call RNG. Specifically, when the powerup inside
        pops out, it calls RNG twice to determine its velocity (one RNG call
        for X velocity, the other for Y velocity). Since its exact velocity
        isn't easily observable in a speedrun, I just count it as two regular
        RNG calls.
        """

        CONFIRMED_RNG_CALLS = 58 + jumps + (13 * bricks_broken)

        total_rng_calls = CONFIRMED_RNG_CALLS + (2 * did_hit_ice_flower_block)
        sequence = [
            [total_rng_calls - 1, [1, [0]]]
        ]
        self.potential_rng = self.rng_batch.prune_rng_seeds(sequence)

        return self.potential_rng

    def get_hammer_bro_sequence(self, prior_jumps:int, between_jumps:int,
                                throw_timer:int, jump_timer:int, throws:int,
                                does_hammer_bro_jump_throw:bool,
                                does_mario_kill_hammer_bro:bool) -> list:
        """
        Generates and returns an RNG sequence for a Hammer Bro given its
        attack pattern and other gameplay context.
        """

        if throw_timer not in (30, 45): return []

        if throw_timer == 30: # Hammer Bro spawned on a 1-hammer
            throw_cycle_randint_entry = [8, [1, 4, 6]]
            jump_timer_randint_entry = [4, [0, 1, 2, 3]]

            sequence = [
                [prior_jumps, throw_cycle_randint_entry],
                [0, jump_timer_randint_entry],
                [between_jumps + 1, [1, [0]]]
            ]
            return sequence

        # Hammer Bro spawned on a 3-hammer

        jump_attack_randint_entry = [2, [int(not does_hammer_bro_jump_throw)]]

        if jump_timer == 45: # Hammer Bro jumped early
            throw_cycle_randint_entry = [8, [0, 2, 3, 5, 7]]
            jump_timer_randint_entry = [4, [0, 2]]

            sequence = [
                [prior_jumps, throw_cycle_randint_entry],
                [0, jump_timer_randint_entry],
                [between_jumps + 1, jump_attack_randint_entry],
            ]
            if not does_mario_kill_hammer_bro:
                # RNG is called an extra time because Hammer Bro landed
                sequence += [
                    [0, [1, [0]]]
                ]

            return sequence

        if throws not in (1, 3): return []

        if throws == 3: # Hammer Bro jumps off-screen
            throw_cycle_randint_entry = [8, [2, 7]]
            jump_timer_randint_entry = [4, [0, 1, 2, 3]]

            sequence = [
                [prior_jumps, throw_cycle_randint_entry],
                [0, jump_timer_randint_entry],
                [between_jumps + 1, [1, [0]]]
            ]
            return sequence

        if jump_timer not in (50, 55): return []

        if throws == 1: # Hammer Bro jumps after Mario passes it
            throw_cycle_randint_entry = [8, [0, 3, 5]]
            jump_timer_randint_entry = [4, [3 if jump_timer == 50 else 1]]

            sequence = [
                [prior_jumps, throw_cycle_randint_entry],
                [0, jump_timer_randint_entry],
                [between_jumps + 1, jump_attack_randint_entry]
            ]
            return sequence

        return []

    def _1_3_S(self, first_bro_prior_jumps:int, first_bro_between_jumps:int,
               first_bro_throw_timer:int, first_bro_jump_timer:int,
               first_bro_throws:int, does_first_bro_jump_throw:bool,
               does_first_bro_die:bool, second_bro_prior_jumps:int,
               second_bro_between_jumps:int, second_bro_throw_timer:int,
               second_bro_jump_timer:int, second_bro_throws:int,
               does_second_bro_jump_throw:bool, does_second_bro_die:bool,
               total_jumps:int, bricks_broken_after_both_bros:int) -> Batch:
        """
        Generates and returns a new RNG batch for 1-3 from Hammer Bro RNG and
        gameplay in 1-3.

        -----

        RNG tracking is possible for Any% speedruns only because of the Hammer
        Bros in 1-3. Observing their initial attack patterns requires very
        little extra effort, and they narrow down the batch of plausible RNG
        values by at least several hundred. The more unlikely the Hammer Bro
        attack patterns observed, the more the batch of RNG values are
        narrowed down.

        However, for this to work properly, Yoshi can't spawn. Yoshi calls RNG
        seemingly randomly while he's in existence, and he doesn't despawn
        when he goes off-screen. I don't know how to account for Yoshi's RNG,
        so please don't spawn Yoshi.
        """

        second_bro_prior_jumps -= first_bro_prior_jumps + \
            first_bro_between_jumps
        remaining_jumps = total_jumps - first_bro_prior_jumps - \
            first_bro_between_jumps - second_bro_prior_jumps - \
            second_bro_between_jumps

        # 89 RNG calls when loading 1-3
        CONFIRMED_START_RNG_CALLS = 89 + first_bro_prior_jumps

        # 14 RNG calls from Goombas spawning
        CONFIRMED_MIDDLE_RNG_CALLS = 14 + second_bro_prior_jumps

        # 159 RNG calls from Goombas spawning, extra Hammer Bros spawning, the
        # pipe transition, World 1 overworld RNG after 1-3, and loading
        # 1-Cannon
        CONFIRMED_END_RNG_CALLS = 159 + remaining_jumps + \
            (13 * bricks_broken_after_both_bros)

        first_hammer_bro_sequence = self.get_hammer_bro_sequence(
            CONFIRMED_START_RNG_CALLS, first_bro_between_jumps,
            first_bro_throw_timer, first_bro_jump_timer, first_bro_throws,
            does_first_bro_jump_throw, does_first_bro_die
        )
        second_hammer_bro_sequence = self.get_hammer_bro_sequence(
            CONFIRMED_MIDDLE_RNG_CALLS, second_bro_between_jumps,
            second_bro_throw_timer, second_bro_jump_timer, second_bro_throws,
            does_second_bro_jump_throw, does_second_bro_die
        )
        end_sequence = [
            [CONFIRMED_END_RNG_CALLS - 1, [1, [0]]]
        ]

        self.sequence = first_hammer_bro_sequence + \
            second_hammer_bro_sequence + end_sequence
        self.potential_rng = self.potential_rng.prune_rng_seeds(self.sequence)

        return self.potential_rng

    def calculate_piranha_probabilities(self, max_jumps:int) -> list[float]:
        """
        Calculates and returns the probability of being on an RNG value which
        will spawn the World 5 piranha plants optimally, for each extra jump
        past the 1-3 pipe.
        """

        WORLD_5_RNG_CALLS = 9

        probabilities = []
        for jumps in range(max_jumps + 1):
            piranha_sequence = [
                [WORLD_5_RNG_CALLS + jumps, [1, [0]]],
                [0, [4, [1]]],
                [0, [4, [2, 3]]]
            ]

            probabilities.append(self.potential_rng.get_sequence_probability(
                piranha_sequence
            ))

        return probabilities
