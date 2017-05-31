from PyQt5 import QtCore, QtGui, QtWidgets
import time
from qtui import mainmenu, miss_ingredients, pump_set_ui, drink_list, pouring, manual_pour
from xml.etree import ElementTree
import pump_setup
import threading

AppLocation = '/data/Drink_Machine/'
library = ElementTree.parse(AppLocation + 'recipes')
my_recipes = library.findall('drinks/drink')
possible_drinks = my_recipes
pumpset = ElementTree.parse(AppLocation + 'pump_settings')
pumps = pumpset.findall('pumps/pump')


class MainWindow(QtWidgets.QMainWindow, mainmenu.Ui_MainMenu):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.background = QtGui.QPalette()
        self.background.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(AppLocation + 'images/MainScreen.jpg')))
        self.setPalette(self.background)

        self.btn_drink.clicked.connect(self.drink_set)
        self.btn_recipe.clicked.connect(self.recipe_set)
        self.btn_bar.clicked.connect(self.bar_set)
        self.btn_pump.clicked.connect(self.pump_set)
        self.btn_exit.clicked.connect(self.close)

    def drink_set(self):
        drink_list.show()

    def recipe_set(self):
        pass

    def bar_set(self):
        pass

    def pump_set(self):
        Pumps.show()


class DrinksList(QtWidgets.QWidget, drink_list.Ui_DrinkList):
    def __init__(self):
        super(DrinksList, self).__init__()
        self.setupUi(self)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.image_path = ''

        self.setPalette(Main_Window.background)
        self.lbl_ingredients.setStyleSheet('color: white')
        self.lbl_instructions.setStyleSheet('color: white')
        self.box_drinklbl.setStyleSheet('color: white')

        for i in possible_drinks:
            self.drink_menu.addItem(i.find('name').text)
        self.drink_menu.currentItemChanged.connect(self.populate)
        self.btn_back.clicked.connect(self.hide)

        self.btn_pour.clicked.connect(self.pour_selected)
        self.btn_manual.clicked.connect(self.manual_pour)

    def populate(self):
        drink = self.drink_menu.currentItem().text()
        for d in possible_drinks:
            if d.find('name').text != drink:
                continue
            else:
                self.box_drinklbl.setTitle(drink)
                self.lbl_instructions.setText('Instructions:\n' + d.find('instruction').text)
                ingredients = []
                for booze in d.findall('ingredients/booze'):
                    ingredients.append('-' + booze.get('name'))
                ingredients = '\n'.join(ingredients)
                self.lbl_ingredients.setText('\n\nIngredients:\n' + ingredients)
                self.image_path = AppLocation + 'images/' + d.find('image').text
                self.lbl_image.setPixmap(QtGui.QPixmap(self.image_path))

    def pour_selected(self):
        Prep.setup_pour(self.drink_menu.currentItem().text())
        # drink_image_bkground = QtGui.QPalette()
        # drink_image_bkground.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(self.image_path)))
        # Prep.setPalette(drink_image_bkground)
        Prep.show()

    def manual_pour(self):
        Manual.populate()
        Manual.show()


class PrepWindow(QtWidgets.QWidget, pouring.Ui_PourWindow):
    def __init__(self):
        super(PrepWindow, self).__init__()
        self.setupUi(self)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.setPalette(Main_Window.background)

        self.drink = ''
        self.instruction = ''
        self.garnish = ''
        self.ingredients = []
        self.multiplier = 1.00
        self.abort = False

        self.btn_back.clicked.connect(self.hide)
        self.doubleSpinBox.valueChanged.connect(self.update)
        self.btn_stop.clicked.connect(self.all_stop)
        self.btn_pour.clicked.connect(self.serve_clicked)

    def update(self):
        self.multiplier = self.doubleSpinBox.value()
        self.dsp_name.setText(self.drink)
        self.dsp_instructions.setText(self.instruction + '\n\n-Optional garnishes:\n' + self.garnish)
        ingredient_str = ''
        for i in self.ingredients:
            ingredient_str += i[0] + ' - ' + str(float(i[1]) * self.multiplier) + 'oz\n'
        self.dsp_ingredients.setText(ingredient_str)

    def all_stop(self):
        self.abort = True
        Pumps.p1.stop()
        Pumps.p2.stop()
        Pumps.p3.stop()
        Pumps.p4.stop()
        Pumps.p5.stop()
        Pumps.p6.stop()
        Pumps.p7.stop()
        Pumps.p8.stop()
        Pumps.p9.stop()
        Pumps.p10.stop()
        Pumps.p11.stop()
        Pumps.p12.stop()

    def serve_clicked(self):
        threading.Thread(target=self.serve).start()

    def serve(self):
        missing = []
        for i in self.ingredients:
            found = False
            for p in Pumps.all_pumps:
                if i[0] == p.booze:
                    found = True
                    break
            if not found:
                missing.append(i)
        if missing == [] :
            missing_window.label.setText('There are no missing ingredients.\n'
                                         'Your drink will be ready in a moment.')
            missing_window.populate(missing, self.multiplier, self.instruction)
        else:
            missing_window.label.setText('The following ingredients are not in the machine.\n'
                                         'Please add them to your drink according to the instructions.')
            missing_window.populate(missing, self.multiplier, self.instruction)
        missing_window.show()

        active_threads = threading.activeCount()

        for i in self.ingredients:
            if self.abort: break
            for p in Pumps.all_pumps:
                if self.abort: break
                if i[0] == p.booze:
                    while threading.activeCount() >= active_threads + 4:
                        time.sleep(.5)
                        if self.abort: break
                    if self.abort: break
                    threading.Thread(target=p.pour, args=(float(i[1]) * float(self.multiplier), )).start()
                    break
                else:
                    continue
        while threading.activeCount() > active_threads:
            continue
        self.abort = False
        self.hide()
        Manual.pouring = False
        Manual.btn_start.setText('Start')

    def setup_pour(self, drink):
        for d in my_recipes:
            if d.find('name').text != drink:
                continue
            else:
                self.drink = drink
                self.instruction = d.find('instruction').text
                self.garnish = d.find('garnish').text
                self.ingredients = []
                for booze in d.findall('ingredients/booze'):
                    self.ingredients.append([booze.get('name'), booze.text])
                self.update()
                self.show()
                break


class MissingIngredients(QtWidgets.QWidget, miss_ingredients.Ui_MissingIngredients):
    def __init__(self):
        super(MissingIngredients, self).__init__()
        self.setupUi(self)
        self.setGeometry(150, 70, 500, 375)

        self.btn_ok.clicked.connect(self.hide)
        self.btn_stop.clicked.connect(self.stop)

    def stop(self):
        Prep.all_stop()
        Prep.show()
        self.hide()

    def populate(self, ingredients, serving_size, instructions):
        ing_list = ''
        for i in ingredients:
            ing_list += i[0] + ' - ' + str(float(i[1]) * serving_size) + '\n'
        self.dsp_miss_ingredients.setText(ing_list)
        self.dsp_instructions.setText(instructions)


class PumpSetup(QtWidgets.QWidget, pump_set_ui.Ui_PumpSettings):
    def __init__(self):
        super(PumpSetup, self).__init__()
        self.setupUi(self)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.setPalette(Main_Window.background)

        self.active_pump = object
        self.testing = False
        self.calibrating = False
        self.time_start = float
        self.time_stop = float

        # Declare pump objects so they can be defined in self.setupPumps().
        self.p1 = object
        self.p2 = object
        self.p3 = object
        self.p4 = object
        self.p5 = object
        self.p6 = object
        self.p7 = object
        self.p8 = object
        self.p9 = object
        self.p10 = object
        self.p11 = object
        self.p12 = object
        self.setupPumps()
        self.all_pumps = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6,
                          self.p7, self.p8, self.p9, self.p10, self.p11, self.p12]

        self.btn_pump1.clicked.connect(self.pump1_click)
        self.btn_pump2.clicked.connect(self.pump2_click)
        self.btn_pump3.clicked.connect(self.pump3_click)
        self.btn_pump4.clicked.connect(self.pump4_click)
        self.btn_pump5.clicked.connect(self.pump5_click)
        self.btn_pump6.clicked.connect(self.pump6_click)
        self.btn_pump7.clicked.connect(self.pump7_click)
        self.btn_pump8.clicked.connect(self.pump8_click)
        self.btn_pump9.clicked.connect(self.pump9_click)
        self.btn_pump10.clicked.connect(self.pump10_click)
        self.btn_pump11.clicked.connect(self.pump11_click)
        self.btn_pump12.clicked.connect(self.pump12_click)
        self.btn_back.clicked.connect(self.hide)
        self.btn_save.clicked.connect(self.save_settings)
        self.btn_calibrate.clicked.connect(self.calibrate_click)
        self.btn_prime.clicked.connect(self.test)

    def setupPumps(self):
        self.p1 = pump_setup.Pumps()
        self.p1.number = int(pumps[0].find('number').text)
        self.p1.booze = pumps[0].find('liquor').text
        self.p1.flavor = pumps[0].find('flavor').text
        self.p1.brand = pumps[0].find('brand').text
        self.p1.bottle_size = float(pumps[0].find('bottle').text)
        self.p1.oz_left = float(pumps[0].find('ozleft').text)
        self.p1.oz_notify = float(pumps[0].find('oznotify').text)
        self.p1.oneoz_timing = float(pumps[0].find('oneoz_timing').text)
        self.p1.reverse_pump = pumps[0].find('reverse').text
        self.p1.speed = int(pumps[0].find('speed').text)
        self.p1.pump = pump_setup.hat1.getMotor(1)

        self.p2 = pump_setup.Pumps()
        self.p2.number = int(pumps[1].find('number').text)
        self.p2.booze = pumps[1].find('liquor').text
        self.p2.flavor = pumps[1].find('flavor').text
        self.p2.brand = pumps[1].find('brand').text
        self.p2.bottle_size = float(pumps[1].find('bottle').text)
        self.p2.oz_left = float(pumps[1].find('ozleft').text)
        self.p2.oz_notify = float(pumps[1].find('oznotify').text)
        self.p2.oneoz_timing = float(pumps[1].find('oneoz_timing').text)
        self.p2.reverse_pump = pumps[1].find('reverse').text
        self.p2.speed = int(pumps[1].find('speed').text)
        self.p2.pump = pump_setup.hat1.getMotor(2)

        self.p3 = pump_setup.Pumps()
        self.p3.number = int(pumps[2].find('number').text)
        self.p3.booze = pumps[2].find('liquor').text
        self.p3.flavor = pumps[2].find('flavor').text
        self.p3.brand = pumps[2].find('brand').text
        self.p3.bottle_size = float(pumps[2].find('bottle').text)
        self.p3.oz_left = float(pumps[2].find('ozleft').text)
        self.p3.oz_notify = float(pumps[2].find('oznotify').text)
        self.p3.oneoz_timing = float(pumps[2].find('oneoz_timing').text)
        self.p3.reverse_pump = pumps[2].find('reverse').text
        self.p3.speed = int(pumps[2].find('speed').text)
        self.p3.pump = pump_setup.hat1.getMotor(3)

        self.p4 = pump_setup.Pumps()
        self.p4.number = int(pumps[3].find('number').text)
        self.p4.booze = pumps[3].find('liquor').text
        self.p4.flavor = pumps[3].find('flavor').text
        self.p4.brand = pumps[3].find('brand').text
        self.p4.bottle_size = float(pumps[3].find('bottle').text)
        self.p4.oz_left = float(pumps[3].find('ozleft').text)
        self.p4.oz_notify = float(pumps[3].find('oznotify').text)
        self.p4.oneoz_timing = float(pumps[3].find('oneoz_timing').text)
        self.p4.reverse_pump = pumps[3].find('reverse').text
        self.p4.speed = int(pumps[3].find('speed').text)
        self.p4.pump = pump_setup.hat1.getMotor(4)

        self.p5 = pump_setup.Pumps()
        self.p5.number = int(pumps[4].find('number').text)
        self.p5.booze = pumps[4].find('liquor').text
        self.p5.flavor = pumps[4].find('flavor').text
        self.p5.brand = pumps[4].find('brand').text
        self.p5.bottle_size = float(pumps[4].find('bottle').text)
        self.p5.oz_left = float(pumps[4].find('ozleft').text)
        self.p5.oz_notify = float(pumps[4].find('oznotify').text)
        self.p5.oneoz_timing = float(pumps[4].find('oneoz_timing').text)
        self.p5.reverse_pump = pumps[4].find('reverse').text
        self.p5.speed = int(pumps[4].find('speed').text)
        self.p5.pump = pump_setup.hat2.getMotor(1)

        self.p6 = pump_setup.Pumps()
        self.p6.number = int(pumps[5].find('number').text)
        self.p6.booze = pumps[5].find('liquor').text
        self.p6.flavor = pumps[5].find('flavor').text
        self.p6.brand = pumps[5].find('brand').text
        self.p6.bottle_size = float(pumps[5].find('bottle').text)
        self.p6.oz_left = float(pumps[5].find('ozleft').text)
        self.p6.oz_notify = float(pumps[5].find('oznotify').text)
        self.p6.oneoz_timing = float(pumps[5].find('oneoz_timing').text)
        self.p6.reverse_pump = pumps[5].find('reverse').text
        self.p6.speed = int(pumps[5].find('speed').text)
        self.p6.pump = pump_setup.hat2.getMotor(2)

        self.p7 = pump_setup.Pumps()
        self.p7.number = int(pumps[6].find('number').text)
        self.p7.booze = pumps[6].find('liquor').text
        self.p7.flavor = pumps[6].find('flavor').text
        self.p7.brand = pumps[6].find('brand').text
        self.p7.bottle_size = float(pumps[6].find('bottle').text)
        self.p7.oz_left = float(pumps[6].find('ozleft').text)
        self.p7.oz_notify = float(pumps[6].find('oznotify').text)
        self.p7.oneoz_timing = float(pumps[6].find('oneoz_timing').text)
        self.p7.reverse_pump = pumps[6].find('reverse').text
        self.p7.speed = int(pumps[6].find('speed').text)
        self.p7.pump = pump_setup.hat2.getMotor(3)

        self.p8 = pump_setup.Pumps()
        self.p8.number = int(pumps[7].find('number').text)
        self.p8.booze = pumps[7].find('liquor').text
        self.p8.flavor = pumps[7].find('flavor').text
        self.p8.brand = pumps[7].find('brand').text
        self.p8.bottle_size = float(pumps[7].find('bottle').text)
        self.p8.oz_left = float(pumps[7].find('ozleft').text)
        self.p8.oz_notify = float(pumps[7].find('oznotify').text)
        self.p8.oneoz_timing = float(pumps[7].find('oneoz_timing').text)
        self.p8.reverse_pump = pumps[7].find('reverse').text
        self.p8.speed = int(pumps[7].find('speed').text)
        self.p8.pump = pump_setup.hat2.getMotor(4)

        self.p9 = pump_setup.Pumps()
        self.p9.number = int(pumps[8].find('number').text)
        self.p9.booze = pumps[8].find('liquor').text
        self.p9.flavor = pumps[8].find('flavor').text
        self.p9.brand = pumps[8].find('brand').text
        self.p9.bottle_size = float(pumps[8].find('bottle').text)
        self.p9.oz_left = float(pumps[8].find('ozleft').text)
        self.p9.oz_notify = float(pumps[8].find('oznotify').text)
        self.p9.oneoz_timing = float(pumps[8].find('oneoz_timing').text)
        self.p9.reverse_pump = pumps[8].find('reverse').text
        self.p9.speed = int(pumps[8].find('speed').text)
        self.p9.pump = pump_setup.hat3.getMotor(1)

        self.p10 = pump_setup.Pumps()
        self.p10.number = int(pumps[9].find('number').text)
        self.p10.booze = pumps[9].find('liquor').text
        self.p10.flavor = pumps[9].find('flavor').text
        self.p10.brand = pumps[9].find('brand').text
        self.p10.bottle_size = float(pumps[9].find('bottle').text)
        self.p10.oz_left = float(pumps[9].find('ozleft').text)
        self.p10.oz_notify = float(pumps[9].find('oznotify').text)
        self.p10.oneoz_timing = float(pumps[9].find('oneoz_timing').text)
        self.p10.reverse_pump = pumps[9].find('reverse').text
        self.p10.speed = int(pumps[9].find('speed').text)
        self.p10.pump = pump_setup.hat3.getMotor(2)

        self.p11 = pump_setup.Pumps()
        self.p11.number = int(pumps[10].find('number').text)
        self.p11.booze = pumps[10].find('liquor').text
        self.p11.flavor = pumps[10].find('flavor').text
        self.p11.brand = pumps[10].find('brand').text
        self.p11.bottle_size = float(pumps[10].find('bottle').text)
        self.p11.oz_left = float(pumps[10].find('ozleft').text)
        self.p11.oz_notify = float(pumps[10].find('oznotify').text)
        self.p11.oneoz_timing = float(pumps[10].find('oneoz_timing').text)
        self.p11.reverse_pump = pumps[10].find('reverse').text
        self.p11.speed = int(pumps[10].find('speed').text)
        self.p11.pump = pump_setup.hat3.getMotor(3)

        self.p12 = pump_setup.Pumps()
        self.p12.number = int(pumps[11].find('number').text)
        self.p12.booze = pumps[11].find('liquor').text
        self.p12.flavor = pumps[11].find('flavor').text
        self.p12.brand = pumps[11].find('brand').text
        self.p12.bottle_size = float(pumps[11].find('bottle').text)
        self.p12.oz_left = float(pumps[11].find('ozleft').text)
        self.p12.oz_notify = float(pumps[11].find('oznotify').text)
        self.p12.oneoz_timing = float(pumps[11].find('oneoz_timing').text)
        self.p12.reverse_pump = pumps[11].find('reverse').text
        self.p12.speed = int(pumps[11].find('speed').text)
        self.p12.pump = pump_setup.hat3.getMotor(4)

    # Change the currently selected pump.
    def pump1_click(self):
        self.pumpbtn_change(self.btn_pump1)
        self.show_curr_pump(self.p1)
    def pump2_click(self):
        self.pumpbtn_change(self.btn_pump2)
        self.show_curr_pump(self.p2)
    def pump3_click(self):
        self.pumpbtn_change(self.btn_pump3)
        self.show_curr_pump(self.p3)
    def pump4_click(self):
        self.pumpbtn_change(self.btn_pump4)
        self.show_curr_pump(self.p4)
    def pump5_click(self):
        self.pumpbtn_change(self.btn_pump5)
        self.show_curr_pump(self.p5)
    def pump6_click(self):
        self.pumpbtn_change(self.btn_pump6)
        self.show_curr_pump(self.p6)
    def pump7_click(self):
        self.pumpbtn_change(self.btn_pump7)
        self.show_curr_pump(self.p7)
    def pump8_click(self):
        self.pumpbtn_change(self.btn_pump8)
        self.show_curr_pump(self.p8)
    def pump9_click(self):
        self.pumpbtn_change(self.btn_pump9)
        self.show_curr_pump(self.p9)
    def pump10_click(self):
        self.pumpbtn_change(self.btn_pump10)
        self.show_curr_pump(self.p10)
    def pump11_click(self):
        self.pumpbtn_change(self.btn_pump11)
        self.show_curr_pump(self.p11)
    def pump12_click(self):
        self.pumpbtn_change(self.btn_pump12)
        self.show_curr_pump(self.p12)

    # Simply toggle between which of the 12 pump buttons is currently visually pushed down.
    def pumpbtn_change(self, btn):
        self.btn_pump1.setChecked(False)
        self.btn_pump2.setChecked(False)
        self.btn_pump3.setChecked(False)
        self.btn_pump4.setChecked(False)
        self.btn_pump5.setChecked(False)
        self.btn_pump6.setChecked(False)
        self.btn_pump7.setChecked(False)
        self.btn_pump8.setChecked(False)
        self.btn_pump9.setChecked(False)
        self.btn_pump10.setChecked(False)
        self.btn_pump11.setChecked(False)
        self.btn_pump12.setChecked(False)

        btn.setChecked(True)

    # Update the displayed pumps with the Pumps of the chosen pump.
    def show_curr_pump(self, pump):
        self.active_pump = pump

        self.dsp_curr_pump.setText('Pump ' + str(pump.number))
        self.dsp_booze.setText(pump.booze)
        self.dsp_flavor.setText(pump.flavor)
        self.dsp_brand.setText(pump.brand)
        self.dsp_bottle.setText(str(pump.bottle_size))
        self.dsp_ozleft.setText(str(pump.oz_left))
        self.dsp_timing.setText(str(pump.oneoz_timing))
        self.dsp_speed.setText(str(pump.speed))
        self.dsp_oznotify.setText(str(pump.oz_notify))
        if pump.reverse_pump == 'True':
            self.chk_reverse.setChecked(True)
        else:
            self.chk_reverse.setChecked(False)

    # Save the pumps back into the xml file when the save button is clicked.
    def save_settings(self):
        self.active_pump.booze = str(self.dsp_booze.text())
        self.active_pump.flavor = str(self.dsp_flavor.text())
        self.active_pump.brand = str(self.dsp_brand.text())
        self.active_pump.bottle_size = float(self.dsp_bottle.text())
        self.active_pump.oz_left = float(self.dsp_ozleft.text())
        self.active_pump.oneoz_timing = float(self.dsp_timing.text())
        self.active_pump.speed = int(self.dsp_speed.text())
        self.active_pump.oz_notify = float(self.dsp_oznotify.text())
        if self.chk_reverse.isChecked():
            self.active_pump.reverse_pump = 'True'
        else:
            self.active_pump.reverse_pump = 'False'

        pnum = self.active_pump.number - 1
        pumps[pnum].find('liquor').text = self.active_pump.booze
        pumps[pnum].find('flavor').text = self.active_pump.flavor
        pumps[pnum].find('brand').text = self.active_pump.brand
        pumps[pnum].find('bottle').text = str(self.active_pump.bottle_size)
        pumps[pnum].find('ozleft').text = str(self.active_pump.oz_left)
        pumps[pnum].find('oneoz_timing').text = str(self.active_pump.oneoz_timing)
        pumps[pnum].find('speed').text = str(self.active_pump.speed)
        pumps[pnum].find('oznotify').text = str(self.active_pump.oz_notify)
        pumps[pnum].find('reverse').text = self.active_pump.reverse_pump
        pumpset.write('pump_settings')

        self.show_curr_pump(self.active_pump)

    def calibrate_click(self):
        threading.Thread(target=self.calibrate).start()

    # Calibrate how long the pump needs to run in order to dispense 1 ounce.
    def calibrate(self):
        if self.calibrating:
            self.active_pump.stop()
            self.time_stop = time.time()
            self.calibrating = False
            self.btn_calibrate.setText('Calibrate Ounce')
            duration = (self.time_stop - self.time_start)
            duration = format(duration, '.2f')
            self.dsp_timing.setText(str(duration))
            self.save_settings()
        else:
            self.calibrating = True
            self.btn_calibrate.setText('Starting in... 3')
            time.sleep(1)
            self.btn_calibrate.setText('Starting in... 2')
            time.sleep(1)
            self.btn_calibrate.setText('Starting in... 1')
            time.sleep(1)
            self.btn_calibrate.setText('Press again when 1oz has been poured.')
            self.time_start = time.time()
            self.active_pump.start()

    def test(self):
        if self.testing:
            self.testing = False
            self.btn_prime.setText('Prime/Test Pump')
            self.active_pump.stop()
        else:
            self.save_settings()
            self.testing = True
            self.btn_prime.setText('Stop')
            self.active_pump.start()


class ManualPour(QtWidgets.QWidget, manual_pour.Ui_ManualPour):
    def __init__(self):
        super(ManualPour, self).__init__()
        self.setupUi(self)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setPalette(Main_Window.background)

        self.btn_reset.clicked.connect(self.reset)
        self.btn_start.clicked.connect(self.toggle_pour)
        self.btn_back.clicked.connect(self.hide)

        self.p1_dec_down.clicked.connect(lambda: self.decimal_change(self.p1_val_sbox, 'down'))
        self.p1_dec_up.clicked.connect(lambda: self.decimal_change(self.p1_val_sbox, 'up'))
        self.p2_dec_down.clicked.connect(lambda: self.decimal_change(self.p2_val_sbox, 'down'))
        self.p2_dec_up.clicked.connect(lambda: self.decimal_change(self.p2_val_sbox, 'up'))
        self.p3_dec_down.clicked.connect(lambda: self.decimal_change(self.p3_val_sbox, 'down'))
        self.p3_dec_up.clicked.connect(lambda: self.decimal_change(self.p3_val_sbox, 'up'))
        self.p4_dec_down.clicked.connect(lambda: self.decimal_change(self.p4_val_sbox, 'down'))
        self.p4_dec_up.clicked.connect(lambda: self.decimal_change(self.p4_val_sbox, 'up'))
        self.p5_dec_down.clicked.connect(lambda: self.decimal_change(self.p5_val_sbox, 'down'))
        self.p5_dec_up.clicked.connect(lambda: self.decimal_change(self.p5_val_sbox, 'up'))
        self.p6_dec_down.clicked.connect(lambda: self.decimal_change(self.p6_val_sbox, 'down'))
        self.p6_dec_up.clicked.connect(lambda: self.decimal_change(self.p6_val_sbox, 'up'))
        self.p7_dec_down.clicked.connect(lambda: self.decimal_change(self.p7_val_sbox, 'down'))
        self.p7_dec_up.clicked.connect(lambda: self.decimal_change(self.p7_val_sbox, 'up'))
        self.p8_dec_down.clicked.connect(lambda: self.decimal_change(self.p8_val_sbox, 'down'))
        self.p8_dec_up.clicked.connect(lambda: self.decimal_change(self.p8_val_sbox, 'up'))
        self.p9_dec_down.clicked.connect(lambda: self.decimal_change(self.p9_val_sbox, 'down'))
        self.p9_dec_up.clicked.connect(lambda: self.decimal_change(self.p9_val_sbox, 'up'))
        self.p10_dec_down.clicked.connect(lambda: self.decimal_change(self.p10_val_sbox, 'down'))
        self.p10_dec_up.clicked.connect(lambda: self.decimal_change(self.p10_val_sbox, 'up'))
        self.p11_dec_down.clicked.connect(lambda: self.decimal_change(self.p11_val_sbox, 'down'))
        self.p11_dec_up.clicked.connect(lambda: self.decimal_change(self.p11_val_sbox, 'up'))
        self.p12_dec_down.clicked.connect(lambda: self.decimal_change(self.p12_val_sbox, 'down'))
        self.p12_dec_up.clicked.connect(lambda: self.decimal_change(self.p12_val_sbox, 'up'))

        self.pouring = False
        self.manual_liquor_list = [[self.p1_box, self.p1_val_sbox], [self.p2_box, self.p2_val_sbox],
                                   [self.p3_box, self.p3_val_sbox], [self.p4_box, self.p4_val_sbox],
                                   [self.p5_box, self.p5_val_sbox], [self.p6_box, self.p6_val_sbox],
                                   [self.p7_box, self.p7_val_sbox], [self.p8_box, self.p8_val_sbox],
                                   [self.p9_box, self.p9_val_sbox], [self.p10_box, self.p10_val_sbox],
                                   [self.p11_box, self.p11_val_sbox], [self.p12_box, self.p12_val_sbox]]

    def decimal_change(self, sbox, direction):
        current = sbox.value()
        if direction == 'up':
            sbox.setValue(current + 0.1)
        else:
            sbox.setValue(current - 0.1)

    def populate(self):
        self.p1_box.setTitle(Pumps.p1.booze)
        self.p2_box.setTitle(Pumps.p2.booze)
        self.p3_box.setTitle(Pumps.p3.booze)
        self.p4_box.setTitle(Pumps.p4.booze)
        self.p5_box.setTitle(Pumps.p5.booze)
        self.p6_box.setTitle(Pumps.p6.booze)
        self.p7_box.setTitle(Pumps.p7.booze)
        self.p8_box.setTitle(Pumps.p8.booze)
        self.p9_box.setTitle(Pumps.p9.booze)
        self.p10_box.setTitle(Pumps.p10.booze)
        self.p11_box.setTitle(Pumps.p11.booze)
        self.p12_box.setTitle(Pumps.p12.booze)

    def reset(self):
        self.p1_val_sbox.setValue(0.0)
        self.p2_val_sbox.setValue(0.0)
        self.p3_val_sbox.setValue(0.0)
        self.p4_val_sbox.setValue(0.0)
        self.p5_val_sbox.setValue(0.0)
        self.p6_val_sbox.setValue(0.0)
        self.p7_val_sbox.setValue(0.0)
        self.p8_val_sbox.setValue(0.0)
        self.p9_val_sbox.setValue(0.0)
        self.p10_val_sbox.setValue(0.0)
        self.p11_val_sbox.setValue(0.0)
        self.p12_val_sbox.setValue(0.0)

    def toggle_pour(self):
        Prep.multiplier = 1.0
        Prep.ingredients = []
        if self.pouring == True:
            self.pouring = False
            Prep.all_stop()
            self.btn_start.setText('Start')
        else:
            self.pouring = True
            self.btn_start.setText('Stop')
            # Sort the list so that the ingredient with the longest pour time begins first.
            self.manual_liquor_list.sort(key=lambda x: float(x[1].value()), reverse=True)
            for liquor in self.manual_liquor_list:
                if liquor[1].value() != 0.0:
                    ingredient = liquor[0].title()
                    amount = liquor[1].value()
                    Prep.ingredients.append([ingredient, amount])
            Prep.serve_clicked()
            missing_window.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Main_Window = MainWindow()
    drink_list = DrinksList()
    Main_Window.show()

    Prep = PrepWindow()
    Pumps = PumpSetup()
    missing_window = MissingIngredients()
    Manual = ManualPour()

    sys.exit(app.exec_())
