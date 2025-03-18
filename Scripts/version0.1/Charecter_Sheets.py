import customtkinter
import customtkinter as ctk
import math
import tkinter
from functools import partial

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class CharacterSheet:

    def __init__(self):
        ''' Charecter Statistics-------------------------------------------------------------------------------------'''
        # name, class, level, background, race, alignment, experience points
        self.top_stats_label = ['Name', 'Class', 'Level', 'Background', 'Race', 'Alignment', 'Experience points', '']
        self.top_stats = ['', '', 0, '', '', '', 0, None]

        # strength, dexterity, constitution, intelligence, wisdom, charisma
        self.ability_scores_name = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        self.ability_scores = [0 for i in range(0, 6, 1)]

        self.ability_scores_bonus = []
        for i in range(0, 6, 1):
            self.ability_scores_bonus += [math.floor((((self.ability_scores[i]) - 10) / 2))]

        # Sub Skills
        self.str_skills = [self.ability_scores_bonus[0]]  # Athletics

        self.dex_skills = []
        self.dex_skills_name = ['Acrobatics', 'Sleight of Hand', 'Stealth']
        for i in range(0, 3, 1):
            self.dex_skills += [self.ability_scores_bonus[1]]

        self.int_skills = []  # Arcana, History, Investigation, Nature, Religion
        self.int_skills_name = ['Arcana', 'History', 'Investigation', 'Nature', 'Religion']
        for i in range(0, 5, 1):
            self.int_skills += [self.ability_scores_bonus[3]]

        self.wis_skills = []
        self.wis_skills_name = ['Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival']
        for i in range(0, 5, 1):
            self.wis_skills += [self.ability_scores_bonus[4]]

        self.chr_skills = []
        self.chr_skills_name = ['Deception', 'Intimidation', 'Performance', 'Persuasion']
        for i in range(0, 4, 1):
            self.chr_skills += [self.ability_scores_bonus[5]]

        # Profeciency Bonus, Inspiration, Passive Wisdom(Perception), Passive Intelligence(Investigation)
        self.passive_scores_name = ["Proficiency", "Inspiration", "Passive Perception", "Passive Investigation"]
        self.passive_scores = [0 for i in range(0, 4, 1)]

        # Combat Defense Stats
        self.comb_def_scores_name = ['Armor Class', 'Initiative', 'Speed',
                                     'Max Hit Points', 'Current Hit points', 'Temporary Hit points',
                                     'Total Hit Dice', 'Current Hit Dice',
                                     'Successes', 'Failures']
        # (0 - 2) AC, Initiative, Speed; (3 - 5) Hp max, Current Hp, Temp Hp; (6-7) #D# Total Hd; (8-9) #D# Current Hd
        self.comb_def_scores = [0, 0, 0,
                                0, 0, 0,
                                0, 0, 0, 0]
        # Charecter Lore
        self.character_lore_name = ['Personality Traits', 'Ideals', 'Bonds', 'Flaws']

        # Options
        self.option_buttons_name = ['Features and Traits', 'Proficiencies & Languages',
                                    'Equipment and Appearance', 'Spells']

        # Top Level


        ''' Main Window-------------------------- '''
        self.root = ctk.CTk()
        self.root.title("Charecter Sheet")

        self.canvas = ctk.CTkCanvas(master=self.root, bg='gray13', highlightthickness=0, height=1000, width=1360)
        self.canvas.grid(row=0, column=0)

        self.scroll_bar = ctk.CTkScrollbar(master=self.root, command=self.canvas.yview)
        self.scroll_bar.grid(row=0, column=1, sticky='ns')

        self.mainframe = ctk.CTkFrame(master=self.canvas, fg_color='gray13')

        self.canvas.create_window((0, 0), window=self.mainframe, anchor='nw')

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.mainframe.bind("<KeyPress>", self.scroll_bar)

        '''Top Stat--------------------------------------------------------------------------------------------------'''
        self.frame1 = ctk.CTkFrame(master=self.mainframe)
        for i in range(0, 4, 1):
            self.frame1.columnconfigure(i, weight=1)
            self.frame1.rowconfigure(i, weight=1)

        # Put in headers
        for i in range(0, 2, 1):
            for b in range(0, 4, 1):
                top_label = ctk.CTkLabel(master=self.frame1,
                                         text=self.top_stats_label[b + (i * 4)], font=('Times New Romans', 18))
                top_label.grid(row=(2 * i), column=b, padx=20)

        # Put in header values
        self.top_stats_values_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        for i in range(0, 8, 1):
            self.top_stats_values_labels += [ctk.CTkLabel(master=self.frame1, text=self.top_stats[i],
                                                          font=('Times New Romans', 18))]
        for i in range(0, 2, 1):
            for b in range(0, 4, 1):
                self.top_stats_values_labels[b + (i * 4)].grid(row=((i * 2) + 1), column=b, padx=20)
        self.frame1.grid(row=0, column=0, padx=20, pady=20, columnspan=3)

        ''' Ability Scores + Passive Scores--------------------------------------------------------------------------'''
        self.frame_ability = ctk.CTkFrame(master=self.mainframe)

        # Passive Scores--------------------------------------------------------
        self.frame_ability_passive = ctk.CTkFrame(master=self.frame_ability)

        self.passive_scores_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        self.passive_scores_name_labels = []
        for i in range(0, 4, 1):
            self.passive_scores_labels += [ctk.CTkLabel(master=self.frame_ability_passive,
                                                        text=self.passive_scores[i],
                                                        font=('Times New Romans', 18))]
            self.passive_scores_labels[i].grid(row=i, column=0, padx=10)

            self.passive_scores_name_labels += [ctk.CTkLabel(master=self.frame_ability_passive,
                                                             text=self.passive_scores_name[i],
                                                             font=('Times New Romans', 15))]
            self.passive_scores_name_labels[i].grid(row=i, column=1, padx=10)
        for i in range(0, 2, 1):
            self.passive_scores_labels[i + 2].configure(text=10 + self.ability_scores[4])

        self.frame_ability_passive.pack(pady=10)
        # Ability Scores (name, score, bonus, Skills)--------------------------------------------------------
        self.frame_ability_act = ctk.CTkFrame(master=self.frame_ability)

        self.frame_ability_act_frame = []  # mini frame for each score
        self.ability_scores_name_label = []  # label for each attribute
        self.ability_scores_label = []  # label for each attribute score                                                  # !!!IMPORTANT LABEL VALUE!!!
        self.ability_scores_bonus_label = []  # !!!IMPORTANT LABEL VALUE!!!
        self.saving_throws_label = []  # !!!IMPORTANT LABEL VALUE!!!
        self.saving_throws_bonus_label = []  # !!!IMPORTANT LABEL VALUE!!!

        # All mini frames
        for i in range(0, 6, 1):
            self.frame_ability_act_frame += [ctk.CTkFrame(master=self.frame_ability_act)]
            self.ability_scores_name_label += [ctk.CTkLabel(master=self.frame_ability_act_frame[i],
                                                            text=self.ability_scores_name[i],
                                                            font=('Times New Romans', 15))]
            self.ability_scores_name_label[i].grid(row=0, column=0, padx=10)

            self.ability_scores_label += [ctk.CTkLabel(master=self.frame_ability_act_frame[i],
                                                       text=self.ability_scores[i],
                                                       font=('Times New Romans', 13))]
            self.ability_scores_label[i].grid(row=1, column=0, padx=10)

            self.ability_scores_bonus_label += [ctk.CTkLabel(master=self.frame_ability_act_frame[i],
                                                             text=self.ability_scores_bonus[0],
                                                             font=('Times New Romans', 20))]
            self.ability_scores_bonus_label[i].grid(row=2, column=0, padx=10, rowspan=5)

            self.saving_throws_label += [ctk.CTkLabel(master=self.frame_ability_act_frame[i],
                                                      text="Saving Throws: ",
                                                      font=('Times New Romans', 12))]
            self.saving_throws_label[i].grid(row=1, column=1, padx=10)

            self.saving_throws_bonus_label += [ctk.CTkLabel(master=self.frame_ability_act_frame[i],
                                                            text="",
                                                            font=('Times New Romans', 12))]
            self.saving_throws_bonus_label[i].grid(row=1, column=2, padx=10)

            self.frame_ability_act_frame[i].pack(pady=10, padx=10)

        # Strength

        self.str_skills_bonus_labels = [
            ctk.CTkLabel(master=self.frame_ability_act_frame[0],  # !!!IMPORTANT LABEL VALUE!!!
                         text="",
                         font=('Times New Romans', 12))]
        self.str_skills_bonus_labels[0].grid(row=2, column=2)
        self.str_skills_name_labels = [ctk.CTkLabel(master=self.frame_ability_act_frame[0],
                                                    text="Athletics: ",
                                                    font=('Times New Romans', 12))]
        self.str_skills_name_labels[0].grid(row=2, column=1, padx=10)

        # Dex
        self.dex_skills_name_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        self.dex_skills_bonus_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        for i in range(0, 3, 1):
            self.dex_skills_name_labels += [ctk.CTkLabel(master=self.frame_ability_act_frame[1],
                                                         text=self.dex_skills_name[i] + ':',
                                                         font=('Times New Romans', 12))]
            self.dex_skills_name_labels[i].grid(row=2 + i, column=1)

            self.dex_skills_bonus_labels += [ctk.CTkLabel(master=self.frame_ability_act_frame[1],
                                                          text="",
                                                          font=('Times New Romans', 12))]
            self.dex_skills_bonus_labels[i].grid(row=2 + i, column=2, padx=10)

        # Constitution

        # Intelligence
        self.int_skills_name_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        self.int_skills_bonus_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        for i in range(0, 5, 1):
            self.int_skills_name_labels += [ctk.CTkLabel(master=self.frame_ability_act_frame[3],
                                                         text=self.int_skills_name[i] + ':',
                                                         font=('Times New Romans', 12))]
            self.int_skills_name_labels[i].grid(row=2 + i, column=1)

            self.int_skills_bonus_labels += [ctk.CTkLabel(master=self.frame_ability_act_frame[3],
                                                          text="",
                                                          font=('Times New Romans', 12))]
            self.int_skills_bonus_labels[i].grid(row=2 + i, column=2, padx=10)

        # Wisdom
        self.wis_skills_name_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        self.wis_skills_bonus_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        for i in range(0, 5, 1):
            self.wis_skills_name_labels += [ctk.CTkLabel(master=self.frame_ability_act_frame[4],
                                                         text=self.wis_skills_name[i] + ':',
                                                         font=('Times New Romans', 12))]
            self.wis_skills_name_labels[i].grid(row=2 + i, column=1)

            self.wis_skills_bonus_labels += [
                ctk.CTkLabel(master=self.frame_ability_act_frame[4],
                             text="",
                             font=('Times New Romans', 12))]
            self.wis_skills_bonus_labels[i].grid(row=2 + i, column=2, padx=10)

        # Charisma
        self.chr_skills_name_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        self.chr_skills_bonus_labels = []  # !!!IMPORTANT LABEL VALUE!!!
        for i in range(0, 4, 1):
            self.chr_skills_name_labels += [ctk.CTkLabel(master=self.frame_ability_act_frame[5],
                                                         text=self.chr_skills_name[i] + ':',
                                                         font=('Times New Romans', 12))]
            self.chr_skills_name_labels[i].grid(row=2 + i, column=1)

            self.chr_skills_bonus_labels += [
                ctk.CTkLabel(master=self.frame_ability_act_frame[5],
                             text="",
                             font=('Times New Romans', 12))]
            self.chr_skills_bonus_labels[i].grid(row=2 + i, column=2, padx=10)

        self.frame_ability_act.pack(pady=10)
        self.frame_ability.grid(row=1, column=0, padx=20, pady=20, rowspan=2)

        ''' Combat Defense Stats-------------------------------------------------------------------------------------'''
        self.frame_defense = ctk.CTkFrame(master=self.mainframe)

        self.frame_defense_frames = []  # 0: AC, 1: Hp, 2: Hd, 3: Death
        for i in range(0, 4, 1):
            self.frame_defense_frames += [ctk.CTkFrame(master=self.frame_defense)]
            self.frame_defense_frames[i].pack(pady=0, padx=10)

        self.comb_def_scores_name_label = []
        self.comb_def_scores_label = []

        for c in range(0, 2, 1):
            for i in range(0, 3, 1):
                self.comb_def_scores_name_label += [
                    ctk.CTkLabel(master=self.frame_defense_frames[c],
                                 text=self.comb_def_scores_name[i + (c * 3)],
                                 font=('Times New Romans', 15),
                                 corner_radius=0)]
                self.comb_def_scores_name_label[i + (3 * c)].grid(row=0, column=i, padx=10)

                self.comb_def_scores_label += [
                    ctk.CTkLabel(master=self.frame_defense_frames[c],
                                 text=self.comb_def_scores[i + (c * 3)],
                                 font=('Times New Romans', 15),
                                 corner_radius=0)]
                self.comb_def_scores_label[i + (3 * c)].grid(row=1, column=i, padx=10)

        for c in range(2, 4, 1):
            self.comb_def_scores_label += [
                ctk.CTkLabel(master=self.frame_defense_frames[2],
                             text=str(self.comb_def_scores[(c - 2) * 2 + 6]) + "D" + str(
                                 self.comb_def_scores[(c - 2) * 2 + 7]),
                             font=('Times New Romans', 15))]
            self.comb_def_scores_label[(c - 2) + 6].grid(row=1, column=(c - 2), padx=10)
            for i in range(0, 2, 1):
                self.comb_def_scores_name_label += [
                    ctk.CTkLabel(master=self.frame_defense_frames[c],
                                 text=self.comb_def_scores_name[i + (2 * c) + 2],
                                 font=('Times New Romans', 15))]
                self.comb_def_scores_name_label[i + (2 * c) + 2].grid(row=0, column=i, padx=10)

        # Death Saves -----------------------------------------------------------------------------------------
        self.death_saves_frame = ctk.CTkFrame(master=self.frame_defense)

        self.death_saves_values = []
        self.death_saves_boxs = []
        for i in range(0, 3, 1):
            self.death_saves_values += [tkinter.StringVar(value='off')]                                                  # !!!IMPORTANT LABEL VALUE!!!
            self.death_saves_boxs += [customtkinter.CTkCheckBox(master=self.death_saves_frame,
                                                                text= '',
                                                                variable=self.death_saves_values[i],
                                                                onvalue="on", offvalue="off",
                                                                width=20,
                                                                fg_color='white',
                                                                hover_color='white')]
            self.death_saves_boxs[i].pack(side='left')
        for i in range(3, 6, 1):
            self.death_saves_values += [tkinter.StringVar(value='off')]
            self.death_saves_boxs += [customtkinter.CTkCheckBox(master=self.death_saves_frame,
                                                                text= '',
                                                                variable=self.death_saves_values[i],
                                                                onvalue="on", offvalue="off",
                                                                width=20,
                                                                fg_color='red',
                                                                hover_color='red')]
            self.death_saves_boxs[i].pack(side='left', pady=10)
        self.death_saves_frame.pack()

        self.frame_defense.grid(row=1, column=1, padx=20, pady=20, sticky='new')
        ''' Combat Attack Stats--------------------------------------------------------------------------------------'''
        self.frame_Attack = ctk.CTkFrame(master=self.mainframe)

        self.frame_Attack.grid(row=2, column=1, padx=20, pady=20)
        ''' Charecter Lore Stats-------------------------------------------------------------------------------------'''
        self.frame_character_lore = ctk.CTkFrame(master=self.mainframe)

        self.character_lore_label = []
        self.character_lore_boxs = []
        for i in range(0, 4, 1):
            self.character_lore_label += [ctk.CTkLabel(master=self.frame_character_lore,
                                                       text=self.character_lore_name[i],
                                                       font=('Times New Romans', 15))]
            self.character_lore_label[i].pack()
            self.character_lore_boxs += [ctk.CTkTextbox(master=self.frame_character_lore,
                                                        font=('Times New Romans', 12),
                                                        width=300, height=150)]
            self.character_lore_boxs[i].pack()

        self.frame_character_lore.grid(row=1, column=2, padx=20, pady=20, sticky='ns')
        ''' Options Menu---------------------------------------------------------------------------------------------'''
        self.frame_options = ctk.CTkFrame(master=self.mainframe)

        self.option_buttons = []
        for i in range(0, 4, 1):
            self.option_buttons += [ctk.CTkButton(master=self.frame_options,
                                                  text=self.option_buttons_name[i],
                                                  font=('Times New Romans', 15),
                                                  height=70,
                                                  width=200,
                                                  fg_color='darkred')]
            self.option_buttons[i].pack(pady=10)

        self.frame_options.grid(row=2, column=2, padx=20, pady=20, sticky='new')

        '''Top Levels-----------------------------------------------------------------------------------------------'''

        self.features = ctk.CTkToplevel
        self.proficiency = ctk.CTkToplevel
        self.inventory = ctk.CTkToplevel
        self.spells = ctk.CTkToplevel
        # self.inventory(self.root)

        self.root.mainloop()

    def pick_race(self, race):
        # Ability Score Increase
        self.Increase = input("Pick any ability score increase")


CharacterSheet()
