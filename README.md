# NSMBW Any% RNG Tracker
A desktop app for tracking New Super Mario Bros. Wii's RNG in Any% speedruns, written in Python. I recommend speedrunners who are planning on using this tool to read below about how the app works, how RNG works, and how to understand some of the notation used in the app.

## Setup
1. Install **Python 3.13+** if you haven't already
2. Download the source code
3. Double-click on `main.py`

## Tracking RNG
This app tracks the runner's RNG value until they enter World 5 and spawn the overworld Piranha Plant enemies. Their positions in their respective areas are determined by RNG and can cost speedrunners up to 30 frames (0.5 seconds) in timeloss over the best-case scenario. The aim of tracking the runner's RNG is to maximize the chances of this best-case scenario occurring and prevent RNG timeloss.

The method of RNG tracking outlined in this readme works in the first place because speedrunners have figured out how to precisely set their RNG values at the start of each speedrun. This allows predictions to be made about how many times the RNG value has incremented since the start of each speedrun.

### How RNG works
NSMBW's **RNG** (Random Number Generator) is essentially a set of functions in the game's code which use and modify a number in memory, called the **RNG value**, to make this number seem random. When the RNG value is modified by an RNG function, it's said to be **incremented**. An **RNG call**, or **calling RNG**, takes place when the game calls one of the RNG functions. Thus, each RNG call increments RNG.

NSMBW's algorithm for incrementing RNG is written below, in Python:

```python
# rng_seed is a 32-bit unsigned integer

def increment_rng(rng_seed:int) -> int:
	new_value = (rng_seed * 0x19660D) + 0x3C6EF35F
	new_value += new_value >> 32
	return new_value & 0xFFFFFFFF
```
*(Note that this just represents how RNG changes when it's incremented; the actual RNG functions look a little different than this.)*

Here's a list of some ways that Mario can increment RNG:
- Mario calls RNG once per jump, per wall-jump, and per bounce off an enemy. He doesn't call RNG when spin-jumping, jumping with an object in hand, jumping while he has Star, or crouch-jumping (unless he uncrouches mid-air).
- Every time Mario breaks a brick block, RNG is incremented 13 times.

### How RNG is tracked over time

RNG is tracked by separating a speedrun in World 1 into periods of **passive play** and **observation**. Passive play happens when the player is just playing the game without paying attention to RNG-determined events, and isn't all that important. Observation happens whenever the player pays attention to RNG-determined events and uses them to narrow down the set of plausible RNG values. A **plausible RNG value** is simply an RNG value that *could* match the RNG value actually stored in memory, given the observed RNG-determined events.

During 1-1, the player's RNG value almost immediately becomes uncertain (more on 1-1 RNG below) and RNG observation is impractical until 1-3. To account for the uncertainty caused by 1-1, the app generates a set of plausible RNG values which depend on how long the player spent in the second half of 1-1. This set is later tested against Hammer Bro attack patterns in 1-3 and narrowed down considerably. RNG observation becomes impractical from this point until entering World 5. Because of this, the app generates a list of the probabilities that the World 5 overworld enemies are in their optimal positions, given how many times Mario jumps in 1-Cannon.

### RNG in 1-1
1-1 is an RNG nightmare. There are eight cloud sprites scattered throughout the second half of the level, each of which increments RNG 75 times per frame (or 4,500 times per second) while on-screen. Since more than one of these cloud sprites tends to be on-screen at once, there are sections of the level in which RNG increments tens of thousands of times per second. In a typical speedrun through 1-1, RNG is called at least 200,000 times.

I figured out while researching this level's RNG calls that speedruns of 1-1 tend to have an *average RNG call rate* between 150 and 225 RNG calls per frame (between 9,000 and 13,500 RNG calls per second). This gives us a lower and upper bound for estimating the player's RNG value. The app applies these bounds to the amount of time between grabbing the checkpoint flag and grabbing the flagpole to account for the player's actual RNG value.

Additionally, Mario doesn't call RNG when jumping while holding a Koopa shell.

There are a few other RNG calls in 1-1 that aren't important to know for using the app, but here they are anyway:
- 1 RNG call every time a Goomba spawns,
- 196 RNG calls when loading into the level (after the level banner), and
- 225 RNG calls on every cloud sprite's first frame on-screen (on top of the prior 75 RNG calls per frame).

### RNG in 1-2
1-2's RNG is much tamer than 1-1's. The only RNG calls of note to keep track of are (out-of-star) jumps and the number of brick blocks broken.

### RNG in 1-3 (Secret Exit)
1-3 gives us the perfect opportunity to observe RNG-determined events and narrow down the set of plausible RNG values. This is possible thanks to the two useful Hammer Bros in 1-3.

#### Hammer Bro RNG

There are two lists which are important to know regarding how each Hammer Bro calls RNG: the **Hammer Throw Cycle** and the **Jump Timer List**.

The Hammer Throw Cycle (HTC) is shown below. Each Hammer Bro calls RNG to generate a random index to this list and stores the HTC value at that index in memory, which determines how many hammers it will throw when it next decides to throw hammers. For example: if a Hammer Bro's HTC index is 2 it'll throw three hammers, and if its HTC index is 4 it'll throw one hammer. When a Hammer Bro decides to throw hammers, its HTC index increases by 1 beforehand. Each Hammer Bro's HTC index also determines how long it will wait until throwing hammers (its Throw Timer), shown in the third row in the below table, which doesn't actually exist anywhere in memory. For example, if a Hammer Bro's HTC index is 2, it will stall for 45 frames before attempting to throw hammers.

<table>
	<tr>
		<th>Hammer Throw Cycle</th>
	</tr>
	<tr>
		<th>List Index</th>
		<td>0</td>
		<td>1</td>
		<td>2</td>
		<td>3</td>
		<td>4</td>
		<td>5</td>
		<td>6</td>
		<td>7</td>
	</tr>
	<tr>
		<th>Hammer Throws</th>
		<td>3</td>
		<td>1</td>
		<td>3</td>
		<td>3</td>
		<td>1</td>
		<td>3</td>
		<td>1</td>
		<td>3</td>
	</tr>
	<tr>
		<th>Throw Timer</th>
		<td>45</td>
		<td>30</td>
		<td>45</td>
		<td>45</td>
		<td>30</td>
		<td>45</td>
		<td>30</td>
		<td>45</td>
	</tr>
</table>

The Jump Timer List (JTL) is shown below. Each Hammer Bro calls RNG to generate a random index to this list every time it lands on solid ground. The first time a Hammer Bro generates a JTL index, it stores half the element at that index in memory. For example: if a Hammer Bro generates a JTL index of 2, its Jump Timer is set to 45 frames, even though the value at index 2 of the JTL is 90. This is represented in the third row in the below table, which (again) doesn't actually exist in memory.

<table>
	<tr>
		<th>Jump Timer List</th>
	</tr>
	<tr>
		<th>List Index</th>
		<td>0</td>
		<td>1</td>
		<td>2</td>
		<td>3</td>
	</tr>
	<tr>
		<th>Jump Timer</th>
		<td>90</td>
		<td>110</td>
		<td>90</td>
		<td>100</td>
	</tr>
	<tr>
		<th>Jump Timer (First Pass)</th>
		<td>45</td>
		<td>55</td>
		<td>45</td>
		<td>50</td>
	</tr>
</table>

If a Hammer Bro's Throw Timer is equal to its Jump Timer, then **jumping takes priority over throwing hammers**. This is why the Hammer Bros in 1-3 sometimes jump early before throwing hammers. If a Hammer Bro's Throw Timer is less than its Jump Timer, then it will throw hammers normally.
Each Hammer Bro's Jump Timer is paused while it's throwing hammers and resumes when it's done throwing hammers. This is why some Hammer Bro attack patterns last way longer than 55 frames despite 55 being the maximum effective value in the JTL.

#### Hammer Bro RNG notation
The notation used in the app for Hammer Bro RNG follows the format **(Hammer Bro Cycle Start - Hammer Throws - Jump Timer)**, with "X" as a placeholder value for unknown variables. Below are all the different observable attack patterns:
- **1-3-X** means the Hammer Bro started the HTC on 1 hammer throw (waited 30 frames), threw 3 hammers before jumping, and started its attack pattern with an unknown Jump Timer.
- **3-3-X** means the Hammer Bro started the HTC on 3 hammer throws (waited 45 frames), threw 3 hammers before jumping, and started its attack pattern with an unknown Jump Timer.
- **3-X-45** means the Hammer Bro started the HTC on 3 hammer throws (waited 45 frames), didn't get to throw hammers before jumping, and started its attack pattern with a Jump Timer of 45 frames. (This is the early-jump attack pattern.)
- **3-1-50** means the Hammer Bro started the HTC on 3 hammer throws (waited 45 frames), threw 1 hammer before jumping, and started its attack pattern with a Jump Timer of 50 frames. (The visual cue I use for 3-1-50 is the Hammer Bro jumping while facing toward the screen.)
- **3-1-55** means the Hammer Bro started the HTC on 3 hammer throws (waited 45 frames), threw 1 hammer before jumping, and started its attack pattern with a Jump Timer of 55 frames. (The visual cue I use for 3-1-50 is the Hammer Bro jumping while facing to the right.)

### 1-Cannon
From the uncertainty caused by 1-1 and the observation of Hammer Bro attack patterns in 1-3, the app generates multiple probabilities for how likely the World 5 overworld enemies are to be in their optimal positions, with different probabilities for a different number of jumps in 1-Cannon. The app automatically calculates these probabilities when switching tabs, so you don't have to worry about hitting a "Calculate" button or anything of that sort.
