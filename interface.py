
# interface.py

from any_percent import AnyPercentRNG
from rng import increment_seed, Batch

from tkinter import ttk
import tkinter as tk
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IGT_OFFSETS = {'Low': 0.167, 'Mid': 0.500, 'High': 0.833}
IGT_RANGES = {0.167: 'Low', 0.500: 'Mid', 0.833: 'High'}

class AnyPercentInterface:
    class _1_1_Data:
        def __init__(self, jumps:int = 28, bricks_broken:int = 0,
                     checkpoint_igt:float = 482.833,
                     flagpole_igt:float = 455.500, did_grab_prop:bool = True):
            self.jumps = jumps
            self.bricks_broken = bricks_broken
            self.checkpoint_igt = checkpoint_igt
            self.flagpole_igt = flagpole_igt
            self.igt_error_margin = 0.167
            self.did_grab_prop = did_grab_prop

    class _1_2_Data:
        def __init__(self, jumps:int = 17, bricks_broken:int = 4,
                     did_hit_ice_flower_block:bool = True):
            self.jumps = jumps
            self.bricks_broken = bricks_broken
            self.did_hit_ice_flower_block = did_hit_ice_flower_block

    class _1_3_Data:
        def __init__(self, first_bro_prior_jumps:int = 2,
                     first_bro_between_jumps:int = 2,
                     second_bro_prior_jumps:int = 9,
                     second_bro_between_jumps:int = 2,
                     jumps_after_both_bros:int = 8,
                     bricks_broken_after_both_bros:int = 0):
            self.first_bro_prior_jumps = first_bro_prior_jumps
            self.first_bro_between_jumps = first_bro_between_jumps
            self.second_bro_prior_jumps = second_bro_prior_jumps
            self.second_bro_between_jumps = second_bro_between_jumps
            self.jumps_after_both_bros = jumps_after_both_bros
            self.bricks_broken_after_both_bros = bricks_broken_after_both_bros

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Any% RNG Tracker')
        self.root.geometry('480x360+0+0')
        self.root.minsize(480, 320)
        self.root.maxsize(640, 480)
        self.root.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.rng = AnyPercentRNG()
        self.import_defaults()

        # Setup begin

        self.frame = ttk.Frame(self.root)
        self.frame.grid(column=0, row=0, sticky='NSEW')

        notebook = ttk.Notebook(self.frame)
        notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
        _1_1_frame = ttk.LabelFrame(notebook, text='1-1')
        _1_2_frame = ttk.LabelFrame(notebook, text='1-2')
        _1_3_frame = ttk.LabelFrame(notebook, text='1-3 Secret')
        W5_rng_frame = ttk.LabelFrame(notebook, text='World 5 RNG')

        _1_1_igt_frame = ttk.Frame(_1_1_frame)
        _1_3_first_bro_frame = ttk.Frame(_1_3_frame)
        _1_3_second_bro_frame = ttk.Frame(_1_3_frame)
        _1_3_first_pattern_frame = ttk.Frame(_1_3_first_bro_frame)
        _1_3_second_pattern_frame = ttk.Frame(_1_3_second_bro_frame)
        _1_1_igt_frame.grid(column=0, columnspan=2, row=2, sticky='NSEW')
        _1_3_first_bro_frame.grid(column=0, row=0, sticky='NSEW')
        _1_3_second_bro_frame.grid(column=1, row=0, sticky='NSEW')
        _1_3_first_pattern_frame.grid(
            column=0, columnspan=2, row=2, sticky='NSEW'
        )
        _1_3_second_pattern_frame.grid(
            column=0, columnspan=2, row=2, sticky='NSEW'
        )

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        for d in range(4):
            _1_1_frame.grid_rowconfigure(d, weight=1)

            if d >= 3: continue

            _1_2_frame.grid_rowconfigure(d, weight=1)
            _1_3_frame.grid_rowconfigure(d, weight=1)
            W5_rng_frame.grid_columnconfigure(d, weight=1)

            _1_1_igt_frame.grid_columnconfigure(d, weight=1)
            _1_3_first_bro_frame.grid_columnconfigure(d, weight=1)
            _1_3_first_bro_frame.grid_rowconfigure(d, weight=1)
            _1_3_second_bro_frame.grid_columnconfigure(d, weight=1)
            _1_3_second_bro_frame.grid_rowconfigure(d, weight=1)
            _1_3_first_pattern_frame.grid_columnconfigure(d, weight=1)
            _1_3_second_pattern_frame.grid_columnconfigure(d, weight=1)

            if d >= 2: continue

            notebook.grid_columnconfigure(d, weight=1)
            notebook.grid_rowconfigure(d, weight=1)
            _1_1_frame.grid_columnconfigure(d, weight=1)
            _1_2_frame.grid_columnconfigure(d, weight=1)
            _1_3_frame.grid_columnconfigure(d, weight=1)
            W5_rng_frame.grid_rowconfigure(d, weight=1)

            _1_1_igt_frame.grid_rowconfigure(d, weight=1)
            _1_3_first_pattern_frame.grid_rowconfigure(d, weight=1)
            _1_3_second_pattern_frame.grid_rowconfigure(d, weight=1)

        # 1-1 tab begin

        _1_1_jumps_label = ttk.Label(_1_1_frame, text='Jumps*')
        _1_1_jumps_asterisk = ttk.Label(
            _1_1_frame, font=(None, 8),
            text='*excluding holding-shell, spin, and crouch jumps.'
        )
        _1_1_jumps_counter = ttk.Spinbox(
            _1_1_frame, from_=0, to=50, textvariable=self._1_1_jumps_var,
            width=5, state='readonly'
        )
        _1_1_jumps_label.grid(column=0, row=0)
        _1_1_jumps_asterisk.grid(column=0, columnspan=2, row=5, pady=5)
        _1_1_jumps_counter.grid(column=1, row=0)

        _1_1_bricks_label = ttk.Label(_1_1_frame, text='Brick blocks broken')
        _1_1_bricks_counter = ttk.Spinbox(
            _1_1_frame, from_=0, to=4, textvariable=self._1_1_bricks_var,
            width=5, state='readonly'
        )
        _1_1_bricks_label.grid(column=0, row=1)
        _1_1_bricks_counter.grid(column=1, row=1)

        # 1-1 IGT frame

        igt_range_values = ['Low', 'Mid', 'High']

        _1_1_checkpoint_igt_label = ttk.Label(
            _1_1_igt_frame, text='Checkpoint IGT'
        )
        _1_1_checkpoint_igt_range = ttk.Combobox(
            _1_1_igt_frame, textvariable=self._1_1_checkpoint_igt_range_var,
            values=igt_range_values, width=5, state='readonly'
        )
        _1_1_checkpoint_igt_counter = ttk.Spinbox(
            _1_1_igt_frame, from_=455, to=486,
            textvariable=self._1_1_checkpoint_igt_var,
            width=7, state='readonly'
        )
        _1_1_checkpoint_igt_label.grid(column=0, row=0, sticky='E')
        _1_1_checkpoint_igt_range.grid(column=1, row=0, sticky='E')
        _1_1_checkpoint_igt_counter.grid(column=2, row=0, sticky='W')

        _1_1_flagpole_igt_label = ttk.Label(
            _1_1_igt_frame, text='Flagpole IGT'
        )
        _1_1_flagpole_igt_range = ttk.Combobox(
            _1_1_igt_frame, textvariable=self._1_1_flagpole_igt_range_var,
            values=igt_range_values, width=5, state='readonly'
        )
        _1_1_flagpole_igt_counter = ttk.Spinbox(
            _1_1_igt_frame, from_=455, to=486,
            textvariable=self._1_1_flagpole_igt_var,
            width=7, state='readonly'
        )
        _1_1_flagpole_igt_label.grid(column=0, row=1, sticky='E')
        _1_1_flagpole_igt_range.grid(column=1, row=1, sticky='E')
        _1_1_flagpole_igt_counter.grid(column=2, row=1, sticky='W')

        # 1-1 tab finish

        _1_1_grab_prop_label = ttk.Label(_1_1_frame, text='Grabbed prop?')
        _1_1_grab_prop_check = ttk.Checkbutton(
            _1_1_frame, variable=self._1_1_grabbed_prop_var
        )
        _1_1_grab_prop_label.grid(column=0, row=3)
        _1_1_grab_prop_check.grid(column=1, row=3)

        _1_1_set_defaults_button = ttk.Button(
            _1_1_frame, text='Set Defaults', command=self.set_1_1_defaults
        )
        _1_1_load_defaults_button = ttk.Button(
            _1_1_frame, text='Load Defaults', command=self.load_1_1_defaults
        )
        _1_1_set_defaults_button.grid(column=0, row=4, padx=5, sticky='SE')
        _1_1_load_defaults_button.grid(column=1, row=4, padx=5, sticky='SW')

        # 1-2 tab

        self._1_2_jumps_var = tk.StringVar(value=str(self._1_2.jumps))
        _1_2_jumps_label = ttk.Label(_1_2_frame, text='Jumps*')
        _1_2_jumps_asterisk = ttk.Label(
            _1_2_frame, font=(None, 8),
            text='*excluding star and crouch jumps.'
        )
        _1_2_jumps_counter = ttk.Spinbox(
            _1_2_frame, from_=0, to=50, textvariable=self._1_2_jumps_var,
            width=5, state='readonly'
        )
        _1_2_jumps_label.grid(column=0, row=0)
        _1_2_jumps_asterisk.grid(column=0, columnspan=2, row=4, pady=5)
        _1_2_jumps_counter.grid(column=1, row=0)

        self._1_2_bricks_var = tk.StringVar(
            value=str(self._1_2.bricks_broken)
        )
        _1_2_bricks_label = ttk.Label(_1_2_frame, text='Brick blocks broken')
        _1_2_bricks_counter = ttk.Spinbox(
            _1_2_frame, from_=0, to=7, textvariable=self._1_2_bricks_var,
            width=5, state='readonly'
        )
        _1_2_bricks_label.grid(column=0, row=1)
        _1_2_bricks_counter.grid(column=1, row=1)

        self._1_2_ice_block_var = tk.BooleanVar(
            value=self._1_2.did_hit_ice_flower_block
        )
        _1_2_ice_block_label = ttk.Label(
            _1_2_frame, text='Hit the first [?] block?'
        )
        _1_2_ice_block_check = ttk.Checkbutton(
            _1_2_frame, variable=self._1_2_ice_block_var
        )
        _1_2_ice_block_label.grid(column=0, row=2)
        _1_2_ice_block_check.grid(column=1, row=2)

        _1_2_set_defaults_button = ttk.Button(
            _1_2_frame, text='Set Defaults', command=self.set_1_2_defaults
        )
        _1_2_load_defaults_button = ttk.Button(
            _1_2_frame, text='Load Defaults', command=self.load_1_2_defaults
        )
        _1_2_set_defaults_button.grid(column=0, row=3, padx=5, sticky='SE')
        _1_2_load_defaults_button.grid(column=1, row=3, padx=5, sticky='SW')

        # 1-3 tab begin

        _1_3_pattern_values = [
            '1-3-X', '3-3-X',  # No-jump patterns
            '3-X-45',          # Early-jump pattern
            '3-1-50', '3-1-55' # Late-jump patterns
        ]

        # Hammer Bro #1 frame

        self._1_3_first_prior_jumps_var = tk.StringVar(
            value=str(self._1_3.first_bro_prior_jumps)
        )
        _1_3_first_prior_jumps_label = ttk.Label(
            _1_3_first_bro_frame, text='Jumps before spawning\nHammer Bro #1'
        )
        _1_3_first_prior_jumps_counter = ttk.Spinbox(
            _1_3_first_bro_frame, from_=0, to=5,
            textvariable=self._1_3_first_prior_jumps_var,
            width=5, state='readonly'
        )
        _1_3_first_prior_jumps_label.grid(column=0, row=0)
        _1_3_first_prior_jumps_counter.grid(column=1, row=0)

        self._1_3_first_between_jumps_var = tk.StringVar(
            value=str(self._1_3.first_bro_between_jumps)
        )
        _1_3_first_between_jumps_label = ttk.Label(
            _1_3_first_bro_frame,
            text='Jumps before end of\nHammer Bro #1 pattern'
        )
        _1_3_first_between_jumps_counter = ttk.Spinbox(
            _1_3_first_bro_frame, from_=0, to=5,
            textvariable=self._1_3_first_between_jumps_var,
            width=5, state='readonly'
        )
        _1_3_first_between_jumps_label.grid(column=0, row=1)
        _1_3_first_between_jumps_counter.grid(column=1, row=1)

        # Hammer Bro #1 attack pattern frame

        self._1_3_first_pattern_var = tk.StringVar(value='1-3-X')
        self._1_3_first_bro_kill_var = tk.BooleanVar(value=False)
        self._1_3_first_bro_jump_throw_var = tk.BooleanVar(value=False)

        _1_3_first_pattern_label = ttk.Label(
            _1_3_first_pattern_frame, text='Hammer Bro #1\nattack pattern'
        )
        _1_3_first_pattern_dropdown = ttk.Combobox(
            _1_3_first_pattern_frame,
            textvariable=self._1_3_first_pattern_var,
            values=_1_3_pattern_values, width=10, state='readonly'
        )
        _1_3_first_bro_kill_label = ttk.Label(
            _1_3_first_pattern_frame, text='Killed?'
        )
        _1_3_first_bro_kill_check = ttk.Checkbutton(
            _1_3_first_pattern_frame, variable=self._1_3_first_bro_kill_var
        )
        _1_3_first_bro_jump_throw_label = ttk.Label(
            _1_3_first_pattern_frame, text='Jump-threw?'
        )
        _1_3_first_bro_jump_throw_check = ttk.Checkbutton(
            _1_3_first_pattern_frame,
            variable=self._1_3_first_bro_jump_throw_var
        )

        _1_3_first_pattern_label.grid(column=0, row=0)
        _1_3_first_pattern_dropdown.grid(column=0, row=1)
        _1_3_first_bro_jump_throw_label.grid(column=1, row=0)
        _1_3_first_bro_jump_throw_check.grid(column=1, row=1)
        _1_3_first_bro_kill_label.grid(column=2, row=0)
        _1_3_first_bro_kill_check.grid(column=2, row=1)

        # Hammer Bro #2 frame

        self._1_3_second_prior_jumps_var = tk.StringVar(
            value=str(self._1_3.second_bro_prior_jumps)
        )
        _1_3_second_prior_jumps_label = ttk.Label(
            _1_3_second_bro_frame, text='Jumps before spawning\nHammer Bro #2'
        )
        _1_3_second_prior_jumps_counter = ttk.Spinbox(
            _1_3_second_bro_frame, from_=0, to=20,
            textvariable=self._1_3_second_prior_jumps_var,
            width=5, state='readonly'
        )
        _1_3_second_prior_jumps_label.grid(column=0, row=0)
        _1_3_second_prior_jumps_counter.grid(column=1, row=0)

        self._1_3_second_between_jumps_var = tk.StringVar(
            value=str(self._1_3.second_bro_between_jumps)
        )
        _1_3_second_between_jumps_label = ttk.Label(
            _1_3_second_bro_frame,
            text='Jumps before end of\nHammer Bro #2 pattern'
        )
        _1_3_second_between_jumps_counter = ttk.Spinbox(
            _1_3_second_bro_frame, from_=0, to=5,
            textvariable=self._1_3_second_between_jumps_var,
            width=5, state='readonly'
        )
        _1_3_second_between_jumps_label.grid(column=0, row=1)
        _1_3_second_between_jumps_counter.grid(column=1, row=1)

        # Hammer Bro #2 attack pattern frame

        self._1_3_second_pattern_var = tk.StringVar(value='1-3-X')
        self._1_3_second_bro_kill_var = tk.BooleanVar(value=False)
        self._1_3_second_bro_jump_throw_var = tk.BooleanVar(value=False)

        _1_3_second_pattern_label = ttk.Label(
            _1_3_second_pattern_frame, text='Hammer Bro #2\nattack pattern'
        )
        _1_3_second_pattern_dropdown = ttk.Combobox(
            _1_3_second_pattern_frame,
            textvariable=self._1_3_second_pattern_var,
            values=_1_3_pattern_values, width=10, state='readonly'
        )
        _1_3_second_bro_kill_label = ttk.Label(
            _1_3_second_pattern_frame, text='Killed?'
        )
        _1_3_second_bro_kill_check = ttk.Checkbutton(
            _1_3_second_pattern_frame, variable=self._1_3_second_bro_kill_var
        )
        _1_3_second_bro_jump_throw_label = ttk.Label(
            _1_3_second_pattern_frame, text='Jump-threw?'
        )
        _1_3_second_bro_jump_throw_check = ttk.Checkbutton(
            _1_3_second_pattern_frame,
            variable=self._1_3_second_bro_jump_throw_var
        )

        _1_3_second_pattern_label.grid(column=0, row=0)
        _1_3_second_pattern_dropdown.grid(column=0, row=1)
        _1_3_second_bro_jump_throw_label.grid(column=1, row=0)
        _1_3_second_bro_jump_throw_check.grid(column=1, row=1)
        _1_3_second_bro_kill_label.grid(column=2, row=0)
        _1_3_second_bro_kill_check.grid(column=2, row=1)

        # 1-3 tab finish

        self._1_3_remaining_jumps_var = tk.StringVar(
            value=str(self._1_3.jumps_after_both_bros)
        )
        _1_3_remaining_jumps_label = ttk.Label(
            _1_3_frame, text='Remaining jumps'
        )
        _1_3_remaining_jumps_counter = ttk.Spinbox(
            _1_3_frame, from_=0, to=15,
            textvariable=self._1_3_remaining_jumps_var,
            width=5, state='readonly'
        )
        _1_3_remaining_jumps_label.grid(column=0, row=1)
        _1_3_remaining_jumps_counter.grid(column=1, row=1)

        self._1_3_remaining_bricks_var = tk.StringVar(
            value=str(self._1_3.bricks_broken_after_both_bros)
        )
        _1_3_remaining_bricks_label = ttk.Label(
            _1_3_frame, text='Remaining broken brick blocks'
        )
        _1_3_remaining_bricks_counter = ttk.Spinbox(
            _1_3_frame, from_=0, to=15,
            textvariable=self._1_3_remaining_bricks_var,
            width=5, state='readonly'
        )
        _1_3_remaining_bricks_label.grid(column=0, row=2)
        _1_3_remaining_bricks_counter.grid(column=1, row=2)

        _1_3_set_defaults_button = ttk.Button(
            _1_3_frame, text='Set Defaults', command=self.set_1_3_defaults
        )
        _1_3_load_defaults_button = ttk.Button(
            _1_3_frame, text='Load Defaults', command=self.load_1_3_defaults
        )
        _1_3_set_defaults_button.grid(
            column=0, row=3, padx=5, pady=5, sticky='SE'
        )
        _1_3_load_defaults_button.grid(
            column=1, row=3, padx=5, pady=5, sticky='SW'
        )

        # RNG tab

        self.W5_rng_prediction_max_jumps = tk.StringVar(value='6')
        self.W5_rng_prediction_list_var = tk.StringVar(value='')

        W5_rng_prediction_label_1 = ttk.Label(
            W5_rng_frame, text='Probability of success, given up to'
        )
        W5_rng_prediction_extra_jump_counter = ttk.Spinbox(
            W5_rng_frame, from_=0, to=20,
            textvariable=self.W5_rng_prediction_max_jumps,
            command=self.update_rng, width=5, state='readonly'
        )
        W5_rng_prediction_label_2 = ttk.Label(
            W5_rng_frame, text='extra jumps:'
        )
        W5_rng_prediction_list = tk.Listbox(
            W5_rng_frame, listvariable=self.W5_rng_prediction_list_var
        )
        W5_rng_prediction_label_1.grid(column=0, row=0)
        W5_rng_prediction_extra_jump_counter.grid(column=1, row=0)
        W5_rng_prediction_label_2.grid(column=2, row=0)
        W5_rng_prediction_list.grid(
            column=0, columnspan=3, row=1, padx=5, sticky='NSEW'
        )

        # Setup finish

        notebook.add(_1_1_frame, padding=10, text='1-1')
        notebook.add(_1_2_frame, padding=10, text='1-2')
        notebook.add(_1_3_frame, padding=10, text='1-3 Secret')
        notebook.add(W5_rng_frame, padding=10, text='World 5 RNG')
        notebook.grid(column=0, row=0, padx=10, pady=10, sticky='NSEW')

    def export_defaults(self) -> None:
        defaults_string = '[1-1]\n'
        defaults_string += f'{self._1_1.jumps}\n'
        defaults_string += f'{self._1_1.bricks_broken}\n'
        defaults_string += f'{self._1_1.checkpoint_igt}\n'
        defaults_string += f'{self._1_1.flagpole_igt}\n'
        defaults_string += f'{int(self._1_1.did_grab_prop)}\n\n'

        defaults_string += '[1-2]\n'
        defaults_string += f'{self._1_2.jumps}\n'
        defaults_string += f'{self._1_2.bricks_broken}\n'
        defaults_string += f'{int(self._1_2.did_hit_ice_flower_block)}\n\n'

        defaults_string += '[1-3 Secret]\n'
        defaults_string += f'{self._1_3.first_bro_prior_jumps}\n'
        defaults_string += f'{self._1_3.first_bro_between_jumps}\n'
        defaults_string += f'{self._1_3.second_bro_prior_jumps}\n'
        defaults_string += f'{self._1_3.second_bro_between_jumps}\n'
        defaults_string += f'{self._1_3.jumps_after_both_bros}\n'
        defaults_string += f'{self._1_3.bricks_broken_after_both_bros}'

        with open(f'{SCRIPT_DIR}/defaults.txt', 'w+') as file:
            file.write(defaults_string)

        return

    def import_defaults(self) -> None:
        try:
            raw_data = open(f'{SCRIPT_DIR}/defaults.txt', 'r').read()
            raw_data = raw_data.split('\n')

            _1_1_defaults = raw_data[1:raw_data.index('[1-2]')]
            _1_2_defaults = raw_data[
                raw_data.index('[1-2]') + 1 : raw_data.index('[1-3 Secret]')
            ]
            _1_3_defaults = raw_data[raw_data.index('[1-3 Secret]') + 1:]

            # 1-1

            _1_1_jumps = int(_1_1_defaults[0])
            _1_1_bricks_broken = int(_1_1_defaults[1])
            _1_1_checkpoint_igt = float(_1_1_defaults[2])
            _1_1_flagpole_igt = float(_1_1_defaults[3])
            _1_1_did_grab_prop = bool(int(_1_1_defaults[4]))
            self._1_1 = self._1_1_Data(
                _1_1_jumps, _1_1_bricks_broken, _1_1_checkpoint_igt,
                _1_1_flagpole_igt, _1_1_did_grab_prop
            )

            # 1-2

            _1_2_jumps = int(_1_2_defaults[0])
            _1_2_bricks_broken = int(_1_2_defaults[1])
            _1_2_did_hit_ice_flower_block = bool(int(_1_2_defaults[2]))
            self._1_2 = self._1_2_Data(
                _1_2_jumps, _1_2_bricks_broken, _1_2_did_hit_ice_flower_block
            )

            # 1-3 Secret

            _1_3_first_bro_prior_jumps = int(_1_3_defaults[0])
            _1_3_first_bro_between_jumps = int(_1_3_defaults[1])
            _1_3_second_bro_prior_jumps = int(_1_3_defaults[2])
            _1_3_second_bro_between_jumps = int(_1_3_defaults[3])
            _1_3_jumps_after_both_bros = int(_1_3_defaults[4])
            _1_3_bricks_broken_after_both_bros = int(_1_3_defaults[5])
            self._1_3 = self._1_3_Data(
                _1_3_first_bro_prior_jumps, _1_3_first_bro_between_jumps,
                _1_3_second_bro_prior_jumps, _1_3_second_bro_between_jumps,
                _1_3_jumps_after_both_bros, _1_3_bricks_broken_after_both_bros
            )

        except Exception as e:
            #raise e
            self._1_1 = self._1_1_Data()
            self._1_2 = self._1_2_Data()
            self._1_3 = self._1_3_Data()
            self.export_defaults()

        self.load_1_1_defaults()
        self.load_1_2_defaults()
        self.load_1_3_defaults()

        return

    def set_1_1_defaults(self) -> None:
        _1_1_checkpoint_igt_whole = int(self._1_1_checkpoint_igt_var.get())
        _1_1_checkpoint_igt_range = self._1_1_checkpoint_igt_range_var.get()
        _1_1_checkpoint_igt = _1_1_checkpoint_igt_whole + \
            IGT_OFFSETS[_1_1_checkpoint_igt_range]
        _1_1_flagpole_igt_whole = int(self._1_1_flagpole_igt_var.get())
        _1_1_flagpole_igt_range = self._1_1_flagpole_igt_range_var.get()
        _1_1_flagpole_igt = _1_1_flagpole_igt_whole + \
            IGT_OFFSETS[_1_1_flagpole_igt_range]

        self._1_1 = self._1_1_Data(
            int(self._1_1_jumps_var.get()), int(self._1_1_bricks_var.get()),
            _1_1_checkpoint_igt, _1_1_flagpole_igt,
            self._1_1_grabbed_prop_var.get()
        )

        return

    def load_1_1_defaults(self) -> None:
        jumps = self._1_1.jumps
        bricks = self._1_1.bricks_broken

        checkpoint_igt_whole = int(self._1_1.checkpoint_igt)
        checkpoint_igt_offset = \
            round(self._1_1.checkpoint_igt - checkpoint_igt_whole, 3)
        checkpoint_igt_range = IGT_RANGES[checkpoint_igt_offset]

        flagpole_igt_whole = int(self._1_1.flagpole_igt)
        flagpole_igt_offset = \
            round(self._1_1.flagpole_igt - flagpole_igt_whole, 3)
        flagpole_igt_range = IGT_RANGES[flagpole_igt_offset]

        grabbed_prop = self._1_1.did_grab_prop

        try:
            self._1_1_jumps_var.set(str(jumps))
            self._1_1_bricks_var.set(str(bricks))
            self._1_1_checkpoint_igt_range_var.set(checkpoint_igt_range)
            self._1_1_checkpoint_igt_var.set(str(checkpoint_igt_whole))
            self._1_1_flagpole_igt_range_var.set(flagpole_igt_range)
            self._1_1_flagpole_igt_var.set(str(flagpole_igt_whole))
            self._1_1_grabbed_prop_var.set(grabbed_prop)

        except:
            self._1_1_jumps_var = tk.StringVar(value=str(jumps))
            self._1_1_bricks_var = tk.StringVar(value=str(bricks))
            self._1_1_checkpoint_igt_range_var = tk.StringVar(
                value=checkpoint_igt_range
            )
            self._1_1_checkpoint_igt_var = tk.StringVar(
                value=str(checkpoint_igt_whole)
            )
            self._1_1_flagpole_igt_range_var = tk.StringVar(
                value=flagpole_igt_range
            )
            self._1_1_flagpole_igt_var = tk.StringVar(
                value=str(flagpole_igt_whole)
            )
            self._1_1_grabbed_prop_var = tk.BooleanVar(value=grabbed_prop)

        return

    def set_1_2_defaults(self) -> None:
        self._1_2 = self._1_2_Data(
            int(self._1_2_jumps_var.get()), int(self._1_2_bricks_var.get()),
            self._1_2_ice_block_var.get()
        )

        return

    def load_1_2_defaults(self) -> None:
        jumps = self._1_2.jumps
        bricks = self._1_2.bricks_broken
        ice_block = self._1_2.did_hit_ice_flower_block

        try:
            self._1_2_jumps_var.set(str(jumps))
            self._1_2_bricks_var.set(str(bricks))
            self._1_2_ice_block_var.set(ice_block)

        except:
            self._1_2_jumps_var = tk.StringVar(value=str(jumps))
            self._1_2_bricks_var = tk.StringVar(value=str(bricks))
            self._1_2_ice_block_var = tk.BooleanVar(value=ice_block)

        return

    def set_1_3_defaults(self) -> None:
        self._1_3 = self._1_3_Data(
            int(self._1_3_first_prior_jumps_var.get()),
            int(self._1_3_first_between_jumps_var.get()),
            int(self._1_3_second_prior_jumps_var.get()),
            int(self._1_3_second_between_jumps_var.get()),
            int(self._1_3_remaining_jumps_var.get()),
            int(self._1_3_remaining_bricks_var.get())
        )

        return

    def load_1_3_defaults(self) -> None:
        first_prior_jumps = self._1_3.first_bro_prior_jumps
        first_between_jumps = self._1_3.first_bro_between_jumps
        second_prior_jumps = self._1_3.second_bro_prior_jumps
        second_between_jumps = self._1_3.second_bro_between_jumps
        remaining_jumps = self._1_3.jumps_after_both_bros
        remaining_bricks = self._1_3.bricks_broken_after_both_bros

        try:
            self._1_3_first_prior_jumps_var.set(str(first_prior_jumps))
            self._1_3_first_between_jumps_var.set(str(first_between_jumps))
            self._1_3_second_prior_jumps_var.set(str(second_prior_jumps))
            self._1_3_second_between_jumps_var.set(str(second_between_jumps))
            self._1_3_remaining_jumps_var.set(str(remaining_jumps))
            self._1_3_remaining_bricks_var.set(str(remaining_bricks))

        except:
            self._1_3_first_prior_jumps_var = tk.StringVar(
                value=str(first_prior_jumps)
            )
            self._1_3_first_between_jumps_var = tk.StringVar(
                value=str(first_between_jumps)
            )
            self._1_3_second_prior_jumps_var = tk.StringVar(
                value=str(second_prior_jumps)
            )
            self._1_3_second_between_jumps_var = tk.StringVar(
                value=str(second_between_jumps)
            )
            self._1_3_remaining_jumps_var = tk.StringVar(
                value=str(remaining_jumps)
            )
            self._1_3_remaining_bricks_var = tk.StringVar(
                value=str(remaining_bricks)
            )

        return

    def on_tab_change(self, event:tk.Event) -> None:
        self.root.focus_set()
        self.update_rng()

    def update_rng(self) -> None:
        # 1-1

        _1_1_jumps = int(self._1_1_jumps_var.get())
        _1_1_bricks = int(self._1_1_bricks_var.get())
        _1_1_grab_prop = self._1_1_grabbed_prop_var.get()

        _1_1_checkpoint_igt_whole = int(self._1_1_checkpoint_igt_var.get())
        _1_1_checkpoint_igt_range = self._1_1_checkpoint_igt_range_var.get()
        _1_1_checkpoint_igt = _1_1_checkpoint_igt_whole + \
            IGT_OFFSETS[_1_1_checkpoint_igt_range]
        _1_1_flagpole_igt_whole = int(self._1_1_flagpole_igt_var.get())
        _1_1_flagpole_igt_range = self._1_1_flagpole_igt_range_var.get()
        _1_1_flagpole_igt = _1_1_flagpole_igt_whole + \
            IGT_OFFSETS[_1_1_flagpole_igt_range]

        self._1_1 = self._1_1_Data(
            _1_1_jumps, _1_1_bricks, _1_1_checkpoint_igt, _1_1_flagpole_igt,
            _1_1_grab_prop
        )

        # 1-2

        _1_2_jumps = int(self._1_2_jumps_var.get())
        _1_2_bricks = int(self._1_2_bricks_var.get())
        _1_2_ice_block = self._1_2_ice_block_var.get()

        self._1_2 = self._1_2_Data(_1_2_jumps, _1_2_bricks, _1_2_ice_block)

        # 1-3 Secret

        _1_3_first_prior_jumps = int(self._1_3_first_prior_jumps_var.get())
        _1_3_first_between_jumps = \
            int(self._1_3_first_between_jumps_var.get())
        _1_3_second_prior_jumps = int(self._1_3_second_prior_jumps_var.get())
        _1_3_second_between_jumps = \
            int(self._1_3_second_between_jumps_var.get())
        _1_3_remaining_jumps = int(self._1_3_remaining_jumps_var.get())
        _1_3_remaining_bricks = int(self._1_3_remaining_bricks_var.get())

        THROW_CYCLE_TIMERS = {'1': 30, '3': 45}

        first_bro_pattern = self._1_3_first_pattern_var.get().split('-')
        first_bro_throw_timer = THROW_CYCLE_TIMERS[first_bro_pattern[0]]
        try: first_bro_jump_timer = int(first_bro_pattern[2])
        except ValueError: first_bro_jump_timer = 55
        try: first_bro_throws = int(first_bro_pattern[1])
        except ValueError: first_bro_throws = 3

        second_bro_pattern = self._1_3_second_pattern_var.get().split('-')
        second_bro_throw_timer = THROW_CYCLE_TIMERS[second_bro_pattern[0]]
        try: second_bro_jump_timer = int(second_bro_pattern[2])
        except ValueError: second_bro_jump_timer = 55
        try: second_bro_throws = int(second_bro_pattern[1])
        except ValueError: second_bro_throws = 3

        does_first_bro_jump_throw = self._1_3_first_bro_jump_throw_var.get()
        does_first_bro_die = self._1_3_first_bro_kill_var.get()
        does_second_bro_jump_throw = self._1_3_second_bro_jump_throw_var.get()
        does_second_bro_die = self._1_3_second_bro_kill_var.get()

        self._1_3 = self._1_3_Data(
            _1_3_first_prior_jumps, _1_3_first_between_jumps,
            _1_3_second_prior_jumps, _1_3_second_between_jumps,
            _1_3_remaining_jumps, _1_3_remaining_bricks
        )

        # Final predictions

        self.rng._1_1(
            self._1_1.jumps, self._1_1.bricks_broken,
            self._1_1.checkpoint_igt, self._1_1.flagpole_igt, 0.167,
            self._1_1.did_grab_prop
        )
        self.rng._1_2(
            self._1_2.jumps, self._1_2.bricks_broken,
            self._1_2.did_hit_ice_flower_block
        )
        self.rng._1_3_S(
            self._1_3.first_bro_prior_jumps,
            self._1_3.first_bro_between_jumps,
            first_bro_throw_timer, first_bro_jump_timer, first_bro_throws,
            does_first_bro_jump_throw, does_first_bro_die,
            self._1_3.second_bro_prior_jumps,
            self._1_3.second_bro_between_jumps,
            second_bro_throw_timer, second_bro_jump_timer, second_bro_throws,
            does_second_bro_jump_throw, does_second_bro_die,
            self._1_3.jumps_after_both_bros,
            self._1_3.bricks_broken_after_both_bros
        )

        probabilities = self.rng.calculate_piranha_probabilities(
            int(self.W5_rng_prediction_max_jumps.get())
        )

        prediction_list = []
        for p in range(len(probabilities)):
            probability = probabilities[p]

            if p == 1:
                prediction_list.append(
                    f'{p} jump: {round(probability * 100, 2)}%'
                )
            else:
                prediction_list.append(
                    f'{p} jumps: {round(probability * 100, 2)}%'
                )

        self.W5_rng_prediction_list_var.set(tuple(prediction_list))

        return

    def mainloop(self) -> None:
        self.root.mainloop()
        self.export_defaults()
