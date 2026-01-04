
# interface.py

from __future__ import annotations

from any_percent import AnyPercentRNG

from copy import copy
from tkinter import ttk
import tkinter as tk
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IGT_OFFSETS = {'Low': 0.167, 'Mid': 0.500, 'High': 0.833}
IGT_RANGES = {0.167: 'Low', 0.500: 'Mid', 0.833: 'High'}
HAMMER_BRO_PATTERNS = { # 'Display name': 'Pattern name'
    '1-3-X': '1-3-X',
    '3-3-X': '3-3-X',
    '3-X-45': '3-X-45',
    '3-1-50': '3-1-50',
    '3-1-55': '3-1-55'
}

class AnyPercentUI:
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

        def create_frame(self, interface:AnyPercentUI) -> None:
            # Remove all widgets from the interface's 1-1 frame

            for widget in interface._1_1_frame.winfo_children():
                widget.destroy()

            # Tk Frame setup

            igt_frame = ttk.Frame(interface._1_1_frame)
            igt_frame.grid(column=0, columnspan=2, row=2, sticky='NSEW')
            for d in range(3):
                igt_frame.grid_columnconfigure(d, weight=1)

                if d >= 2: continue

                igt_frame.grid_rowconfigure(d, weight=1)

            # 1-1 tab begin

            jumps_label = ttk.Label(interface._1_1_frame, text='Jumps*')
            jumps_asterisk = ttk.Label(
                interface._1_1_frame, font=(None, 8),
                text='*excluding holding-shell, spin, and crouch jumps.'
            )
            jumps_counter = ttk.Spinbox(
                interface._1_1_frame, from_=0, to=50,
                textvariable=interface._1_1_jumps_var, width=5,
                state='readonly'
            )
            jumps_label.grid(column=0, row=0)
            jumps_asterisk.grid(column=0, columnspan=2, row=5, pady=5)
            jumps_counter.grid(column=1, row=0)

            bricks_label = ttk.Label(
                interface._1_1_frame, text='Brick blocks broken'
            )
            bricks_counter = ttk.Spinbox(
                interface._1_1_frame, from_=0, to=4,
                textvariable=interface._1_1_bricks_var, width=5,
                state='readonly'
            )
            bricks_label.grid(column=0, row=1)
            bricks_counter.grid(column=1, row=1)

            # 1-1 IGT frame

            checkpoint_igt_label = ttk.Label(
                igt_frame, text='Checkpoint IGT'
            )
            checkpoint_igt_range = ttk.Combobox(
                igt_frame,
                textvariable=interface._1_1_checkpoint_igt_range_var,
                values=list(IGT_OFFSETS), width=5, state='readonly'
            )
            checkpoint_igt_counter = ttk.Spinbox(
                igt_frame, from_=455, to=486,
                textvariable=interface._1_1_checkpoint_igt_var, width=7,
                state='readonly'
            )
            checkpoint_igt_label.grid(column=0, row=0, sticky='E')
            checkpoint_igt_range.grid(column=1, row=0, sticky='E')
            checkpoint_igt_counter.grid(column=2, row=0, sticky='W')

            flagpole_igt_label = ttk.Label(
                igt_frame, text='Flagpole IGT'
            )
            flagpole_igt_range = ttk.Combobox(
                igt_frame,
                textvariable=interface._1_1_flagpole_igt_range_var,
                values=list(IGT_OFFSETS), width=5, state='readonly'
            )
            flagpole_igt_counter = ttk.Spinbox(
                igt_frame, from_=430, to=460,
                textvariable=interface._1_1_flagpole_igt_var, width=7,
                state='readonly'
            )
            flagpole_igt_label.grid(column=0, row=1, sticky='E')
            flagpole_igt_range.grid(column=1, row=1, sticky='E')
            flagpole_igt_counter.grid(column=2, row=1, sticky='W')

            # 1-1 tab finish

            grab_prop_label = ttk.Label(
                interface._1_1_frame, text='Grabbed prop?'
            )
            grab_prop_check = ttk.Checkbutton(
                interface._1_1_frame, variable=interface._1_1_grabbed_prop_var
            )
            grab_prop_label.grid(column=0, row=3)
            grab_prop_check.grid(column=1, row=3)

            set_defaults_button = ttk.Button(
                interface._1_1_frame, text='Set Defaults',
                command=interface.set_1_1_defaults
            )
            load_defaults_button = ttk.Button(
                interface._1_1_frame, text='Load Defaults',
                command=interface.load_1_1_defaults
            )
            set_defaults_button.grid(
                column=0, row=4, padx=5, sticky='SE'
            )
            load_defaults_button.grid(
                column=1, row=4, padx=5, sticky='SW'
            )

            return

    class _1_2_Data:
        def __init__(self, jumps:int = 17, bricks_broken:int = 4,
                     did_hit_ice_flower_block:bool = True):
            self.jumps = jumps
            self.bricks_broken = bricks_broken
            self.did_hit_ice_flower_block = did_hit_ice_flower_block

        def create_frame(self, interface:AnyPercentUI) -> None:
            # Remove all widgets from the interface's 1-2 frame

            for widget in interface._1_2_frame.winfo_children():
                widget.destroy()

            # 1-2 tab

            jumps_label = ttk.Label(interface._1_2_frame, text='Jumps*')
            jumps_asterisk = ttk.Label(
                interface._1_2_frame, font=(None, 8),
                text='*excluding star and crouch jumps.'
            )
            jumps_counter = ttk.Spinbox(
                interface._1_2_frame, from_=0, to=50,
                textvariable=interface._1_2_jumps_var, width=5,
                state='readonly'
            )
            jumps_label.grid(column=0, row=0)
            jumps_asterisk.grid(column=0, columnspan=2, row=4, pady=5)
            jumps_counter.grid(column=1, row=0)

            bricks_label = ttk.Label(
                interface._1_2_frame, text='Brick blocks broken'
            )
            bricks_counter = ttk.Spinbox(
                interface._1_2_frame, from_=0, to=7,
                textvariable=interface._1_2_bricks_var, width=5,
                state='readonly'
            )
            bricks_label.grid(column=0, row=1)
            bricks_counter.grid(column=1, row=1)

            ice_block_label = ttk.Label(
                interface._1_2_frame, text='Hit the first [?] block?'
            )
            ice_block_check = ttk.Checkbutton(
                interface._1_2_frame, variable=interface._1_2_ice_block_var
            )
            ice_block_label.grid(column=0, row=2)
            ice_block_check.grid(column=1, row=2)

            set_defaults_button = ttk.Button(
                interface._1_2_frame, text='Set Defaults',
                command=interface.set_1_2_defaults
            )
            load_defaults_button = ttk.Button(
                interface._1_2_frame, text='Load Defaults',
                command=interface.load_1_2_defaults
            )
            set_defaults_button.grid(
                column=0, row=3, padx=5, sticky='SE'
            )
            load_defaults_button.grid(
                column=1, row=3, padx=5, sticky='SW'
            )

            return

    class _1_3_Data:
        def __init__(self, first_bro_prior_jumps:int = 2,
                     first_bro_between_jumps:list[int] = [0, 0, 2, 2, 2],
                     second_bro_prior_jumps:int = 13,
                     second_bro_between_jumps:list[int] = [0, 0, 2, 2, 2],
                     total_jumps:int = 23,
                     bricks_broken_after_both_bros:int = 0):
            self.first_bro_prior_jumps = first_bro_prior_jumps
            self.first_bro_between_jumps = \
                [0, 0] + first_bro_between_jumps[2:]
            self.second_bro_prior_jumps = second_bro_prior_jumps
            self.second_bro_between_jumps = \
                [0, 0] + second_bro_between_jumps[2:]
            self.total_jumps = total_jumps
            self.bricks_broken_after_both_bros = bricks_broken_after_both_bros

        def create_frame(self, interface:AnyPercentUI) -> None:
            # Remove all widgets from the interface's 1-1 frame

            for widget in interface._1_3_frame.winfo_children():
                widget.destroy()

            # Variable setup

            interface._1_3_first_between_jumps_list[
                interface._1_3_first_pattern_index
            ] = int(interface._1_3_first_between_jumps_var.get())
            interface._1_3_second_between_jumps_list[
                interface._1_3_second_pattern_index
            ] = int(interface._1_3_second_between_jumps_var.get())

            first_pattern_name = interface._1_3_first_pattern_var.get()
            second_pattern_name = interface._1_3_second_pattern_var.get()
            first_pattern = HAMMER_BRO_PATTERNS[first_pattern_name]
            second_pattern = HAMMER_BRO_PATTERNS[second_pattern_name]
            interface._1_3_first_pattern_index = \
                list(HAMMER_BRO_PATTERNS).index(first_pattern_name)
            interface._1_3_second_pattern_index = \
                list(HAMMER_BRO_PATTERNS).index(second_pattern_name)

            first_between_jumps = interface._1_3_first_between_jumps_list[
                interface._1_3_first_pattern_index
            ]
            interface._1_3_first_between_jumps_var.set(
                str(first_between_jumps)
            )
            second_between_jumps = interface._1_3_second_between_jumps_list[
                interface._1_3_second_pattern_index
            ]
            interface._1_3_second_between_jumps_var.set(
                str(second_between_jumps)
            )

            # Tk Frame setup

            first_bro_frame = ttk.Frame(interface._1_3_frame)
            second_bro_frame = ttk.Frame(interface._1_3_frame)
            first_pattern_frame = ttk.Frame(first_bro_frame)
            second_pattern_frame = ttk.Frame(second_bro_frame)
            first_bro_frame.grid(column=0, row=0, sticky='NSEW')
            second_bro_frame.grid(column=1, row=0, sticky='NSEW')

            for d in range(2):
                first_bro_frame.grid_columnconfigure(d, weight=1)
                first_bro_frame.grid_rowconfigure(d, weight=1)
                second_bro_frame.grid_columnconfigure(d, weight=1)
                second_bro_frame.grid_rowconfigure(d, weight=1)

                first_pattern_frame.grid_rowconfigure(d, weight=1)
                second_pattern_frame.grid_rowconfigure(d, weight=1)

                if d >= 1: continue

                first_pattern_frame.grid_columnconfigure(d, weight=1)
                second_pattern_frame.grid_columnconfigure(d, weight=1)

            if first_pattern in ('3-1-50', '3-1-55'): # Late jump patterns
                first_bro_frame.grid_columnconfigure(2, weight=1)
                first_bro_frame.grid_rowconfigure(2, weight=1)

                first_pattern_frame.grid_columnconfigure(1, weight=1)
                first_pattern_frame.grid(
                    column=0, columnspan=2, row=2, sticky='NSEW'
                )
            elif first_pattern == '3-X-45': # Early jump pattern
                first_pattern_frame.grid_columnconfigure(1, weight=1)
                first_pattern_frame.grid_columnconfigure(2, weight=1)
                first_pattern_frame.grid(
                    column=0, columnspan=2, row=2, sticky='NSEW'
                )
            else:
                first_pattern_frame.grid(
                    column=0, columnspan=2, row=1, sticky='NSEW'
                )

            if second_pattern in ('3-1-50', '3-1-55'): # Late jump patterns
                second_bro_frame.grid_columnconfigure(2, weight=1)
                second_bro_frame.grid_rowconfigure(2, weight=1)

                second_pattern_frame.grid_columnconfigure(1, weight=1)
                second_pattern_frame.grid(
                    column=0, columnspan=2, row=2, sticky='NSEW'
                )
            elif second_pattern == '3-X-45': # Early jump pattern
                second_pattern_frame.grid_columnconfigure(1, weight=1)
                second_pattern_frame.grid_columnconfigure(2, weight=1)
                second_pattern_frame.grid(
                    column=0, columnspan=2, row=2, sticky='NSEW'
                )
            else:
                second_pattern_frame.grid(
                    column=0, columnspan=2, row=1, sticky='NSEW'
                )

            # Hammer Bro #1 frame

            first_prior_jumps_label = ttk.Label(
                first_bro_frame,
                text='Total jumps\nbefore spawning\nHammer Bro #1'
            )
            first_prior_jumps_counter = ttk.Spinbox(
                first_bro_frame, from_=0, to=5,
                textvariable=interface._1_3_first_prior_jumps_var, width=5,
                state='readonly'
            )
            first_prior_jumps_label.grid(column=0, row=0)
            first_prior_jumps_counter.grid(column=1, row=0)

            if first_pattern not in ('1-3-X', '3-3-X'): # No-jump patterns
                first_between_jumps_label = ttk.Label(
                    first_bro_frame,
                    text='Jumps before\nHammer Bro #1\njumped'
                )
                first_between_jumps_counter = ttk.Spinbox(
                    first_bro_frame, from_=0, to=5,
                    textvariable=interface._1_3_first_between_jumps_var,
                    width=5, state='readonly'
                )
                first_between_jumps_label.grid(column=0, row=1)
                first_between_jumps_counter.grid(column=1, row=1)

            # Hammer Bro #1 attack pattern frame

            first_pattern_label = ttk.Label(
                first_pattern_frame,
                text='Hammer Bro #1\nattack pattern'
            )
            first_pattern_dropdown = ttk.Combobox(
                first_pattern_frame,
                textvariable=interface._1_3_first_pattern_var,
                values=list(HAMMER_BRO_PATTERNS), width=11, state='readonly'
            )
            first_pattern_label.grid(column=0, row=0)
            first_pattern_dropdown.grid(column=0, row=1)

            if first_pattern == '3-X-45': # Early jump pattern
                first_bro_jump_throw_label = ttk.Label(
                    first_pattern_frame, text='Jump-threw?'
                )
                first_bro_jump_throw_check = ttk.Checkbutton(
                    first_pattern_frame,
                    variable=interface._1_3_first_bro_jump_throw_var
                )
                first_bro_kill_label = ttk.Label(
                    first_pattern_frame, text='Killed?'
                )
                first_bro_kill_check = ttk.Checkbutton(
                    first_pattern_frame,
                    variable=interface._1_3_first_bro_kill_var
                )
                first_bro_jump_throw_label.grid(column=1, row=0)
                first_bro_jump_throw_check.grid(column=1, row=1)
                first_bro_kill_label.grid(column=2, row=0)
                first_bro_kill_check.grid(column=2, row=1)

            elif first_pattern in ('3-1-50', '3-1-55'): # Late jump patterns
                first_bro_jump_throw_label = ttk.Label(
                    first_pattern_frame, text='Jump-threw?'
                )
                first_bro_jump_throw_check = ttk.Checkbutton(
                    first_pattern_frame,
                    variable=interface._1_3_first_bro_jump_throw_var
                )
                first_bro_jump_throw_label.grid(column=1, row=0)
                first_bro_jump_throw_check.grid(column=1, row=1)

            # Hammer Bro #2 frame

            second_prior_jumps_label = ttk.Label(
                second_bro_frame,
                text='Total jumps\nbefore spawning\nHammer Bro #2'
            )
            second_prior_jumps_counter = ttk.Spinbox(
                second_bro_frame, from_=0, to=33,
                textvariable=interface._1_3_second_prior_jumps_var, width=5,
                state='readonly'
            )
            second_prior_jumps_label.grid(column=0, row=0)
            second_prior_jumps_counter.grid(column=1, row=0)

            if second_pattern not in ('1-3-X', '3-3-X'): # No-jump patterns
                second_between_jumps_label = ttk.Label(
                    second_bro_frame,
                    text='Jumps before\nHammer Bro #2\njumped'
                )
                second_between_jumps_counter = ttk.Spinbox(
                    second_bro_frame, from_=0, to=5,
                    textvariable=interface._1_3_second_between_jumps_var,
                    width=5, state='readonly'
                )
                second_between_jumps_label.grid(column=0, row=1)
                second_between_jumps_counter.grid(column=1, row=1)

            # Hammer Bro #2 attack pattern frame

            second_pattern_label = ttk.Label(
                second_pattern_frame,
                text='Hammer Bro #2\nattack pattern'
            )
            second_pattern_dropdown = ttk.Combobox(
                second_pattern_frame,
                textvariable=interface._1_3_second_pattern_var,
                values=list(HAMMER_BRO_PATTERNS), width=11, state='readonly'
            )
            second_pattern_label.grid(column=0, row=0)
            second_pattern_dropdown.grid(column=0, row=1)

            if second_pattern == '3-X-45': # Early jump
                second_bro_jump_throw_label = ttk.Label(
                    second_pattern_frame, text='Jump-threw?'
                )
                second_bro_jump_throw_check = ttk.Checkbutton(
                    second_pattern_frame,
                    variable=interface._1_3_second_bro_jump_throw_var
                )
                second_bro_kill_label = ttk.Label(
                    second_pattern_frame, text='Killed?'
                )
                second_bro_kill_check = ttk.Checkbutton(
                    second_pattern_frame,
                    variable=interface._1_3_second_bro_kill_var
                )
                second_bro_jump_throw_label.grid(column=1, row=0)
                second_bro_jump_throw_check.grid(column=1, row=1)
                second_bro_kill_label.grid(column=2, row=0)
                second_bro_kill_check.grid(column=2, row=1)

            elif second_pattern in ('3-1-50', '3-1-55'): # Late jump patterns
                second_bro_jump_throw_label = ttk.Label(
                    second_pattern_frame, text='Jump-threw?'
                )
                second_bro_jump_throw_check = ttk.Checkbutton(
                    second_pattern_frame,
                    variable=interface._1_3_second_bro_jump_throw_var
                )
                second_bro_jump_throw_label.grid(column=1, row=0)
                second_bro_jump_throw_check.grid(column=1, row=1)

            # 1-3 tab finish

            total_jumps_label = ttk.Label(
                interface._1_3_frame, text='Total jumps before pipe'
            )
            total_jumps_counter = ttk.Spinbox(
                interface._1_3_frame, from_=0, to=50,
                textvariable=interface._1_3_total_jumps_var, width=5,
                state='readonly'
            )
            total_jumps_label.grid(column=0, row=1)
            total_jumps_counter.grid(column=1, row=1)

            remaining_bricks_label = ttk.Label(
                interface._1_3_frame,
                text='Brick blocks broken after checkpoint'
            )
            remaining_bricks_counter = ttk.Spinbox(
                interface._1_3_frame, from_=0, to=15,
                textvariable=interface._1_3_remaining_bricks_var, width=5,
                state='readonly'
            )
            remaining_bricks_label.grid(column=0, row=2)
            remaining_bricks_counter.grid(column=1, row=2)

            set_defaults_button = ttk.Button(
                interface._1_3_frame, text='Set Defaults',
                command=interface.set_1_3_defaults
            )
            load_defaults_button = ttk.Button(
                interface._1_3_frame, text='Load Defaults',
                command=interface.load_1_3_defaults
            )
            set_defaults_button.grid(
                column=0, row=3, padx=5, pady=5, sticky='SE'
            )
            load_defaults_button.grid(
                column=1, row=3, padx=5, pady=5, sticky='SW'
            )

            return

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Any% RNG Tracker')
        self.root.geometry('500x380+0+0')
        self.root.minsize(500, 380)
        self.root.maxsize(640, 480)
        self.root.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.rng = AnyPercentRNG()

        self._1_3_first_pattern_index = 0
        self._1_3_second_pattern_index = 0
        self.import_defaults()

        # Setup begin

        self.root_frame = ttk.Frame(self.root)
        self.root_frame.grid(column=0, row=0, sticky='NSEW')

        self.notebook = ttk.Notebook(self.root_frame)
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
        self._1_1_frame = ttk.LabelFrame(self.notebook, text='1-1')
        self._1_2_frame = ttk.LabelFrame(self.notebook, text='1-2')
        self._1_3_frame = ttk.LabelFrame(self.notebook, text='1-3 Secret')
        self.W5_rng_frame = ttk.LabelFrame(self.notebook, text='World 5 RNG')

        self._1_3_first_pattern_var = tk.StringVar(
            value=list(HAMMER_BRO_PATTERNS)[0]
        )
        self._1_3_first_pattern_var.trace(
            'w', lambda *_: self._1_3.create_frame(self)
        )
        self._1_3_first_bro_kill_var = tk.BooleanVar(value=True)
        self._1_3_first_bro_jump_throw_var = tk.BooleanVar(value=False)
        self._1_3_second_pattern_var = tk.StringVar(
            value=list(HAMMER_BRO_PATTERNS)[0]
        )
        self._1_3_second_pattern_var.trace(
            'w', lambda *_: self._1_3.create_frame(self)
        )
        self._1_3_second_bro_kill_var = tk.BooleanVar(value=False)
        self._1_3_second_bro_jump_throw_var = tk.BooleanVar(value=False)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root_frame.grid_columnconfigure(0, weight=1)
        self.root_frame.grid_rowconfigure(0, weight=1)
        for d in range(4):
            self._1_1_frame.grid_rowconfigure(d, weight=1)

            if d >= 3: continue

            self._1_2_frame.grid_rowconfigure(d, weight=1)
            self._1_3_frame.grid_rowconfigure(d, weight=1)
            self.W5_rng_frame.grid_columnconfigure(d, weight=1)

            if d >= 2: continue

            self.notebook.grid_columnconfigure(d, weight=1)
            self.notebook.grid_rowconfigure(d, weight=1)
            self._1_1_frame.grid_columnconfigure(d, weight=1)
            self._1_2_frame.grid_columnconfigure(d, weight=1)
            self._1_3_frame.grid_columnconfigure(d, weight=1)
            self.W5_rng_frame.grid_rowconfigure(d, weight=1)

        # 1-1 tab
        self._1_1.create_frame(self)

        # 1-2 tab
        self._1_2.create_frame(self)

        # 1-3 tab
        self._1_3.create_frame(self)

        # RNG tab

        self.W5_rng_prediction_max_jumps = tk.StringVar(value='10')
        self.W5_rng_prediction_list_var = tk.StringVar(value='')

        W5_rng_prediction_label_1 = ttk.Label(
            self.W5_rng_frame,
            text='Probability of optimal overworld enemies, given up to'
        )
        W5_rng_prediction_extra_jump_counter = ttk.Spinbox(
            self.W5_rng_frame, from_=0, to=20,
            textvariable=self.W5_rng_prediction_max_jumps,
            command=self.update_rng, width=3, state='readonly'
        )
        W5_rng_prediction_label_2 = ttk.Label(
            self.W5_rng_frame, text='extra jumps:'
        )
        W5_rng_prediction_list = tk.Listbox(
            self.W5_rng_frame, listvariable=self.W5_rng_prediction_list_var
        )
        W5_rng_prediction_label_1.grid(column=0, row=0, sticky='E')
        W5_rng_prediction_extra_jump_counter.grid(column=1, row=0)
        W5_rng_prediction_label_2.grid(column=2, row=0, sticky='W')
        W5_rng_prediction_list.grid(
            column=0, columnspan=3, row=1, padx=5, pady=5, sticky='NSEW'
        )

        # Setup finish

        self.notebook.add(self._1_1_frame, padding=10, text='1-1')
        self.notebook.add(self._1_2_frame, padding=10, text='1-2')
        self.notebook.add(self._1_3_frame, padding=10, text='1-3 Secret')
        self.notebook.add(self.W5_rng_frame, padding=10, text='World 5 RNG')
        self.notebook.grid(column=0, row=0, padx=10, pady=10, sticky='NSEW')

    def export_defaults(self) -> None:
        # 1-1

        defaults_string = '[1-1]\n'
        defaults_string += f'{self._1_1.jumps}\n'
        defaults_string += f'{self._1_1.bricks_broken}\n'
        defaults_string += f'{self._1_1.checkpoint_igt}\n'
        defaults_string += f'{self._1_1.flagpole_igt}\n'
        defaults_string += f'{int(self._1_1.did_grab_prop)}\n\n'

        # 1-2

        defaults_string += '[1-2]\n'
        defaults_string += f'{self._1_2.jumps}\n'
        defaults_string += f'{self._1_2.bricks_broken}\n'
        defaults_string += f'{int(self._1_2.did_hit_ice_flower_block)}\n\n'

        # 1-3

        first_bro_between_jumps = \
            '/'.join([str(n) for n in self._1_3.first_bro_between_jumps])
        second_bro_between_jumps = \
            '/'.join([str(n) for n in self._1_3.second_bro_between_jumps])

        defaults_string += '[1-3 Secret]\n'
        defaults_string += f'{self._1_3.first_bro_prior_jumps}\n'
        defaults_string += f'{first_bro_between_jumps}\n'
        defaults_string += f'{self._1_3.second_bro_prior_jumps}\n'
        defaults_string += f'{second_bro_between_jumps}\n'
        defaults_string += f'{self._1_3.total_jumps}\n'
        defaults_string += f'{self._1_3.bricks_broken_after_both_bros}'

        # Filewrite

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
            _1_3_first_bro_between_jumps = [
                int(n) for n in _1_3_defaults[1].split('/')
            ]
            _1_3_second_bro_prior_jumps = int(_1_3_defaults[2])
            _1_3_second_bro_between_jumps = [
                int(n) for n in _1_3_defaults[3].split('/')
            ]
            _1_3_total_jumps = int(_1_3_defaults[4])
            _1_3_bricks_broken_after_both_bros = int(_1_3_defaults[5])
            self._1_3 = self._1_3_Data(
                _1_3_first_bro_prior_jumps, _1_3_first_bro_between_jumps,
                _1_3_second_bro_prior_jumps, _1_3_second_bro_between_jumps,
                _1_3_total_jumps, _1_3_bricks_broken_after_both_bros
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
        self._1_3_first_between_jumps_list[self._1_3_first_pattern_index] \
            = int(self._1_3_first_between_jumps_var.get())
        self._1_3_second_between_jumps_list[self._1_3_second_pattern_index] \
            = int(self._1_3_second_between_jumps_var.get())

        self._1_3 = self._1_3_Data(
            int(self._1_3_first_prior_jumps_var.get()),
            copy(self._1_3_first_between_jumps_list),
            int(self._1_3_second_prior_jumps_var.get()),
            copy(self._1_3_second_between_jumps_list),
            int(self._1_3_total_jumps_var.get()),
            int(self._1_3_remaining_bricks_var.get())
        )

        return

    def load_1_3_defaults(self) -> None:
        first_prior_jumps = self._1_3.first_bro_prior_jumps
        first_between_jumps = self._1_3.first_bro_between_jumps
        second_prior_jumps = self._1_3.second_bro_prior_jumps
        second_between_jumps = self._1_3.second_bro_between_jumps
        total_jumps = self._1_3.total_jumps
        remaining_bricks = self._1_3.bricks_broken_after_both_bros

        self._1_3_first_between_jumps_list = first_between_jumps
        self._1_3_second_between_jumps_list = second_between_jumps

        try:
            self._1_3_first_prior_jumps_var.set(str(first_prior_jumps))
            self._1_3_first_between_jumps_var.set(
                str(first_between_jumps[self._1_3_first_pattern_index])
            )
            self._1_3_second_prior_jumps_var.set(str(second_prior_jumps))
            self._1_3_second_between_jumps_var.set(
                str(second_between_jumps[self._1_3_second_pattern_index])
            )
            self._1_3_total_jumps_var.set(str(total_jumps))
            self._1_3_remaining_bricks_var.set(str(remaining_bricks))

        except:
            self._1_3_first_prior_jumps_var = tk.StringVar(
                value=str(first_prior_jumps)
            )
            self._1_3_first_between_jumps_var = tk.StringVar(
                value=str(
                    first_between_jumps[self._1_3_first_pattern_index]
                )
            )
            self._1_3_second_prior_jumps_var = tk.StringVar(
                value=str(second_prior_jumps)
            )
            self._1_3_second_between_jumps_var = tk.StringVar(
                value=str(
                    second_between_jumps[self._1_3_second_pattern_index]
                )
            )
            self._1_3_total_jumps_var = tk.StringVar(
                value=str(total_jumps)
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

        working_1_1 = self._1_1_Data(
            _1_1_jumps, _1_1_bricks, _1_1_checkpoint_igt, _1_1_flagpole_igt,
            _1_1_grab_prop
        )

        # 1-2

        _1_2_jumps = int(self._1_2_jumps_var.get())
        _1_2_bricks = int(self._1_2_bricks_var.get())
        _1_2_ice_block = self._1_2_ice_block_var.get()

        working_1_2 = self._1_2_Data(_1_2_jumps, _1_2_bricks, _1_2_ice_block)

        # 1-3 Secret

        _1_3_first_prior_jumps = int(self._1_3_first_prior_jumps_var.get())
        _1_3_first_between_jumps = self._1_3_first_between_jumps_list
        _1_3_second_prior_jumps = int(self._1_3_second_prior_jumps_var.get())
        _1_3_second_between_jumps = self._1_3_second_between_jumps_list
        _1_3_total_jumps = int(self._1_3_total_jumps_var.get())
        _1_3_remaining_bricks = int(self._1_3_remaining_bricks_var.get())

        THROW_CYCLE_TIMERS = {'1': 30, '3': 45}

        first_bro_pattern_name = \
            HAMMER_BRO_PATTERNS[self._1_3_first_pattern_var.get()]
        first_bro_pattern = first_bro_pattern_name.split('-')
        first_bro_throw_timer = THROW_CYCLE_TIMERS[first_bro_pattern[0]]
        try: first_bro_jump_timer = int(first_bro_pattern[2])
        except ValueError: first_bro_jump_timer = 55
        try: first_bro_throws = int(first_bro_pattern[1])
        except ValueError: first_bro_throws = 3

        second_bro_pattern_name = \
            HAMMER_BRO_PATTERNS[self._1_3_second_pattern_var.get()]
        second_bro_pattern = second_bro_pattern_name.split('-')
        second_bro_throw_timer = THROW_CYCLE_TIMERS[second_bro_pattern[0]]
        try: second_bro_jump_timer = int(second_bro_pattern[2])
        except ValueError: second_bro_jump_timer = 55
        try: second_bro_throws = int(second_bro_pattern[1])
        except ValueError: second_bro_throws = 3

        does_first_bro_jump_throw = self._1_3_first_bro_jump_throw_var.get()
        does_first_bro_die = self._1_3_first_bro_kill_var.get()
        does_second_bro_jump_throw = self._1_3_second_bro_jump_throw_var.get()
        does_second_bro_die = self._1_3_second_bro_kill_var.get()

        working_1_3 = self._1_3_Data(
            _1_3_first_prior_jumps, _1_3_first_between_jumps,
            _1_3_second_prior_jumps, _1_3_second_between_jumps,
            _1_3_total_jumps, _1_3_remaining_bricks
        )

        # Final predictions

        first_bro_between_jumps = working_1_3.first_bro_between_jumps[
            self._1_3_first_pattern_index
        ]
        second_bro_between_jumps = working_1_3.second_bro_between_jumps[
            self._1_3_second_pattern_index
        ]

        self.rng._1_1(
            working_1_1.jumps, working_1_1.bricks_broken,
            working_1_1.checkpoint_igt, working_1_1.flagpole_igt, 0.167,
            working_1_1.did_grab_prop
        )
        self.rng._1_2(
            working_1_2.jumps, working_1_2.bricks_broken,
            working_1_2.did_hit_ice_flower_block
        )
        self.rng._1_3_S(
            working_1_3.first_bro_prior_jumps,
            first_bro_between_jumps, first_bro_throw_timer,
            first_bro_jump_timer, first_bro_throws, does_first_bro_jump_throw,
            does_first_bro_die, working_1_3.second_bro_prior_jumps,
            second_bro_between_jumps, second_bro_throw_timer,
            second_bro_jump_timer, second_bro_throws,
            does_second_bro_jump_throw, does_second_bro_die,
            working_1_3.total_jumps,
            working_1_3.bricks_broken_after_both_bros
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
