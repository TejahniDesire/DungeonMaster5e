

from Home import *



def create_frame(top_label_str:str, bottom_label_str:str):
    frame = QFrame()
    frame.setFrameShape(QFrame.Panel)
    frame.setMaximumHeight(100)

    layout = QVBoxLayout(frame)

    bottom_label = QLabel()
    bottom_label.setText(bottom_label_str)

    layout.addWidget(create_top_label(top_label_str), alignment=QtCore.Qt.AlignCenter)
    layout.addWidget(bottom_label, alignment=QtCore.Qt.AlignCenter)

    return frame, bottom_label


def create_top_label(string:str):
    top_label = QLabel()
    top_label.setText(string)
    top_label.setFont(style.LabelFont2)
    return top_label

class AllStatWidgets:

    def __init__(self, charecter):
        self.charecter = charecter
        self.attribute_labels = {
            'str': StatLayout(
                self.charecter.get_specific_attribute('str'), self.charecter.get_specific_skill_of_attribute('str')),
            'dex': StatLayout(
                self.charecter.get_specific_attribute('dex'), self.charecter.get_specific_skill_of_attribute('dex')),
            'con': StatLayout(
                self.charecter.get_specific_attribute('con'), self.charecter.get_specific_skill_of_attribute('con')),
            'int': StatLayout(
                self.charecter.get_specific_attribute('int'), self.charecter.get_specific_skill_of_attribute('int')),
            'wis': StatLayout(
                self.charecter.get_specific_attribute('wis'), self.charecter.get_specific_skill_of_attribute('wis')),
            'chr': StatLayout(
                self.charecter.get_specific_attribute('chr'), self.charecter.get_specific_skill_of_attribute('chr'))
        }

    def get_specific_layout(self,layout:str):
        return self.attribute_labels[layout]

    def add_widgets_to_layout(self,layout):
        for name in list(self.attribute_labels):
            layout.addWidget(self.attribute_labels[name].getWidget())

    def update(self):
        for name in list(self.attribute_labels):
            self.attribute_labels[name].update()


class StatLayout:

    def __init__(self, attribute: ruleTools.Stat, skills: list[ruleTools.Skill]):
        self.attribute = attribute
        self.skills = skills

        # widget to be returned to app
        self.main_widget = QWidget()

        # Widgets main layout
        outer_layout = QVBoxLayout(self.main_widget)

        # Separators for aestetic
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)

        outer_layout.addWidget(separator1)

        outer_layout.addWidget(separator2)

        # Layout for left and right side of stats
        main_layout = QHBoxLayout()
        outer_layout.addLayout(main_layout)

        # Frame for attribute labels
        frame1 = QFrame()
        frame1.setFrameShape(QFrame.Panel)
        # Frame for skill labels
        frame2 = QFrame()
        frame2.setFrameShape(QFrame.Panel)

        main_layout.addWidget(frame1)
        main_layout.addWidget(frame2)

        attribute_layout = QVBoxLayout(frame1)
        skill_layout = QVBoxLayout(frame2)

        # Attributes Labels___________
        self.att_labels = [
            QLabel(),
            QLabel()
        ]
        self.att_labels[0].setText(str(attribute.get_total_base()))

        bonus = attribute.get_total_bonus()

        sign = ruleTools.sign_string(bonus)

        self.att_labels[1].setText(sign + str(bonus))
        self.att_labels[1].setFont( QFont('Times', 20, QFont.Decorative))

        # Label for "Strength, Wisdom, etc"
        top_label = QLabel(attribute.get_type())
        top_label.setFont(style.LabelFont2)

        attribute_layout.addWidget(top_label, alignment=QtCore.Qt.AlignCenter)
        for i in range(len(self.att_labels)):
            attribute_layout.addWidget(self.att_labels[i], alignment=QtCore.Qt.AlignCenter)

        # Skill Labels___________
        self.skill_labels = []
        i = 0
        for name in list(skills):
            skill_string = skills[name].get_type()
            bonus = skills[name].get_total_bonus()
            sign = ruleTools.sign_string(bonus)

            skill_string += ': ' + sign + str(bonus)
            self.skill_labels += [QCheckBox(skill_string)]
            self.skill_labels[i].setFont(style.LabelFont3)
            self.skill_labels[i].toggled.connect(partial(self.skill_checked, skills[name], self.skill_labels[i]))
            skill_layout.addWidget(self.skill_labels[i], alignment=(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
            i += 1

    def getWidget(self):
        return self.main_widget

    def update(self):
        self.attribute.update()

        self.att_labels[0].setText(str(self.attribute.get_total_base()))

        bonus = self.attribute.get_total_bonus()
        sign = ruleTools.sign_string(bonus)
        self.att_labels[1].setText(sign + str(bonus))

        i = 0
        # Update Skills
        for name in list(self.skills):
            self.skills[name].update()
            skill_string = self.skills[name].get_type()
            bonus = self.skills[name].get_total_bonus()
            sign = ruleTools.sign_string(bonus)
            skill_string += ': ' + sign + str(bonus)

            self.skill_labels[i].setText(skill_string)
            i += 1

    def skill_checked(self, skill, button: QCheckBox):
        if button.isChecked():
            skill.give()
        else:
            skill.unlearn()

        self.update()


class RPWidget:

    def __init__(self, top_stats: list[ruleTools.TopStatValue]):
        self.tp = top_stats

        # Main Widget to be given to app
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)

        # Upper layout has Name, Class and level
        upper_layout = QHBoxLayout()
        # Lower layout has background, race, alignment and exp
        lower_layout = QHBoxLayout()

        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)

        main_layout.addLayout(upper_layout)
        main_layout.addWidget(separator1)
        main_layout.addLayout(lower_layout)
        main_layout.addWidget(separator2)

        # names = ['name',
        #          'class',
        #          'level',
        #          'background',
        #          'race',
        #          'alignment',
        #          'experience']

        self.tp_values = {}

        # Name________________________
        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)

        upper_layout.addWidget(frame)

        inner_label_layout = QVBoxLayout(frame)

        label = QLabel()
        label.setText(self.tp['name'].get_type())
        label.setFont(style.LabelFont1)

        self.tp_values['name'] = QPushButton()
        self.tp_values['name'].setText(self.tp['name'].get_value())
        self.tp_values['name'].clicked.connect(self.name_window)


        # self.tp_values['name'].setAutoFillBackground(True)
        self.tp_values['name'].setStyleSheet(style.TabButtonSheet2)
        # palette = QPalette()
        # palette.setColor(QPalette.WindowText, QColor('red'))
        # self.tp_values['name'].setPalette(palette)


        name_font = QFont('Times', 15, QFont.Bold)
        self.tp_values['name'].setFont(name_font)


        inner_label_layout.addWidget(label)
        inner_label_layout.addWidget(self.tp_values['name'])

        # Class and Level_______________
        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)

        upper_layout.addWidget(frame)

        inner_label_layout0 = QVBoxLayout(frame)
        inner_label_layout1 = QHBoxLayout(frame)

        label = QLabel()
        label.setText(self.tp['class'].get_type() + ' & ' + self.tp['level'].get_type())
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(style.LabelFont1)

        self.tp_values['class'] = QLabel()
        self.tp_values['level'] = QLabel()
        self.tp_values['class'].setText(self.tp['class'].get_value())
        self.tp_values['class'].setAlignment(QtCore.Qt.AlignRight)
        self.tp_values['level'].setText(str(self.tp['level'].get_value()))
        self.tp_values['level'].setAlignment(QtCore.Qt.AlignLeft)

        inner_label_layout0.addWidget(label)
        inner_label_layout0.addLayout(inner_label_layout1)
        inner_label_layout1.addWidget(self.tp_values['class'])
        inner_label_layout1.addWidget(self.tp_values['level'])

        # Background_______________

        self.standard_label('background', lower_layout)

        # Race_______________

        self.standard_label('race', lower_layout)

        # Alignment_______________

        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)

        lower_layout.addWidget(frame)

        inner_label_layout = QVBoxLayout(frame)

        label = QLabel()
        label.setText(self.tp['alignment'].get_type())
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(style.LabelFont1)

        self.tp_values['alignment'] = QPushButton()
        self.tp_values['alignment'].setText(self.tp['alignment'].get_value())
        self.tp_values['alignment'].clicked.connect(self.alignment_window)
        self.tp_values['alignment'].setStyleSheet(style.TabButtonSheet2)

        inner_label_layout.addWidget(label)
        inner_label_layout.addWidget(self.tp_values['alignment'])

        # Experience____________________
        self.standard_label('experience', lower_layout)

    def standard_label(self, label_name, lower_layout):

        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)

        lower_layout.addWidget(frame)

        inner_label_layout = QVBoxLayout(frame)

        label = QLabel()
        label.setText(self.tp[label_name].get_type())
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(style.LabelFont1)

        self.tp_values[label_name] = QLabel()
        self.tp_values[label_name].setAlignment(QtCore.Qt.AlignCenter)
        self.tp_values[label_name].setText(str(self.tp[label_name].get_value()))

        inner_label_layout.addWidget(label)
        inner_label_layout.addWidget(self.tp_values[label_name])

    def get_widget(self):
        return self.main_widget

    def update(self):
        for name in list(self.tp_values):
            self.tp_values[name].setText(str(self.tp[name].get_value()))

    def name_window(self):
        self.name_w = pyqt5_Custom_Windows.NameWindow(self.tp['name'].set, self.update)
        self.name_w.show()

    def alignment_window(self):
        self.alignment_w = pyqt5_Custom_Windows.AlignmentWindow(self.tp['alignment'].set, self.update)
        self.alignment_w.show()


class MiddleWidget:
    def __init__(self, top:list, middle:list):
        self.tp = top
        self.mdl= middle
        self.tp_values = {}
        self.mdl_values = {} # middle values
        # Main Widget to be given to app
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)


        first_layout_outer = QVBoxLayout()
        first_layout_inner = QHBoxLayout()

        first_layout_outer.addWidget(appHelperTools.CreateSeperator())
        first_layout_outer.addLayout(first_layout_inner)
        first_layout_outer.addWidget(appHelperTools.CreateSeperator())

        # AC_Layout_________________
        frame, self.tp_values["ac"] = create_frame(self.tp["ac"].get_type(),
                                                        str(self.tp["ac"].get_total_base()))
        first_layout_inner.addWidget(frame)

        # init_Layout_________________
        frame, self.tp_values["init"]  = create_frame(self.tp["init"].get_type(),
                                                           self.tp["init"].get_total_bonus_string())
        first_layout_inner.addWidget(frame)

        # Speed_Layout_________________
        frame, self.tp_values["speed"] = create_frame(self.tp["speed"].get_type(),
                                                           str(self.tp["speed"].get_total_base()))
        first_layout_inner.addWidget(frame)


        # Second inner layout_________________________________________________________________________________________

        second_layout_inner = QHBoxLayout()

        first_layout_outer.addWidget(appHelperTools.CreateSeperator())
        first_layout_outer.addLayout(second_layout_inner)
        first_layout_outer.addWidget(appHelperTools.CreateSeperator())

        # Hit Points Max_______________
        frame, self.tp_values["mhp"] = create_frame(self.tp["mhp"].get_type(),
                                                         str(self.tp["mhp"].get_total_base()))
        second_layout_inner.addWidget(frame)

        # Hit Points Current_______________

        frame, self.tp_values["chp"] = create_frame(self.tp["chp"].get_type(),
                                                         str(self.tp["chp"].get_total_base()))
        second_layout_inner.addWidget(frame)

        # Thirds inner layout_________________________________________________________________________________________

        third_layout_inner = QHBoxLayout()

        first_layout_outer.addWidget(appHelperTools.CreateSeperator())
        first_layout_outer.addLayout(third_layout_inner)
        first_layout_outer.addWidget(appHelperTools.CreateSeperator())


        # Total Hit dice_______________

        frame, self.mdl_values["thd"] = create_frame(self.mdl["hd"].get_total_hd_label(),
                                                    str(self.mdl["hd"].get_total_hd_string()))
        third_layout_inner.addWidget(frame)

        # Current Hit dice_______________

        frame, self.mdl_values["chd"] = create_frame(self.mdl["hd"].get_current_hd_label(),
                                                    str(self.mdl["hd"].get_current_hd_string()))
        third_layout_inner.addWidget(frame)

        # Death saving throws_______________

        frame1 = QFrame()
        frame1.setFrameShape(QFrame.Panel)
        frame1.setMaximumHeight(50)

        frame2 = QFrame()
        frame2.setFrameShape(QFrame.Panel)
        frame2.setMaximumHeight(100)

        first_layout_outer.addWidget(appHelperTools.CreateSeperator())
        first_layout_outer.addWidget(frame1)
        first_layout_outer.addWidget(frame2)
        first_layout_outer.addWidget(appHelperTools.CreateSeperator())

        second_outer_layout = QVBoxLayout(frame1)
        top_label = create_top_label(self.mdl["death"].get_type())
        second_outer_layout.addWidget(top_label,alignment=QtCore.Qt.AlignCenter)

        fourth_inner_layout = QHBoxLayout(frame2)

        success_layout = QVBoxLayout()

        success_layout.addWidget(create_top_label(self.mdl["death"].get_success_label()),
                                 alignment=QtCore.Qt.AlignCenter)
        success_checkbox_layout = QHBoxLayout()
        success_layout.addLayout(success_checkbox_layout)

        failure_layout = QVBoxLayout()
        failure_layout.addWidget(create_top_label(self.mdl["death"].get_failure_label()),
                                 alignment=QtCore.Qt.AlignCenter)
        failure_checkbox_layout = QHBoxLayout()
        failure_layout.addLayout(failure_checkbox_layout)

        fourth_inner_layout.addLayout(success_layout)
        fourth_inner_layout.addLayout(failure_layout)

        top_label = QLabel()
        top_label.setText(self.mdl["death"].get_success_label())
        top_label.setFont(style.LabelFont2)

        self.fcheckboxes = []
        self.wcheckboxes = []

        for i in range(3):
            self.fcheckboxes += [QCheckBox()]
            self.fcheckboxes[i].clicked.connect(partial(self.death_failure))
            failure_checkbox_layout.addWidget(self.fcheckboxes[i],alignment=QtCore.Qt.AlignCenter)

            self.wcheckboxes += [QCheckBox()]
            self.wcheckboxes[i].clicked.connect(partial(self.death_success))
            self.wcheckboxes[i].setStyleSheet('QPushButton {background-color: red; color: red;}')
            success_checkbox_layout.addWidget(self.wcheckboxes[i],alignment=QtCore.Qt.AlignCenter)


        main_layout.addLayout(first_layout_outer)

    def get_widget(self):
        return self.main_widget

    def update(self):
        for name in list(self.tp_values):
            self.tp[name].update()
            self.tp_values[name].update()

            if name == "init":
                self.tp_values[name].setText(self.tp[name].get_total_bonus_string())
            else:
                self.tp_values[name].setText(str(self.tp[name].get_total_base()))

        self.mdl["hd"].update()
        self.mdl_values["thd"].setText(self.mdl["hd"].get_total_hd_string())
        self.mdl_values["chd"].setText(self.mdl["hd"].get_current_hd_string())

        self.mdl["death"].update()
        total_failures = self.mdl["death"].get_num_failure()
        total_successes = self.mdl["death"].get_num_success()

        f = 0
        w = 0
        for i in range(3):
            f += 1
            w += 1
            self.fcheckboxes[i].checked = False
            self.wcheckboxes[i].checked = False

            if f <= total_failures:
                self.fcheckboxes[i].checked = True

            if w <= total_successes:
                self.wcheckboxes[i].checked = True

            self.wcheckboxes[i].setChecked(self.wcheckboxes[i].checked)
            self.fcheckboxes[i].setChecked(self.fcheckboxes[i].checked)

    def death_failure(self,isChecked):

        if isChecked:
            self.mdl["death"].mark_failure()
        else:
            self.mdl["death"].reduce_failure()
        self.update()

    def death_success(self,isChecked):
        if isChecked:
            self.mdl["death"].mark_success()
        else:
            self.mdl["death"].reduce_success()
        self.update()


class WeaponWidget:

    def __init__(self,tinventory:charManagers.Inventory,attack_inventory:charManagers.AttackInventory,ability_score_counter:dict[ruleTools.Stat]):

        self.main_widget = QFrame()
        self.main_widget.setFrameShape(QFrame.StyledPanel)
        self.ATiventory = attack_inventory
        self.tinventory = tinventory
        self.ABS = ability_score_counter
        self.main_layout = QVBoxLayout(self.main_widget)
        self.mobile_layout = QVBoxLayout()
        self.main_layout.addLayout(self.mobile_layout)
        self.defaultStateCreation()

    def update(self):
        self.ATiventory.update()
        self.refresh()

    def getWidget(self):
        return self.main_widget

    def refresh(self):
        appHelperTools.deleteItemsOfLayout(self.mobile_layout)
        self.mobile_layout = QVBoxLayout()
        self.main_layout.addLayout(self.mobile_layout)
        self.defaultStateCreation()

    def defaultStateCreation(self):

        self.mobile_layout.addWidget(appHelperTools.CreateLabel("Attacks and SpellCasting", style.LabelFont2),
                                   alignment=QtCore.Qt.AlignCenter)

        # Grid Layout
        grid_layout = QGridLayout()
        # grid_layout.SetMaximuHeight
        grid_layout.addWidget(appHelperTools.CreateLabel("Name", style.LabelFont2, style.DarkGreyLabel),
                              0, 1, alignment=QtCore.Qt.AlignCenter)
        grid_layout.addWidget(appHelperTools.CreateLabel("Attack Bonus", style.LabelFont2, style.DarkGreyLabel),
                              0, 3, alignment=QtCore.Qt.AlignCenter)
        grid_layout.addWidget(appHelperTools.CreateLabel("Damage/Type", style.LabelFont2, style.DarkGreyLabel),
                              0, 5, 1, 2, alignment=QtCore.Qt.AlignCenter)

        add_button = appHelperTools.CreateGenButton(stylesheet=style.ItemEditButton,
                                          icon_url=imageURLS.AddUrl, icon_size=QtCore.QSize(20, 20),function=self.addWindow)
        grid_layout.addWidget(add_button, 0, 7, alignment=QtCore.Qt.AlignCenter)

        for i in range(8):
            grid_layout.addWidget(appHelperTools.CreateSeperator(), 1, i)

        """Weapons_________________________________"""

        counter = 2
        for key in self.ATiventory.inventory.keys():
            print(key)
            name, bonus, damage,subtract_button = self.createWeaponRow(self.ATiventory[key])
            grid_layout.addWidget(appHelperTools.CreateVSeperator(), counter, 0)

            grid_layout.addWidget(name, counter, 1, alignment=QtCore.Qt.AlignCenter)
            grid_layout.addWidget(appHelperTools.CreateVSeperator(), counter, 2)

            grid_layout.addWidget(bonus, counter, 3, alignment=QtCore.Qt.AlignCenter)
            grid_layout.addWidget(appHelperTools.CreateVSeperator(), counter, 4)

            grid_layout.addWidget(damage, counter, 5, alignment=QtCore.Qt.AlignCenter)
            grid_layout.addWidget(appHelperTools.CreateVSeperator(), counter, 6)

            grid_layout.addWidget(subtract_button, counter, 7, alignment=QtCore.Qt.AlignCenter)
            grid_layout.addWidget(appHelperTools.CreateVSeperator(), counter, 6)

            for i in range(8):
                grid_layout.addWidget(appHelperTools.CreateSeperator(), counter+1, i)
            counter += 2

        self.mobile_layout.addLayout(grid_layout)

    def createWeaponRow(self,item:objectsDnD.Item):
        name = str(item.get_amount()) + "x " +  item.get_name()
        name_label = appHelperTools.CreateLabel(name,style.LabelFont2p5,style.Attacklabel)
        name_label.setMinimumWidth(10)

        bonus_value = self.ABS[item.getScaling()].get_total_bonus()

        sign = ruleTools.sign_string(bonus_value)
        bonus = sign + str(bonus_value)
        bonus_label = appHelperTools.CreateLabel(bonus,style.LabelFont2p5,style.Attacklabel)

        damage = str(item["damage_dice"]) + " " + str(item["damage_type"])
        damage_label = appHelperTools.CreateLabel(damage,style.LabelFont2p5,style.Attacklabel)

        subtract_button = appHelperTools.CreateGenButton(stylesheet=style.ItemEditButton,
                                       icon_url=imageURLS.MinusUrl, icon_size=QtCore.QSize(20, 20),
                                       function=partial(self.subtractItem, item))

        return name_label,bonus_label,damage_label,subtract_button

    def addWindow(self):
        self.add_w = pyqt5_Custom_Windows.AddWindow(self.tinventory,self.ATiventory, self.update)
        self.add_w.show()

    def subtractItem(self,item):
        self.ATiventory.remove_item(item.get_key_name())
        self.update()


class FinishedSignal(QObject):
    finishedit = pyqtSignal()


class trait_box(QTextEdit):

    def __init__(self, text:str, font, connectingFunction):
        super().__init__()
        self.setFont(font)
        self.setText(text)
        self.signal = FinishedSignal()
        self.signal.finishedit.connect(connectingFunction)

    def focusOutEvent(self, e):
        super(trait_box,self).focusOutEvent(e)
        self.signal.finishedit.emit()
        self.setReadOnly(True)

    def mousePressEvent(self, e):
        self.setReadOnly(False)
        super(trait_box, self).mousePressEvent(e)


class RPTraitWidget:

    def __init__(self, rp_traits):
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)

        self.rp_traits = rp_traits

        frame1, ptext = self.create_trait_box("Peronality Trait", self.rp_traits["person"].get_text())
        frame2, itext = self.create_trait_box("Ideals", self.rp_traits["ideals"].get_text())
        frame3, btext = self.create_trait_box("Bonds", self.rp_traits["bonds"].get_text())
        frame4, ftext = self.create_trait_box("Flaws", self.rp_traits["flaws"].get_text())

        max_width = 400

        frame1.setMaximumWidth(max_width)
        frame2.setMaximumWidth(max_width)
        frame3.setMaximumWidth(max_width)
        frame4.setMaximumWidth(max_width)


        self.boxes = {
            "person": ptext,
            "ideals": itext,
            "bonds": btext,
            "flaws": ftext
        }

        main_layout.addWidget(appHelperTools.CreateSeperator())
        main_layout.addWidget(appHelperTools.CreateSeperator())
        main_layout.addWidget(frame1)
        main_layout.addWidget(frame2)
        main_layout.addWidget(frame3)
        main_layout.addWidget(frame4)
        main_layout.addWidget(appHelperTools.CreateSeperator())
        main_layout.addWidget(appHelperTools.CreateSeperator())

    def update(self):
        for name in list(self.boxes):
            self.boxes[name].setText(self.rp_traits[name].get_text())

    def get_widget(self):
        return self.main_widget

    def create_trait_box(self, label_input:str, text:str):
        frame = QFrame()
        frame.setFrameShape(QFrame.Panel)
        frame.setMaximumWidth(600)
        frame.setMinimumWidth(200)
        layout = QVBoxLayout(frame)

        font = QFont('Times', 15, QFont.StyleItalic)
        font.setWeight(12)
        font.setItalic(True)

        textbox = trait_box(text, font, partial(self.save_text))

        label = QLabel()
        label.setFont(style.LabelFont2)
        label.setText(label_input)

        layout.addWidget(textbox)
        layout.addWidget(label)

        return frame, textbox

    def save_text(self):
        for name in list(self.boxes):
            self.rp_traits[name].set_text(self.boxes[name].toPlainText())


class InventoryWidget:

    def __init__(self,tinventory:charManagers.Inventory):
        self.main_widget = QFrame()
        self.main_widget.setFrameShape(QFrame.Panel)

        inventory_layout = QVBoxLayout(self.main_widget)

        top_sub_layout = QHBoxLayout()

        money_style = "QLabel { border-radius: 9px}"

        money_layout = QGridLayout()

        money_text = ["CP", "SP","EP","GP","PP"]

        self.tinventory = tinventory
        self.items = tinventory.get_all_items()
        money_value = self.tinventory.get_money()

        self.widgets = {}
        for i in range(5):
            money_layout.addWidget(appHelperTools.CreateSeperator(), 0, i)

        """Money___________________________________________________________________"""
        self.widgets["currency_amounts"] = []
        for i in range(1,2*len(money_text)+1,2):
            # CURRENTY DENOMINATION LABELS
            money_layout.addWidget(appHelperTools.CreateLabel(money_text[int(i / 2)], style.LabelFont1, money_style), i, 1)
            money_layout.addWidget(appHelperTools.CreateSeperator(), i + 1, 1)

            # CURRENCY AMOUNT LABELS
            self.widgets["currency_amounts"] += [appHelperTools.CreateLabel(str(money_value[int(i / 2)]), style.LabelFont1, money_style)]
            money_layout.addWidget(self.widgets["currency_amounts"][int(i/2)], i, 3)
            money_layout.addWidget(appHelperTools.CreateSeperator(), i + 1, 3)
            # V SEPERATORS

            money_layout.addWidget(appHelperTools.CreateVSeperator(), i, 0)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i + 1, 0)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i, 2)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i + 1, 2)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i, 4)
            money_layout.addWidget(appHelperTools.CreateVSeperator(), i + 1, 4)

        """Inventory Stats_______________________________________________________"""

        inventory_status_widget = QFrame()
        inventory_status_layout = QVBoxLayout(inventory_status_widget)
        inventory_status_widget.setFrameShape(QFrame.WinPanel)

        encumberance_widget = QFrame()
        encumberance_widget.setFrameShape(QFrame.Panel)
        encumberance_layout = QVBoxLayout(encumberance_widget)

        encumberance_status_layout = QHBoxLayout()
        encumberance_status_label0 = appHelperTools.CreateLabel(
            "Weight: ",style.LabelFontSmallBold)
        self.encumberance_status_label1 = appHelperTools.CreateLabel(
            self.tinventory.encumberance.get_encumberance_word_status(),style.LabelFontBigBold)
        encumberance_status_label0.setMaximumHeight(25)
        encumberance_status_label0.setMaximumWidth(70)
        self.encumberance_status_label1.setMaximumHeight(25)
        self.encumberance_status_label1.setMaximumWidth(400)

        encumberance_status_layout.addWidget(encumberance_status_label0,stretch=1,alignment=QtCore.Qt.AlignLeft)
        encumberance_status_layout.addWidget(self.encumberance_status_label1,stretch=4,alignment=QtCore.Qt.AlignLeft)
        encumberance_status_layout.setContentsMargins(0, 0, 0, 0)

        # self.encumberance_status_label.setMaximumHeight(20)
        encumberance_layout.addLayout(encumberance_status_layout,stretch=1)

        self.encumberance_label = EncumberanceLabel(self.tinventory.encumberance)
        encumberance_layout.addWidget(self.encumberance_label,stretch=3)
        inventory_status_layout.addWidget(encumberance_widget)

        """ Inventory Options________________________________________________________"""

        inventory_options_widget = QFrame()
        inventory_options_layout = QVBoxLayout(inventory_options_widget)
        inventory_options_widget.setFrameShape(QFrame.WinPanel)

        sorting_widget = QFrame()
        sorting_widget.setFrameShape(QFrame.Panel)
        sorting_layout = QVBoxLayout(sorting_widget)
        sorting_layout.addWidget(appHelperTools.CreateLabel("Sorting",style.LabelFont1))

        inventory_options_layout.addWidget(sorting_widget)

        # Sorting buttons__________
        sorting_button_style = style.TabButtonSheet2
        alpha = appHelperTools.CreateGenButton("Alphabetical",style.LabelFont2,sorting_button_style,checkbox=True)
        weight = appHelperTools.CreateGenButton("Weight", style.LabelFont2,sorting_button_style,checkbox=True)
        typet = appHelperTools.CreateGenButton("Category", style.LabelFont2,sorting_button_style,checkbox=True)
        cost = appHelperTools.CreateGenButton("Cost", style.LabelFont2,sorting_button_style,checkbox=True)
        amount = appHelperTools.CreateGenButton("Amount", style.LabelFont2,sorting_button_style,checkbox=True)
        reversal = appHelperTools.CreateGenButton("Reverse", style.LabelFont2,
                                                  sorting_button_style,partial(self.reverse_order),checkbox=True)

        checkboxes = {
            "name":alpha,
            "weight":weight,
            "type":typet,
            "cost":cost,
            "amount":amount,
        }

        for key in checkboxes:
            appHelperTools.ConnectButtonCLicked(checkboxes[key], partial(self.change_order,key,checkboxes))

        sorting_layout.addWidget(alpha)
        sorting_layout.addWidget(typet)
        sorting_layout.addWidget(amount)
        sorting_layout.addWidget(cost)
        sorting_layout.addWidget(weight)
        sorting_layout.addWidget(reversal)

        search_layout = QHBoxLayout()
        self.searchbar = QLineEdit()
        self.searchbar.textEdited.connect(self.update)

        cancel_search = appHelperTools.CreateGenButton(
            stylesheet=style.ItemEditButton,
            icon_url=imageURLS.XUrl,
            icon_size=QtCore.QSize(20, 20),
            function_list=[partial(self.searchbar.setText,''),self.update]
        )

        search_layout.addWidget(self.searchbar)
        search_layout.addWidget(cancel_search)
        sorting_layout.addLayout(search_layout)

        """Inventory Proper___________________________________________"""
        inventory_proper_widget = QFrame()
        inventory_proper_layout = QVBoxLayout(inventory_proper_widget)
        inventory_proper_widget.setFrameShape(QFrame.Box)

        self.stacked_proper = QStackedLayout()
        self.stacked_proper.setAlignment(QtCore.Qt.AlignTop)
        inventory_proper_layout.addLayout(self.stacked_proper)


        self.create_item_labels()

        """Layout Adding____________________________________________"""

        top_sub_layout.addLayout(money_layout,stretch=1)
        top_sub_layout.addWidget(inventory_status_widget, stretch=2)
        top_sub_layout.addWidget(inventory_options_widget, stretch=2)

        inventory_layout.addLayout(top_sub_layout, stretch=1)
        inventory_layout.addWidget(inventory_proper_widget, stretch=3)

        # Inventory ________________________________________________________

    def switch_tab(self, index: int):
        self.stacked_proper.setCurrentIndex(index)

    def make_stacked_layout(self):
        items = self.items
        print(len(items))

        num_of_items = len(items)
        num_per_column = 10
        num_of_pages = int(np.ceil(num_of_items / (num_per_column * 2)))

        j = 0
        for i in range(num_of_pages):
            # Each page list items in range -> [i*16,i*16 + 16)

            current_page_widget = QWidget()
            current_page_outer0_layout = QVBoxLayout()

            current_page_outer1_layout = QHBoxLayout()
            current_page_left_layout = QGridLayout()
            current_page_right_layout = QGridLayout()
            current_page_button_layout = QHBoxLayout()

            current_page_widget.setLayout(current_page_outer0_layout)
            current_page_outer0_layout.addLayout(current_page_outer1_layout)
            current_page_outer0_layout.addLayout(current_page_button_layout)
            current_page_outer1_layout.addLayout(current_page_left_layout)
            current_page_outer1_layout.addLayout(current_page_right_layout)

            for k in range(num_per_column):
                if j < num_of_items:
                    current_page_left_layout.addWidget(appHelperTools.ItemLabel(items[j]), k, 0)
                    j += 1

            for k in range(num_per_column):
                if j < num_of_items:
                    current_page_right_layout.addWidget(appHelperTools.ItemLabel(items[j]), k, 0)
                    j += 1

            if i > 0:
                left_button = appHelperTools.CreateTabButton(self.switch_tab, i - 1, style.LabelFont2, style.TabButtonSheet1, "<-")
                current_page_button_layout.addWidget(left_button,alignment=QtCore.Qt.AlignBottom)

            if i < num_of_pages - 1:
                right_button = appHelperTools.CreateTabButton(self.switch_tab, i + 1, style.LabelFont2, style.TabButtonSheet1, "->")
                current_page_button_layout.addWidget(right_button,alignment=QtCore.Qt.AlignBottom)

            # current_page_outer0_layout.setAlignment(QtCore.Qt.AlignTop)
            # current_page_outer1_layout.setAlignment(QtCore.Qt.AlignTop)
            self.stacked_proper.addWidget(current_page_widget)

    def get_widget(self):
        return self.main_widget

    def update(self):
        money_value = self.tinventory.get_money()
        for i in range(len(self.widgets["currency_amounts"])):
            self.widgets["currency_amounts"][i].setText(str(money_value[i]))

        self.items = self.tinventory.get_items(self.searchbar.text())
        print(self.tinventory.order)
        self.create_item_labels()
        self.encumberance_label.update()
        self.encumberance_status_label1.setText(self.tinventory.encumberance.get_encumberance_word_status())

    def change_order(self,order:str,checkboxes):
        self.tinventory.set_sorting(order)
        # self.search_items = self.tinventory.get_all_items()
        for key in checkboxes:
            if key != order:
                checkboxes[key].setChecked(False)
        self.update()

    def reverse_order(self):
        self.tinventory.reversal()
        self.update()

    def create_item_labels(self):
        appHelperTools.deleteItemsOfLayout(self.stacked_proper)
        self.make_stacked_layout()


class EncumberanceLabel(QFrame):

    num_of_bars =15

    def __init__(self, encumberance:ruleTools.Encumbrance):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setFrameShape(QFrame.Panel)
        self.encumberance = encumberance
        self.create_bar_widget()

    def create_bar_widget(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        bar_layout = QGridLayout(frame)

        set_points = self.encumberance.get_encumberance_levels()
        max_weight = set_points[2]
        if max_weight == 0:
            max_weight = 1
        lvl2 = int(self.num_of_bars - 1)   # minus for 0 index
        lvl1 = int((set_points[1] / max_weight) * self.num_of_bars) - 1
        lvl0 = int((set_points[0] / max_weight) * self.num_of_bars) - 1

        fill_color = ["gainsboro","palegoldenrod","sandybrown","indianred"]
        past_bar = [False,False,False,False]
        current_weight = self.encumberance.get_weight()
        if current_weight >= max_weight:
            current_weight_bar = lvl2
            # current_weight_bar = int((current_weight / max_weight) * self.num_of_bars)
            # print(current_weight_bar)
            # print(lvl2)
        else:
            current_weight_bar = int((current_weight / max_weight) * self.num_of_bars)

        k = self.num_of_bars - 1
        current_level = 0
        weight_style = style.LabelFont2
        for i in range(self.num_of_bars):
            if i == lvl0 and not past_bar[0]:
                current_level += 1
                past_bar[0] = True
                current_weight_marker = appHelperTools.CreateLabel(str(set_points[0]) + " lbs-", weight_style)
                policy = current_weight_marker.sizePolicy()
                policy.setVerticalPolicy(policy.Policy.Maximum)
                policy.setHorizontalPolicy(policy.Policy.Maximum)
                current_weight_marker.setSizePolicy(policy)
                bar_layout.addWidget(current_weight_marker, k, 0)

            if i == lvl1 and not past_bar[1]:
                current_level += 1
                past_bar[1] = True
                current_weight_marker = appHelperTools.CreateLabel(str(set_points[1]) + " lbs-", weight_style)
                policy = current_weight_marker.sizePolicy()
                policy.setVerticalPolicy(policy.Policy.Maximum)
                policy.setHorizontalPolicy(policy.Policy.Maximum)
                current_weight_marker.setSizePolicy(policy)
                bar_layout.addWidget(current_weight_marker, k, 0)

            if i == lvl2 and not past_bar[2]:
                current_level += 1
                past_bar[2] = True
                current_weight_marker = appHelperTools.CreateLabel(str(set_points[2]) + " lbs-", weight_style)
                policy = current_weight_marker.sizePolicy()
                policy.setVerticalPolicy(policy.Policy.Maximum)
                policy.setHorizontalPolicy(policy.Policy.Maximum)
                current_weight_marker.setSizePolicy(policy)
                bar_layout.addWidget(current_weight_marker, k, 0)

            if i <= current_weight_bar:
                color = fill_color[current_level]
                opacity = .7
            else:
                color = fill_color[current_level]
                opacity = .2

            if i == current_weight_bar:
                current_weight_marker = appHelperTools.CreateLabel("-" + str(current_weight) + "lbs", style.LabelFont2)
                policy = current_weight_marker.sizePolicy()
                policy.setVerticalPolicy(policy.Policy.Maximum)
                policy.setHorizontalPolicy(policy.Policy.Maximum)
                current_weight_marker.setSizePolicy(policy)
                bar_layout.addWidget(current_weight_marker, k, 2)


            bar = appHelperTools.MakeColorWidget(color,opacity)

            bar_layout.addWidget(bar,k,1)
            k -= 1

        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setSpacing(1)

        self.layout.addWidget(frame)

    def update(self):
        appHelperTools.deleteItemsOfLayout(self.layout)
        delete(self.layout)
        self.layout = QVBoxLayout(self)
        self.create_bar_widget()





