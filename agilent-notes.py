import visa
import datetime
import time
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

voltage = 'MAXimum'
current = 'MAXimum'
state = True
slope = 'POSitive'

# Set the Voltage Levels here for Low and High Limited Tests
psVoltageLevelLimitedLow = 29
psVoltageLevelLimitedHigh = 31
psVoltageLevelFull = 30

maxCycTimeSpec = 1
maxCurrentSpec = 3
maxResSpec = 0.5
minResSpec = 1000000

numSpec = '1V35000'
testDate = datetime.datetime.now()
partNumber = '4xxx-201'

rm = visa.ResourceManager()
METIS_06676 = rm.open_resource('TCPIP0::K-34465A-06676::hislip0::INSTR')
GANYMEDE_03625 = rm.open_resource('TCPIP0::K-34465A-03625::hislip0::INSTR')
THEBE_00599 = rm.open_resource('TCPIP0::K-34465A-00599::hislip0::INSTR')
IO_06446 = rm.open_resource('TCPIP0::K-34465A-06446::hislip0::INSTR')
EUROPA_00866 = rm.open_resource('TCPIP0::K-34465A-00866::hislip0::INSTR')
CALLISTO_01437 = rm.open_resource('TCPIP0::K-34465A-01437::hislip0::INSTR')

AMALTHEA_04228 = rm.open_resource('TCPIP0::K-34465A-04428::hislip0::INSTR')
ADRASTEA_04250 = rm.open_resource('TCPIP0::K-34465A-04250::hislip0::INSTR')

JUPITER_ARMING_E3634A = rm.open_resource('GPIB0::2::INSTR')
JUPITER_SAFING_E3634A = rm.open_resource('GPIB0::3::INSTR')
JUPITER_GALILEO_E3634A = rm.open_resource('GPIB0::1::INSTR')

def main():

    def interrupterApp():
        firstInput = input("Hello. Welcome to Systima's Ordinance Interrupter Automated Test Bench...\n Please choose what you would like to do:\n (Please respond with:\n 1. Limited Bench Test at Low Voltage\n 2. Limited Bench Test at High Voltage\n 3. Full Bench Test: parts a,b,c,d,e)\n 4. Full Bench Test: part(f)\n 5. Full Bench Test: part(h)\n 6. Quit\n\n")

        if int(firstInput) == 1:
            interrupterApp.testType = 'Low-Voltage-Limited'
            print("You chose to do a Limited Bench Test at Low Volatge...")
            limitedTest(psVoltageLevelLimitedLow)
            print("Limited Bench Test at Low Voltage is Complete.")
        elif int(firstInput) == 2:
            interrupterApp.testType = 'High-Voltage-Limited'
            print("You chose to do a Limited Bench Test at High Voltage...")
            limitedTest(psVoltageLevelLimitedHigh)
            print("Limited Bench Test at High Voltage is Complete.")
        elif int(firstInput) == 3:
            interrupterApp.testType = 'Full-Bench-parts-ABCDE'
            print("You chose to do a Full Bench Test parts(a,b,c,d,e)...")
            limitedTest(psVoltageLevelFull)
            print("Full Bench Test part(a,b,c,d,e) at is Complete.")
        elif int(firstInput) == 4:
            interrupterApp.testType = 'Full-Bench-part-F'
            print("You chose to do a Full Bench Test part(f)...")
            fullTest(psVoltageLevelFull)
            print("Full Bench Test part(f) at is Complete.")
        elif int(firstInput) == 5:
            interrupterApp.testType = 'Full-Bench-part-H'
            print("You chose to do a Full Bench Test part(h)...")
            limitedArmToSafe(psVoltageLevelFull)
            print("Full Bench Test part(f) at is Complete.")
        else:
            print("Now halting the program.")
            quit()
        print("Okay...we're done with that one...Wanna do another?")

    def fullTest(psVoltageLevel):
        def getUserInitialData():
            getUserInitialData.operatorsName = input("What is your name (First, Last)?     ")
            getUserInitialData.serialNumber = input("What is the serial number stamped into the base of this Ordnance Interrupter?    ")
        def visualArmCheck():
            visualArmCheck.armedCondition = input("Can you see the Armed Indicator?:\n (Please respond with:\n 1. Armed\n 2. Safed\n\n")

            if visualArmCheck.armedCondition == 1 or 2:
               visualArmCheck.armedCondition = visualArmCheck.armedCondition
               print("Thank you. Now continuing test.....")
            else:
              print("Please respond with '1' or '2'")
        def visualSafeCheck():
            visualSafeCheck.safedCondition = input("Can you see the Safed Indicator?:\n (Please respond with:\n 1. Armed\n 2. Safed\n\n")

            if visualSafeCheck.safedCondition == 1 or 2:
               visualSafeCheck.safedCondition = visualSafeCheck.safedCondition
               print("Thank you. Now continuing test.....")
            else:
              print("Please respond with '1' or '2'")
        def simpleSafingCycle():
            print("Safing the Device...")
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_SAFING_E3634A.write('*CLS')
            JUPITER_SAFING_E3634A.write('*RST')
            JUPITER_SAFING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_SAFING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_SAFING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (1))
            time.sleep(0.256)
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            print("...finished safing the device")
        def configurePowerSupplyJupiterArming():
            print("Setting up Jupiter Arming...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            print("Jupiter-Arming Power Supply is now Configured")
        def configurePowerSupplyJupiterSafing():
            print("Setting up Jupiter Safing...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            print("Jupiter-Safing Power Supply is now Configured")
        def configurePowerSupplyGalileo():
            print("Setting up Galileo...")
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write('*CLS')
            JUPITER_GALILEO_E3634A.write('*RST')
            JUPITER_GALILEO_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (5.0))
            JUPITER_GALILEO_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_GALILEO_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            #JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            time.sleep(0.512)
            print("Galileo Power Supply is now Configured and Output is On")
        def setupDMM():
            METIS_06676.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_DC_CURRENT.sta'))
            METIS_06676.write(':TRIGger:SOURce %s' % ('IMMediate'))
            METIS_06676.write(':TRIGger:COUNt %G' % (1.0))
            METIS_06676.write(':SENSe:CURRent:DC:RANGe %G' % (0.01))
            METIS_06676.write(':SENSe:CURRent:DC:TERMinals %d' % (10))
            METIS_06676.write(':SAMPle:COUNt %d' % (16384))
            print("Metis is Configured")

            CALLISTO_01437.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_DC_CURRENT.sta'))
            CALLISTO_01437.write(':TRIGger:SOURce %s' % ('IMMediate'))
            CALLISTO_01437.write(':TRIGger:COUNt %G' % (1.0))
            CALLISTO_01437.write(':SENSe:CURRent:DC:RANGe %G' % (0.01))
            CALLISTO_01437.write(':SENSe:CURRent:DC:TERMinals %d' % (10))
            CALLISTO_01437.write(':SAMPle:COUNt %d' % (16384))
            print("Callisto is Configured")

            # Load DMM Voltage Configuration State Files
            GANYMEDE_03625.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            THEBE_00599.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            IO_06446.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            EUROPA_00866.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            AMALTHEA_04228_00866.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            ADRASTEA_04250.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))

            # Configure DMM for Voltage or Resistance on Safe Monitor #2
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            GANYMEDE_03625.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            GANYMEDE_03625.write(':TRIGger:COUNt %G' % (1.0))
            GANYMEDE_03625.write(':SAMPle:COUNt %d' % (16384))
            print("Ganymede is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            THEBE_00599.write(':TRIGger:COUNt %G' % (1.0))
            THEBE_00599.write(':SAMPle:COUNt %d' % (16384))
            print("Thebe is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            IO_06446.write(':TRIGger:COUNt %G' % (1.0))
            IO_06446.write(':SAMPle:COUNt %d' % (16384))
            print("Io is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            EUROPA_00866.write(':TRIGger:COUNt %G' % (1.0))
            EUROPA_00866.write(':SAMPle:COUNt %d' % (16384))
            time.sleep(0.128)
            print("Europa is Configured")

            # Configure DMM for Voltage oF Jupiter Safing with Amalthea
            AMALTHEA_04228.write(':TRIGger:SOURce %s' % ('IMMediate'))
            AMALTHEA_04228.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            AMALTHEA_04228.write(':TRIGger:COUNt %G' % (1.0))
            AMALTHEA_04228.write(':SAMPle:COUNt %d' % (16384))
            time.sleep(0.128)
            print("Amalthea is Configured")

            # Configure DMM for Voltage oF Jupiter Safing with Adrastea
            ADRASTEA_04250.write(':TRIGger:SOURce %s' % ('IMMediate'))
            ADRASTEA_04250.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            ADRASTEA_04250.write(':TRIGger:COUNt %G' % (1.0))
            ADRASTEA_04250.write(':SAMPle:COUNt %d' % (16384))
            time.sleep(0.128)
            print("Amalthea is Configured")

        def startTimerArming():
            startTimerArming.start = time.time()
            startTimerArming.startTime = datetime.datetime.now().time()
            startTimerArming.startMS = datetime.datetime.now().strftime('%S.%f')
            print("Arming Timer is started at {}".format(startTimerArming.start))
        def startTimerSafing():
            startTimerSafing.start = time.time()
            startTimerSafing.startTime = datetime.datetime.now().time()
            startTimerSafing.startMS = datetime.datetime.now().strftime('%S.%f')
            print("Safing Timer is started at {}".format(startTimerSafing.start))
        def getDmmVoltageData():
            print("Initiate all DMMs...")
            METIS_06676.write(':INITiate:IMMediate')
            CALLISTO_01437.write(':INITiate:IMMediate')
            GANYMEDE_03625.write(':INITiate:IMMediate')
            THEBE_00599.write(':INITiate:IMMediate')
            IO_06446.write(':INITiate:IMMediate')
            EUROPA_00866.write(':INITiate:IMMediate')
            AMALTHEA_04228.write(':INITiate:IMMediate')
            ADRASTEA_04250.write(':INITiate:IMMediate')
            print("...DMMs are all Intitiated.")
        def armingCyclePower():
            print("Turning Jupiter-Arming Output to 'ON'... ")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (1))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            print("...Jupiter-Arming is now ON")
        def safingCyclePower():
            print("Turning Jupiter-Safing Output to 'ON'... ")
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (1))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            print("...Jupiter-Safing is now ON")
        def collectArmingDMM():
            collectArmingDMM.arming_current_values = METIS_06676.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_current_readings = collectArmingDMM.arming_current_values[0]
            collectArmingDMM.arming_safeMon2_values = GANYMEDE_03625.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_safeMon2_readings = collectArmingDMM.arming_safeMon2_values[0]
            collectArmingDMM.arming_armMon2_values = THEBE_00599.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_armMon2_readings = collectArmingDMM.arming_armMon2_values[0]
            collectArmingDMM.arming_safeMon1_values = IO_06446.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_safeMon1_readings = collectArmingDMM.arming_safeMon1_values[0]
            collectArmingDMM.arming_armMon1_values = EUROPA_00866.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_armMon1_readings = collectArmingDMM.arming_armMon1_values[0]
        def collectSafingDMM():
            collectSafingDMM.safing_current_values = CALLISTO_01437.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_current_readings = collectSafingDMM.safing_current_values[0]
            collectSafingDMM.safing_safeMon2_values = GANYMEDE_03625.query_ascii_values(':FETCh?')
            collectSafingDMM.asafing_safeMon2_readings = collectSafingDMM.safing_safeMon2_values[0]
            collectSafingDMM.safing_armMon2_values = THEBE_00599.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_armMon2_readings = collectSafingDMM.safing_armMon2_values[0]
            collectSafingDMM.safing_safeMon1_values = IO_06446.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_safeMon1_readings = collectSafingDMM.safing_safeMon1_values[0]
            collectSafingDMM.safing_armMon1_values = EUROPA_00866.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_armMon1_readings = collectSafingDMM.safing_armMon1_values[0]
        def stopTimerArming():
            stopTimerArming.end = time.time()
            stopTimerArming.endTime = datetime.datetime.now().time()
            stopTimerArming.endMS = datetime.datetime.now().strftime('%S.%f')
            print("Arming Timer stopped at {} ".format(stopTimerArming.end))
            time.sleep(0.128)
        def stopTimerSafing():
            stopTimerSafing.end = time.time()
            stopTimerSafing.endTime = datetime.datetime.now().time()
            stopTimerSafing.endMS = datetime.datetime.now().strftime('%S.%f')
            print("Safing Timer stopped at {} ".format(stopTimerSafing.end))
            time.sleep(0.128)
        def configureArmedResistanceMeasure():
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            time.sleep(0.128)
        def configureSafedResistanceMeasure():
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            time.sleep(0.128)
        def getResArm():
            getResArm.temp_valuesR = GANYMEDE_03625.query_ascii_values(':MEASure:RESistance?')
            getResArm.aResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = THEBE_00599.query_ascii_values(':MEASure:RESistance?')
            getResArm.bResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = IO_06446.query_ascii_values(':MEASure:RESistance?')
            getResArm.cResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = EUROPA_00866.query_ascii_values(':MEASure:RESistance?')
            getResArm.dResistance = getResArm.temp_valuesR[0]
        def getResSafe():
            getResSafe.temp_valuesR = GANYMEDE_03625.query_ascii_values(':MEASure:RESistance?')
            getResSafe.aResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = THEBE_00599.query_ascii_values(':MEASure:RESistance?')
            getResSafe.bResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = IO_06446.query_ascii_values(':MEASure:RESistance?')
            getResSafe.cResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = EUROPA_00866.query_ascii_values(':MEASure:RESistance?')
            getResSafe.dResistance = getResSafe.temp_valuesR[0]
        def getArmingDB():
            testID = str(getUserInitialData.serialNumber + "-" + testDate.strftime('%b-%d-%H-%M-%S'))
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.arming_current_values))

            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()

            cur.execute('DROP TABLE IF EXISTS ArmingCurrentTable')
            cur.execute('DROP TABLE IF EXISTS ArmingSafeMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS ArmingArmMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS ArmingSafeMonOneTable')
            cur.execute('DROP TABLE IF EXISTS ArmingArmMonOneTable')
            cur.execute('CREATE TABLE ArmingCurrentTable (testID TEXT, timeID FLOAT, currentLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingSafeMonTwoTable (testID TEXT, timeID FLOAT, safeMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingArmMonTwoTable (testID TEXT, timeID FLOAT, armMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingSafeMonOneTable (testID TEXT, timeID FLOAT, safeMon1VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingArmMonOneTable (testID TEXT, timeID FLOAT, armMon1VoltLevel FLOAT)')

            stepCurrent = collectArmingDMM.arming_current_values
            arm = dict(zip(time, stepCurrent))
            for key in arm:
                cur.execute('INSERT INTO ArmingCurrentTable (testID,timeID,currentLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key)), ('{}'.format(arm[key]))))

            stepSafeMon2 = collectArmingDMM.arming_safeMon2_values
            arm2 = dict(zip(time, stepSafeMon2))
            for key2 in arm2:
                cur.execute('INSERT INTO ArmingSafeMonTwoTable (testID,timeID,safeMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key2)), ('{}'.format(arm2[key2]))))

            stepArmMon2 = collectArmingDMM.arming_armMon2_values
            arm3 = dict(zip(time, stepArmMon2))
            for key3 in arm3:
                cur.execute('INSERT INTO ArmingArmMonTwoTable (testID,timeID,armMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key3)), ('{}'.format(arm3[key3]))))

            stepSafeMon1 = collectArmingDMM.arming_safeMon1_values
            arm4 = dict(zip(time, stepSafeMon1))
            for key4 in arm4:
                cur.execute('INSERT INTO ArmingSafeMonOneTable (testID,timeID,safeMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key4)), ('{}'.format(arm4[key4]))))

            stepArmMon1 = collectArmingDMM.arming_armMon1_values
            arm5 = dict(zip(time, stepArmMon1))
            for key5 in arm5:
                cur.execute('INSERT INTO ArmingArmMonOneTable (testID,timeID,armMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key5)), ('{}'.format(arm5[key5]))))
            conn.commit()
            conn.close()
        def getSafingDB():
            testID = str(getUserInitialData.serialNumber + "-" + testDate.strftime('%b-%d-%H-%M-%S'))
            time = np.linspace(float(startTimerSafing.start), float(stopTimerSafing.end), len(collectSafingDMM.safing_current_values))

            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()

            cur.execute('DROP TABLE IF EXISTS SafingCurrentTable')
            cur.execute('DROP TABLE IF EXISTS SafingSafeMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS SafingArmMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS SafingSafeMonOneTable')
            cur.execute('DROP TABLE IF EXISTS SafingArmMonOneTable')
            cur.execute('CREATE TABLE SafingCurrentTable (testID TEXT, timeID FLOAT, currentLevel FLOAT)')
            cur.execute('CREATE TABLE SafingSafeMonTwoTable (testID TEXT, timeID FLOAT, safeMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingArmMonTwoTable (testID TEXT, timeID FLOAT, armMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingSafeMonOneTable (testID TEXT, timeID FLOAT, safeMon1VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingArmMonOneTable (testID TEXT, timeID FLOAT, armMon1VoltLevel FLOAT)')

            stepCurrentS = collectSafingDMM.safing_current_values
            arm = dict(zip(time, stepCurrentS))
            for key in arm:
                cur.execute('INSERT INTO SafingCurrentTable (testID,timeID,currentLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key)), ('{}'.format(arm[key]))))

            stepSafeMon2S = collectSafingDMM.safing_safeMon2_values
            arm2 = dict(zip(time, stepSafeMon2S))
            for key2 in arm2:
                cur.execute('INSERT INTO SafingSafeMonTwoTable (testID,timeID,safeMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key2)), ('{}'.format(arm2[key2]))))

            stepArmMon2S = collectSafingDMM.safing_armMon2_values
            arm3 = dict(zip(time, stepArmMon2S))
            for key3 in arm3:
                cur.execute('INSERT INTO SafingArmMonTwoTable (testID,timeID,armMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key3)), ('{}'.format(arm3[key3]))))

            stepSafeMon1S = collectSafingDMM.safing_safeMon1_values
            arm4 = dict(zip(time, stepSafeMon1S))
            for key4 in arm4:
                cur.execute('INSERT INTO SafingSafeMonOneTable (testID,timeID,safeMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key4)), ('{}'.format(arm4[key4]))))

            stepArmMon1S = collectSafingDMM.safing_armMon1_values
            arm5 = dict(zip(time, stepArmMon1S))
            for key5 in arm5:
                cur.execute('INSERT INTO SafingArmMonOneTable (testID,timeID,armMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key5)), ('{}'.format(arm5[key5]))))
            conn.commit()
            conn.close()
        def armPlot():
            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM interrupterArmingQry')
            armingSummary = cur.fetchall()

            fileData = open('SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M") + '.csv', 'w')
            fileData.write("testID,timeID,currentLevel,armMon1VoltLevel,safeMon1VoltLevel,armMon2VoltLevel,safeMon2VoltLevel\n")
            for row in armingSummary:
                fileData.write(str(row).replace('(','').replace(')','') + '\n')
            fileData.close()

            timeArmingIndex = []
            armingCurrentLevel = []
            armingArmMon1Level = []
            armingSafeMon1Level = []
            armingArmMon2Level = []
            armingSafeMon2Level = []

            for inner in armingSummary:
                timeArmingIndex.append(inner[1])
                armingCurrentLevel.append(inner[2])
                armingArmMon1Level.append(inner[3])
                armingSafeMon1Level.append(inner[4])
                armingArmMon2Level.append(inner[5])
                armingSafeMon2Level.append(inner[6])
            plt.figure(1)
            plt.plot(timeArmingIndex, armingCurrentLevel, label="Current (Amperes)")
            plt.plot(timeArmingIndex, armingArmMon1Level, label = "Arm Monitor #1 (Volts)")
            plt.plot(timeArmingIndex, armingSafeMon1Level, label = "Safe Monitor #1 (Volts)")
            plt.plot(timeArmingIndex, armingArmMon2Level, label = "Arm Monitor #2 (Volts)")
            plt.plot(timeArmingIndex, armingSafeMon2Level, label = "Safe Monitor #2 (Volts)")
            plt.xlabel('Time-stamp (s)')
            plt.ylabel('Measurement Level (Volts/Amperes)')
            plt.title('Arming Cycle Performance')
            plt.legend(loc='upper right', bbox_to_anchor=(1.00, 0.94), fontsize='x-small')
            plt.savefig('C:/repos/ortint/img/Limited_Arming_Cycle')
            #plt.show()

            conn.commit()
            conn.close()
        def safePlot():
            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM interrupterSafingQry')
            safingSummary = cur.fetchall()

            fileData = open('SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M") + '.csv', 'w')
            fileData.write("testID,timeID,currentLevel,armMon1VoltLevel,safeMon1VoltLevel,armMon2VoltLevel,safeMon2VoltLevel\n")
            for row in safingSummary:
                fileData.write(str(row).replace('(','').replace(')','') + '\n')
            fileData.close()

            timeSafingIndex = []
            safingCurrentLevel = []
            safingArmMon1Level = []
            safingSafeMon1Level = []
            safingArmMon2Level = []
            safingSafeMon2Level = []

            for inner in safingSummary:
                timeSafingIndex.append(inner[1])
                safingCurrentLevel.append(inner[2])
                safingArmMon1Level.append(inner[3])
                safingSafeMon1Level.append(inner[4])
                safingArmMon2Level.append(inner[5])
                safingSafeMon2Level.append(inner[6])
            plt.figure(2)
            plt.plot(timeSafingIndex, safingCurrentLevel, label="Current (Amperes)")
            plt.plot(timeSafingIndex, safingArmMon1Level, label = "Arm Monitor #1 (Volts)")
            plt.plot(timeSafingIndex, safingSafeMon1Level, label = "Safe Monitor #1 (Volts)")
            plt.plot(timeSafingIndex, safingArmMon2Level, label = "Arm Monitor #2 (Volts)")
            plt.plot(timeSafingIndex, safingSafeMon2Level, label = "Safe Monitor #2 (Volts)")
            plt.xlabel('Time-stamp (s)')
            plt.ylabel('Measurement Level (Volts/Amperes)')
            plt.title('Safing Cycle Performance')
            plt.legend(loc='upper right', bbox_to_anchor=(1.00, 0.93), fontsize='x-small')
            plt.savefig('C:/repos/ortint/img/Limited_Safing_Cycle')
            #plt.show()

            conn.commit()
            conn.close()

        def calcArmStats():
            calcArmStats.maxCurrent = max(collectArmingDMM.arming_current_values)

            # Make a dictionary from two lists
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.arming_current_values))
            voltStep = collectArmingDMM.arming_armMon2_values
            arm = dict(zip(time, voltStep))
            # The first time stamp
            startArmCycleTimeIdx = next(iter(arm))

            # After the first eight consecutive high voltages, print the last one as endCycleTime
            timeIdxArm = 8
            for key in arm:
                if arm[key] > 4 and timeIdxArm > 0:
                    armCycleEndTime = key
                    timeIdxArm = timeIdxArm -1
            endArmCycleTimeIdx = armCycleEndTime
            # Calculate Cycle Time
            calcArmStats.cycleTimeArm = endArmCycleTimeIdx - startArmCycleTimeIdx
        def saveArmData():
            # Make a dictionary from two lists
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.temp_values3))

            fileData = open(str('current-arming-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            current = collectArmingDMM.temp_values
            arm = dict(zip(time, current))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-safe-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS2 = collectArmingDMM.temp_values2
            arm = dict(zip(time, voltStepS2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-arm-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA2 = collectArmingDMM.temp_values3
            arm = dict(zip(time, voltStepA2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-safe-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS1 = collectArmingDMM.temp_values4
            arm = dict(zip(time, voltStepS1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-arm-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA1 = collectArmingDMM.temp_values5
            arm = dict(zip(time, voltStepA1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()
        def saveSafeData():
            # Make a dictionary from two lists
            time = np.linspace(float(startTimerSafing.startMS), float(stopTimerSafing.endMS), len(collectSafingDMM.temp_values4_S))

            fileData = open(str('current-safing-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            current = collectSafingDMM.temp_values_S
            arm = dict(zip(time, current))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-safe-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS2 = collectSafingDMM.temp_values2_S
            arm = dict(zip(time, voltStepS2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-arm-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA2 = collectSafingDMM.temp_values3_S
            arm = dict(zip(time, voltStepA2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-safe-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS1 = collectSafingDMM.temp_values4_S
            arm = dict(zip(time, voltStepS1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safing-arm-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA1 = collectSafingDMM.temp_values5_S
            arm = dict(zip(time, voltStepA1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()
        def calcSafeStats():
            calcSafeStats.maxCurrent = max(collectSafingDMM.safing_current_values)

            # Make a dictionary from two lists
            time = np.linspace(float(startTimerSafing.start), float(stopTimerSafing.end), len(collectSafingDMM.safing_safeMon1_values))
            voltStepSafe = collectSafingDMM.safing_safeMon1_values
            safe = dict(zip(time, voltStepSafe))
            # The first time stamp
            startSafeCycleTimeIdx = next(iter(safe))

            # After the first eight consecutive high voltages, print the last one as endCycleTime
            timeIdx = 8
            for key in safe:
                if safe[key] > 4 and timeIdx > 0:
                    safeCycleEndTime = key
                    timeIdx = timeIdx -1
            endSafeCycleTimeIdx = safeCycleEndTime
            # Calculate Cycle Time
            calcSafeStats.cycleTimeSafe = endSafeCycleTimeIdx - startSafeCycleTimeIdx
        def closePowerSupplies():
            print("Turning off Jupiter-Arming and Jupiter-Safing Power Supplies...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.close()
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_SAFING_E3634A.write('*CLS')
            JUPITER_SAFING_E3634A.write('*RST')
            JUPITER_SAFING_E3634A.close()
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write('*CLS')
            JUPITER_GALILEO_E3634A.write('*RST')
            JUPITER_GALILEO_E3634A.close()
            print("...Jupiter-Arming and Jupiter-Safing are new off and reset.")
        def closeDMM():
            METIS_06676.close()
            CALLISTO_01437.close()
            GANYMEDE_03625.close()
            IO_06446.close()
            EUROPA_00866.close()
            rm.close()
            print("DMMs are now Closed")

        def printToScreen():
            print("Step (a): The maximum Current reached during the Arming cycle was {} Amperes".format(
                calcArmStats.maxCurrent))
            print("Step (a): Total Arming Time = {} seconds".format(calcArmStats.cycleTimeArm))
            print("Step (b): Safe Monitor2 Resistance after Arming is = {} Ohms".format(getResArm.aResistance))
            print("Step (b): Arm Monitor2 Resistance after Arming is = {} Ohms".format(getResArm.bResistance))
            print("Step (b): Safe Monitor1 Resistance after Arming is = {} Ohms".format(getResArm.cResistance))
            print("Step (b): Arm Monitor1 Resistance after Arming is = {} Ohms".format(getResArm.dResistance))

            print("Step (c): The maximum Current reached during the Safing cycle was {} Amperes".format(
                calcSafeStats.maxCurrent))
            print("Step (c): Total Safing Time = {} seconds".format(calcSafeStats.cycleTimeSafe))
            print("Step (d): Safe Monitor2 Resistance after Arming is = {} Ohms".format(getResSafe.aResistance))
            print("Step (d): Arm Monitor2 Resistance after Arming is = {} Ohms".format(getResSafe.bResistance))
            print("Step (d): Safe Monitor1 Resistance after Arming is = {} Ohms".format(getResSafe.cResistance))
            print("Step (d): Arm Monitor1 Resistance after Arming is = {} Ohms".format(getResSafe.dResistance))
        def writeFullReport():
            f = open('Full-Test-Results.html', 'w')

            f.write("""<html lang="en">""")
            f.write("""<head>""")
            f.write("""  <meta charset="utf-8">""")
            f.write("""    <title>ULA Ordnance Interrupter Bench Test Report</title>""")
            f.write("""  <meta name="description" content="Systima Ordnance Interrupter Test Bench">""")
            f.write("""  <meta name="author" content="SitePoint">""")
            f.write("""  <link rel="stylesheet" href="simple.css" type="text/css"/>""")
            f.write("</head>")
            f.write("<!doctype html>")
            f.write("<body>")

            f.write("""<h1>Ordnance Interrupter Test Report</h1>""")
            f.write("""<h2>Test Type:""" + interrupterApp.testType + """ </h2>""")
            f.write("""<h4>ULA Specification:  """ + numSpecULA + """</h4>""")
            f.write("""<h4>Test Date:  """ + testDate.strftime("%Y-%m-%d %H:%M") + """</h4>""")
            f.write("""<h4>Part Number:  """ + partNumber + """</h4>""")
            f.write("""<h4>Serial Number:  """ + getUserInitialData.serialNumber + """</h4>""")
            f.write("""<h4>Name of Systima Test Engineer:  """ + getUserInitialData.operatorsName + """</h4>""")

            f.write("""<h2>RAW RESULTS</h2>""")


            f.write("""<b>Step (f):</b> The Maximum Observed Cycle Time over 25 cycles was """ + str(maxObservedArmCycleTime) + """ seconds.<br>""")

            f.write("""  <script src="js/scripts.js"></script>""")
            f.write("</body>")
            f.write("</html>")

            f.close()

        getUserInitialData()
        simpleSafingCycle()
        configurePowerSupplyJupiterArming()
        configurePowerSupplyJupiterSafing()
        configurePowerSupplyGalileo()
        startLoopTime = time.time()
        fullTest.n = 25
        fullTest.nStart = fullTest.n
        maxObservedArmCurrent = 0
        maxObservedArmCycleTime = 0
        # HTML Prelude
        f = open('SN-'+ getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime("%Y-%m-%d-%H-%M") +'.html', 'w')
        f.write("""<html lang="en">""")
        f.write("""<head>""")
        f.write("""  <meta charset="utf-8">""")
        f.write("""    <title>ULA Ordnance Interrupter Bench Test Report</title>""")
        f.write("""  <meta name="description" content="Systima Ordnance Interrupter Test Bench">""")
        f.write("""  <meta name="author" content="SitePoint">""")
        f.write("""  <link rel="stylesheet" href="simple.css" type="text/css"/>""")
        f.write("</head>")
        f.write("<!doctype html>")
        f.write("<body>")
        f.write("""<h1>Ordnance Interrupter Test Report</h1>""")
        f.write("""<h2>Test Type:""" + interrupterApp.testType + """ </h2>""")
        f.write("""<h4>ULA Specification:  """ + numSpecULA + """</h4>""")
        f.write("""<h4>Test Date:  """ + testDate.strftime("%Y-%m-%d %H:%M") + """</h4>""")
        f.write("""<h4>Part Number:  """ + partNumber + """</h4>""")
        f.write("""<h4>Serial Number:  """ + getUserInitialData.serialNumber + """</h4>""")
        f.write("""<h4>Name of Systima Test Engineer:  """ + getUserInitialData.operatorsName + """</h4>""")
        f.write("""<h2>RAW RESULTS</h2>""")

        while fullTest.n > 0:
            setupDMM()
            startTimerArming()
            armingCyclePower()
            getDmmVoltageData()
            collectArmingDMM()
            stopTimerArming()
            configureArmedResistanceMeasure()
            getResArm()
            #getArmingDB()
            # armPlot()
            calcArmStats()
            setupDMM()
            startTimerSafing()
            safingCyclePower()
            getDmmVoltageData()
            collectSafingDMM()
            stopTimerSafing()
            configureSafedResistanceMeasure()
            #getResSafe()
            #getSafingDB()
            calcSafeStats()


            fullTest.n = fullTest.n - 1

            thisCyclesArmCurrent = calcArmStats.maxCurrent
            if thisCyclesArmCurrent > maxObservedArmCurrent:
                maxObservedArmCurrent = thisCyclesArmCurrent
            else:
                maxObservedArmCurrent = maxObservedArmCurrent
            print("This cycle's maximum current = " + str(thisCyclesArmCurrent) + ", Max Current = " + str(maxObservedArmCurrent))
            print("Max Arming Time = " + str(calcArmStats.cycleTimeArm))
            print("loops to go = " + str(fullTest.n))

            thisCyclesCycleTime = calcArmStats.cycleTimeArm
            if thisCyclesCycleTime > maxObservedArmCycleTime:
                maxObservedArmCycleTime = thisCyclesCycleTime
            else:
                maxObservedArmCycleTime = maxObservedArmCycleTime
            f.write("""<b> Cycle Number #</b>""" + "{}".format(fullTest.nStart - fullTest.n) + """: cycle-time = """ + str(thisCyclesCycleTime) + """ seconds, Max Cycle Time During Arming = """ + str(maxObservedArmCycleTime) + """seconds<br>""")
            f.write('\n')
            print("This cycle's maximum cycle time = " + str(thisCyclesCycleTime) + ", Max Cycle Time  = " + str(maxObservedArmCycleTime))
            print("Max Arming Time = " + str(calcArmStats.cycleTimeArm))
            endLoopTime = time.time()
            loopTime = (endLoopTime - startLoopTime) / 60

        # HTML Close
        f.write("""  <script src="js/scripts.js"></script>""")
        f.write("</body>")
        f.write("</html>")
        f.close()
        print("Done with Loop...Thanks for waiting for : {} minutes.".format(loopTime))

        #writeFullReport()
        closePowerSupplies()
        closeDMM()

    def limitedTest(psVoltageLevel):
        def getUserInitialData():
            getUserInitialData.operatorsName = input("What is your name (First, Last)?     ")
            getUserInitialData.serialNumber = input("What is the serial number stamped into the base of this Ordnance Interrupter?    ")
        def visualArmCheck():
            visualArmCheck.armedCondition = input("Can you see the Armed Indicator?:\n (Please respond with:\n 1. Armed\n 2. Safed\n\n")

            if visualArmCheck.armedCondition == 1 or 2:
               visualArmCheck.armedCondition = visualArmCheck.armedCondition
               print("Thank you. Now continuing test.....")
            else:
              print("Please respond with '1' or '2'")
        def visualSafeCheck():
            visualSafeCheck.safedCondition = input("Can you see the Safed Indicator?:\n (Please respond with:\n 1. Armed\n 2. Safed\n\n")

            if visualSafeCheck.safedCondition == 1 or 2:
               visualSafeCheck.safedCondition = visualSafeCheck.safedCondition
               print("Thank you. Now continuing test.....")
            else:
              print("Please respond with '1' or '2'")
        def simpleSafingCycle():
            print("Safing the Device...")
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_SAFING_E3634A.write('*CLS')
            JUPITER_SAFING_E3634A.write('*RST')
            JUPITER_SAFING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_SAFING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % ('MAXimum'))
            JUPITER_SAFING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (1))
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (1))
            time.sleep(0.256)
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            print("...finished safing the device")
        def configurePowerSupplyJupiterArming():
            print("Setting up Jupiter Arming...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            print("Jupiter-Arming Power Supply is now Configured")
        def configurePowerSupplyJupiterSafing():
            print("Setting up Jupiter Safing...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            print("Jupiter-Safing Power Supply is now Configured")
        def configurePowerSupplyGalileo():
            print("Setting up Galileo...")
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write('*CLS')
            JUPITER_GALILEO_E3634A.write('*RST')
            JUPITER_GALILEO_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (5.0))
            JUPITER_GALILEO_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_GALILEO_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            #JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            time.sleep(0.512)
            print("Galileo Power Supply is now Configured and Output is On")
        def setupDMM():
            METIS_06676.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_DC_CURRENT.sta'))
            METIS_06676.write(':TRIGger:SOURce %s' % ('IMMediate'))
            METIS_06676.write(':TRIGger:COUNt %G' % (1.0))
            METIS_06676.write(':SENSe:CURRent:DC:RANGe %G' % (0.01))
            METIS_06676.write(':SENSe:CURRent:DC:TERMinals %d' % (10))
            METIS_06676.write(':SAMPle:COUNt %d' % (16384))
            print("Metis is Configured")

            CALLISTO_01437.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_DC_CURRENT.sta'))
            CALLISTO_01437.write(':TRIGger:SOURce %s' % ('IMMediate'))
            CALLISTO_01437.write(':TRIGger:COUNt %G' % (1.0))
            CALLISTO_01437.write(':SENSe:CURRent:DC:RANGe %G' % (0.01))
            CALLISTO_01437.write(':SENSe:CURRent:DC:TERMinals %d' % (10))
            CALLISTO_01437.write(':SAMPle:COUNt %d' % (16384))
            print("Callisto is Configured")

            # Load DMM Voltage Configuration State Files
            GANYMEDE_03625.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            THEBE_00599.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            IO_06446.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            EUROPA_00866.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))

            # Configure DMM for Voltage or Resistance on Safe Monitor #2
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            GANYMEDE_03625.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            GANYMEDE_03625.write(':TRIGger:COUNt %G' % (1.0))
            GANYMEDE_03625.write(':SAMPle:COUNt %d' % (16384))
            print("Ganymede is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            THEBE_00599.write(':TRIGger:COUNt %G' % (1.0))
            THEBE_00599.write(':SAMPle:COUNt %d' % (16384))
            print("Thebe is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            IO_06446.write(':TRIGger:COUNt %G' % (1.0))
            IO_06446.write(':SAMPle:COUNt %d' % (16384))
            print("Io is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            EUROPA_00866.write(':TRIGger:COUNt %G' % (1.0))
            EUROPA_00866.write(':SAMPle:COUNt %d' % (16384))
            time.sleep(0.128)
            print("Europa is Configured")
        def startTimerArming():
            startTimerArming.start = time.time()
            startTimerArming.startTime = datetime.datetime.now().time()
            startTimerArming.startMS = datetime.datetime.now().strftime('%S.%f')
            print("Arming Timer is started at {}".format(startTimerArming.start))
        def startTimerSafing():
            startTimerSafing.start = time.time()
            startTimerSafing.startTime = datetime.datetime.now().time()
            startTimerSafing.startMS = datetime.datetime.now().strftime('%S.%f')
            print("Safing Timer is started at {}".format(startTimerSafing.start))
        def getDmmVoltageData():
            print("Initiate all DMMs...")
            METIS_06676.write(':INITiate:IMMediate')
            CALLISTO_01437.write(':INITiate:IMMediate')
            GANYMEDE_03625.write(':INITiate:IMMediate')
            THEBE_00599.write(':INITiate:IMMediate')
            IO_06446.write(':INITiate:IMMediate')
            EUROPA_00866.write(':INITiate:IMMediate')
            print("...DMMs are all Intitiated.")
        def armingCyclePower():
            print("Turning Jupiter-Arming Output to 'ON'... ")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (1))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            print("...Jupiter-Arming is now ON")
        def safingCyclePower():
            print("Turning Jupiter-Safing Output to 'ON'... ")
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (1))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            print("...Jupiter-Safing is now ON")
        def collectArmingDMM():
            collectArmingDMM.arming_current_values = METIS_06676.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_current_readings = collectArmingDMM.arming_current_values[0]
            collectArmingDMM.arming_safeMon2_values = GANYMEDE_03625.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_safeMon2_readings = collectArmingDMM.arming_safeMon2_values[0]
            collectArmingDMM.arming_armMon2_values = THEBE_00599.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_armMon2_readings = collectArmingDMM.arming_armMon2_values[0]
            collectArmingDMM.arming_safeMon1_values = IO_06446.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_safeMon1_readings = collectArmingDMM.arming_safeMon1_values[0]
            collectArmingDMM.arming_armMon1_values = EUROPA_00866.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_armMon1_readings = collectArmingDMM.arming_armMon1_values[0]
        def collectSafingDMM():
            collectSafingDMM.safing_current_values = CALLISTO_01437.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_current_readings = collectSafingDMM.safing_current_values[0]
            collectSafingDMM.safing_safeMon2_values = GANYMEDE_03625.query_ascii_values(':FETCh?')
            collectSafingDMM.asafing_safeMon2_readings = collectSafingDMM.safing_safeMon2_values[0]
            collectSafingDMM.safing_armMon2_values = THEBE_00599.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_armMon2_readings = collectSafingDMM.safing_armMon2_values[0]
            collectSafingDMM.safing_safeMon1_values = IO_06446.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_safeMon1_readings = collectSafingDMM.safing_safeMon1_values[0]
            collectSafingDMM.safing_armMon1_values = EUROPA_00866.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_armMon1_readings = collectSafingDMM.safing_armMon1_values[0]
        def stopTimerArming():
            stopTimerArming.end = time.time()
            stopTimerArming.endTime = datetime.datetime.now().time()
            stopTimerArming.endMS = datetime.datetime.now().strftime('%S.%f')
            print("Arming Timer stopped at {} ".format(stopTimerArming.end))
            time.sleep(0.128)
        def stopTimerSafing():
            stopTimerSafing.end = time.time()
            stopTimerSafing.endTime = datetime.datetime.now().time()
            stopTimerSafing.endMS = datetime.datetime.now().strftime('%S.%f')
            print("Safing Timer stopped at {} ".format(stopTimerSafing.end))
            time.sleep(0.128)
        def configureArmedResistanceMeasure():
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            time.sleep(0.128)
        def configureSafedResistanceMeasure():
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            time.sleep(0.128)
        def getResArm():
            getResArm.temp_valuesR = GANYMEDE_03625.query_ascii_values(':MEASure:RESistance?')
            getResArm.aResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = THEBE_00599.query_ascii_values(':MEASure:RESistance?')
            getResArm.bResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = IO_06446.query_ascii_values(':MEASure:RESistance?')
            getResArm.cResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = EUROPA_00866.query_ascii_values(':MEASure:RESistance?')
            getResArm.dResistance = getResArm.temp_valuesR[0]
        def getResSafe():
            getResSafe.temp_valuesR = GANYMEDE_03625.query_ascii_values(':MEASure:RESistance?')
            getResSafe.aResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = THEBE_00599.query_ascii_values(':MEASure:RESistance?')
            getResSafe.bResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = IO_06446.query_ascii_values(':MEASure:RESistance?')
            getResSafe.cResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = EUROPA_00866.query_ascii_values(':MEASure:RESistance?')
            getResSafe.dResistance = getResSafe.temp_valuesR[0]
        def getArmingDB():
            testID = str(getUserInitialData.serialNumber + "-" + testDate.strftime('%b-%d-%H-%M-%S'))
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.arming_current_values))

            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()

            cur.execute('DROP TABLE IF EXISTS ArmingCurrentTable')
            cur.execute('DROP TABLE IF EXISTS ArmingSafeMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS ArmingArmMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS ArmingSafeMonOneTable')
            cur.execute('DROP TABLE IF EXISTS ArmingArmMonOneTable')
            cur.execute('CREATE TABLE ArmingCurrentTable (testID TEXT, timeID FLOAT, currentLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingSafeMonTwoTable (testID TEXT, timeID FLOAT, safeMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingArmMonTwoTable (testID TEXT, timeID FLOAT, armMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingSafeMonOneTable (testID TEXT, timeID FLOAT, safeMon1VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingArmMonOneTable (testID TEXT, timeID FLOAT, armMon1VoltLevel FLOAT)')

            stepCurrent = collectArmingDMM.arming_current_values
            arm = dict(zip(time, stepCurrent))
            for key in arm:
                cur.execute('INSERT INTO ArmingCurrentTable (testID,timeID,currentLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key)), ('{}'.format(arm[key]))))

            stepSafeMon2 = collectArmingDMM.arming_safeMon2_values
            arm2 = dict(zip(time, stepSafeMon2))
            for key2 in arm2:
                cur.execute('INSERT INTO ArmingSafeMonTwoTable (testID,timeID,safeMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key2)), ('{}'.format(arm2[key2]))))

            stepArmMon2 = collectArmingDMM.arming_armMon2_values
            arm3 = dict(zip(time, stepArmMon2))
            for key3 in arm3:
                cur.execute('INSERT INTO ArmingArmMonTwoTable (testID,timeID,armMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key3)), ('{}'.format(arm3[key3]))))

            stepSafeMon1 = collectArmingDMM.arming_safeMon1_values
            arm4 = dict(zip(time, stepSafeMon1))
            for key4 in arm4:
                cur.execute('INSERT INTO ArmingSafeMonOneTable (testID,timeID,safeMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key4)), ('{}'.format(arm4[key4]))))

            stepArmMon1 = collectArmingDMM.arming_armMon1_values
            arm5 = dict(zip(time, stepArmMon1))
            for key5 in arm5:
                cur.execute('INSERT INTO ArmingArmMonOneTable (testID,timeID,armMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key5)), ('{}'.format(arm5[key5]))))
            conn.commit()
            conn.close()
        def getSafingDB():
            testID = str(getUserInitialData.serialNumber + "-" + testDate.strftime('%b-%d-%H-%M-%S'))
            time = np.linspace(float(startTimerSafing.start), float(stopTimerSafing.end), len(collectSafingDMM.safing_current_values))

            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()

            cur.execute('DROP TABLE IF EXISTS SafingCurrentTable')
            cur.execute('DROP TABLE IF EXISTS SafingSafeMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS SafingArmMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS SafingSafeMonOneTable')
            cur.execute('DROP TABLE IF EXISTS SafingArmMonOneTable')
            cur.execute('CREATE TABLE SafingCurrentTable (testID TEXT, timeID FLOAT, currentLevel FLOAT)')
            cur.execute('CREATE TABLE SafingSafeMonTwoTable (testID TEXT, timeID FLOAT, safeMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingArmMonTwoTable (testID TEXT, timeID FLOAT, armMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingSafeMonOneTable (testID TEXT, timeID FLOAT, safeMon1VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingArmMonOneTable (testID TEXT, timeID FLOAT, armMon1VoltLevel FLOAT)')

            stepCurrentS = collectSafingDMM.safing_current_values
            arm = dict(zip(time, stepCurrentS))
            for key in arm:
                cur.execute('INSERT INTO SafingCurrentTable (testID,timeID,currentLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key)), ('{}'.format(arm[key]))))

            stepSafeMon2S = collectSafingDMM.safing_safeMon2_values
            arm2 = dict(zip(time, stepSafeMon2S))
            for key2 in arm2:
                cur.execute('INSERT INTO SafingSafeMonTwoTable (testID,timeID,safeMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key2)), ('{}'.format(arm2[key2]))))

            stepArmMon2S = collectSafingDMM.safing_armMon2_values
            arm3 = dict(zip(time, stepArmMon2S))
            for key3 in arm3:
                cur.execute('INSERT INTO SafingArmMonTwoTable (testID,timeID,armMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key3)), ('{}'.format(arm3[key3]))))

            stepSafeMon1S = collectSafingDMM.safing_safeMon1_values
            arm4 = dict(zip(time, stepSafeMon1S))
            for key4 in arm4:
                cur.execute('INSERT INTO SafingSafeMonOneTable (testID,timeID,safeMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key4)), ('{}'.format(arm4[key4]))))

            stepArmMon1S = collectSafingDMM.safing_armMon1_values
            arm5 = dict(zip(time, stepArmMon1S))
            for key5 in arm5:
                cur.execute('INSERT INTO SafingArmMonOneTable (testID,timeID,armMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key5)), ('{}'.format(arm5[key5]))))
            conn.commit()
            conn.close()
        def armPlot():
            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM interrupterArmingQry')
            armingSummary = cur.fetchall()

            fileData = open('SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M") + '.csv', 'w')
            fileData.write("testID,timeID,currentLevel,armMon1VoltLevel,safeMon1VoltLevel,armMon2VoltLevel,safeMon2VoltLevel\n")
            for row in armingSummary:
                fileData.write(str(row).replace('(','').replace(')','') + '\n')
            fileData.close()

            timeArmingIndex = []
            armingCurrentLevel = []
            armingArmMon1Level = []
            armingSafeMon1Level = []
            armingArmMon2Level = []
            armingSafeMon2Level = []

            for inner in armingSummary:
                timeArmingIndex.append(inner[1])
                armingCurrentLevel.append(inner[2])
                armingArmMon1Level.append(inner[3])
                armingSafeMon1Level.append(inner[4])
                armingArmMon2Level.append(inner[5])
                armingSafeMon2Level.append(inner[6])
            plt.figure(1)
            plt.plot(timeArmingIndex, armingCurrentLevel, label="Current (Amperes)")
            plt.plot(timeArmingIndex, armingArmMon1Level, label = "Arm Monitor #1 (Volts)")
            plt.plot(timeArmingIndex, armingSafeMon1Level, label = "Safe Monitor #1 (Volts)")
            plt.plot(timeArmingIndex, armingArmMon2Level, label = "Arm Monitor #2 (Volts)")
            plt.plot(timeArmingIndex, armingSafeMon2Level, label = "Safe Monitor #2 (Volts)")
            plt.xlabel('Time-stamp (s)')
            plt.ylabel('Measurement Level (Volts/Amperes)')
            plt.title('Arming Cycle Performance')
            plt.legend(loc='upper right', bbox_to_anchor=(1.00, 0.94), fontsize='x-small')
            plt.savefig('C:/repos/ortint/img/Limited_Arming_Cycle_' + 'SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M"))
            #plt.show()

            conn.commit()
            conn.close()
        def safePlot():
            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM interrupterSafingQry')
            safingSummary = cur.fetchall()

            fileData = open('SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M") + '.csv', 'w')
            fileData.write("testID,timeID,currentLevel,armMon1VoltLevel,safeMon1VoltLevel,armMon2VoltLevel,safeMon2VoltLevel\n")
            for row in safingSummary:
                fileData.write(str(row).replace('(','').replace(')','') + '\n')
            fileData.close()
            timeSafingIndex = []
            safingCurrentLevel = []
            safingArmMon1Level = []
            safingSafeMon1Level = []
            safingArmMon2Level = []
            safingSafeMon2Level = []

            for inner in safingSummary:
                timeSafingIndex.append(inner[1])
                safingCurrentLevel.append(inner[2])
                safingArmMon1Level.append(inner[3])
                safingSafeMon1Level.append(inner[4])
                safingArmMon2Level.append(inner[5])
                safingSafeMon2Level.append(inner[6])
            plt.figure(2)
            plt.plot(timeSafingIndex, safingCurrentLevel, label="Current (Amperes)")
            plt.plot(timeSafingIndex, safingArmMon1Level, label = "Arm Monitor #1 (Volts)")
            plt.plot(timeSafingIndex, safingSafeMon1Level, label = "Safe Monitor #1 (Volts)")
            plt.plot(timeSafingIndex, safingArmMon2Level, label = "Arm Monitor #2 (Volts)")
            plt.plot(timeSafingIndex, safingSafeMon2Level, label = "Safe Monitor #2 (Volts)")
            plt.xlabel('Time-stamp (s)')
            plt.ylabel('Measurement Level (Volts/Amperes)')
            plt.title('Safing Cycle Performance')
            plt.legend(loc='upper right', bbox_to_anchor=(1.00, 0.93), fontsize='x-small')
            plt.savefig(
                'C:/repos/ortint/img/Limited_Safing_Cycle_' + 'SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                    "%Y-%m-%d-%H-%M"))
            #plt.show()

            conn.commit()
            conn.close()
        def calcArmStats():
            calcArmStats.maxCurrent = max(collectArmingDMM.arming_current_values)

            # Make a dictionary from two lists
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.arming_current_values))
            voltStep = collectArmingDMM.arming_armMon2_values
            arm = dict(zip(time, voltStep))
            # The first time stamp
            startArmCycleTimeIdx = next(iter(arm))

            # After the first eight consecutive high voltages, print the last one as endCycleTime
            timeIdxArm = 8
            for key in arm:
                if arm[key] > 4 and timeIdxArm > 0:
                    armCycleEndTime = key
                    timeIdxArm = timeIdxArm -1
            endArmCycleTimeIdx = armCycleEndTime
            # Calculate Cycle Time
            calcArmStats.cycleTimeArm = endArmCycleTimeIdx - startArmCycleTimeIdx
        def saveArmData():
            # Make a dictionary from two lists
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.temp_values3))

            fileData = open(str('current-arming-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            current = collectArmingDMM.temp_values
            arm = dict(zip(time, current))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-safe-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS2 = collectArmingDMM.temp_values2
            arm = dict(zip(time, voltStepS2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-arm-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA2 = collectArmingDMM.temp_values3
            arm = dict(zip(time, voltStepA2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-safe-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS1 = collectArmingDMM.temp_values4
            arm = dict(zip(time, voltStepS1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-arm-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA1 = collectArmingDMM.temp_values5
            arm = dict(zip(time, voltStepA1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()
        def saveSafeData():
            # Make a dictionary from two lists
            time = np.linspace(float(startTimerSafing.startMS), float(stopTimerSafing.endMS), len(collectSafingDMM.temp_values4_S))

            fileData = open(str('current-safing-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            current = collectSafingDMM.temp_values_S
            arm = dict(zip(time, current))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-safe-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS2 = collectSafingDMM.temp_values2_S
            arm = dict(zip(time, voltStepS2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-arm-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA2 = collectSafingDMM.temp_values3_S
            arm = dict(zip(time, voltStepA2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-safe-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS1 = collectSafingDMM.temp_values4_S
            arm = dict(zip(time, voltStepS1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safing-arm-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA1 = collectSafingDMM.temp_values5_S
            arm = dict(zip(time, voltStepA1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()
        def calcSafeStats():
            calcSafeStats.maxCurrent = max(collectSafingDMM.safing_current_values)

            # Make a dictionary from two lists
            time = np.linspace(float(startTimerSafing.start), float(stopTimerSafing.end), len(collectSafingDMM.safing_safeMon1_values))
            voltStepSafe = collectSafingDMM.safing_safeMon1_values
            safe = dict(zip(time, voltStepSafe))
            # The first time stamp
            startSafeCycleTimeIdx = next(iter(safe))

            # After the first eight consecutive high voltages, print the last one as endCycleTime
            timeIdx = 8
            for key in safe:
                if safe[key] > 4 and timeIdx > 0:
                    safeCycleEndTime = key
                    timeIdx = timeIdx -1
            endSafeCycleTimeIdx = safeCycleEndTime
            # Calculate Cycle Time
            calcSafeStats.cycleTimeSafe = endSafeCycleTimeIdx - startSafeCycleTimeIdx
        def closePowerSupplies():
            print("Turning off Jupiter-Arming and Jupiter-Safing Power Supplies...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.close()
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_SAFING_E3634A.write('*CLS')
            JUPITER_SAFING_E3634A.write('*RST')
            JUPITER_SAFING_E3634A.close()
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write('*CLS')
            JUPITER_GALILEO_E3634A.write('*RST')
            JUPITER_GALILEO_E3634A.close()
            print("...Jupiter-Arming and Jupiter-Safing are new off and reset.")
        def closeDMM():
            METIS_06676.close()
            CALLISTO_01437.close()
            GANYMEDE_03625.close()
            IO_06446.close()
            EUROPA_00866.close()
            rm.close()
            print("DMMs are now Closed")
        def printToScreen():
            print("Step (a): The maximum Current reached during the Arming cycle was {} Amperes".format(
                calcArmStats.maxCurrent))
            print("Step (a): Total Arming Time = {} seconds".format(calcArmStats.cycleTimeArm))
            print("Step (b): Safe Monitor2 Resistance after Arming is = {} Ohms".format(getResArm.aResistance))
            print("Step (b): Arm Monitor2 Resistance after Arming is = {} Ohms".format(getResArm.bResistance))
            print("Step (b): Safe Monitor1 Resistance after Arming is = {} Ohms".format(getResArm.cResistance))
            print("Step (b): Arm Monitor1 Resistance after Arming is = {} Ohms".format(getResArm.dResistance))

            print("Step (c): The maximum Current reached during the Safing cycle was {} Amperes".format(
                calcSafeStats.maxCurrent))
            print("Step (c): Total Safing Time = {} seconds".format(calcSafeStats.cycleTimeSafe))
            print("Step (d): Safe Monitor2 Resistance after Arming is = {} Ohms".format(getResSafe.aResistance))
            print("Step (d): Arm Monitor2 Resistance after Arming is = {} Ohms".format(getResSafe.bResistance))
            print("Step (d): Safe Monitor1 Resistance after Arming is = {} Ohms".format(getResSafe.cResistance))
            print("Step (d): Arm Monitor1 Resistance after Arming is = {} Ohms".format(getResSafe.dResistance))
        def writeLimitedReport():
            f = open('SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M") + '.html', 'w')
            f.write("""<html lang="en">""")
            f.write("""<head>""")
            f.write("""  <meta charset="utf-8">""")
            f.write("""    <title>Test Report</title>""")
            f.write("""  <meta name="description" content="Systima Ordnance Interrupter Test Bench">""")
            f.write("""  <meta name="author" content="SitePoint">""")
            f.write("""  <link rel="stylesheet" href="simple.css" type="text/css"/>""")
            f.write("</head>")
            f.write("<!doctype html>")
            f.write("<body>")

            f.write("""<h1>Test Report</h1>""")
            f.write("""<h2>Test Type:""" + interrupterApp.testType + """ </h2>""")
            f.write("""<h4>ULA Specification:  """ + numSpecULA + """</h4>""")
            f.write("""<h4>Test Date:  """ + testDate.strftime("%Y-%m-%d %H:%M") + """</h4>""")
            f.write("""<h4>Part Number:  """ + partNumber + """</h4>""")
            f.write("""<h4>Serial Number:  """ + getUserInitialData.serialNumber + """</h4>""")
            f.write("""<h4>Name of Systima Test Engineer:  """ + getUserInitialData.operatorsName + """</h4>""")

            f.write("""<h2>RAW RESULTS</h2>""")

            f.write("""<b>Step (a):</b> The maximum Current reached during the Arming cycle was """ + str(
                calcArmStats.maxCurrent) + """ Amperes.<br>""")
            f.write("""<b>Step (a):</b> Total Arming Time was """ + str(calcArmStats.cycleTimeArm) + """ seconds.<br>""")
            f.write("""<b>Step (a):</b> Visual Check is """ + str(visualArmCheck.armedCondition) + """, checked Manually.<br><br>""")

            f.write("""<b>Step (b):</b> Safe Monitor #2 Resistance after Arming is """ + str(
                getResArm.aResistance) + """ Ohms.<br>""")
            f.write("""<b>Step (b):</b> Arm Monitor #2 Resistance after Arming is""" + str(
                getResArm.bResistance) + " Ohms.<br>""")
            f.write("""<b>Step (b):</b> Safe Monitor #1 Resistance after Arming is """ + str(
                getResArm.cResistance) + """ Ohms.<br>""")
            f.write("""<b>Step (b):</b> Arm Monitor #1 Resistance after Arming is """ + str(
                getResArm.dResistance) + """ Ohms.<br><br>""")

            f.write("""<b>Step (c):</b> The maximum Current reached during the Safing cycle was """ + str(
                calcSafeStats.maxCurrent) + """ Amperes.<br>""")
            f.write("""<b>Step (c):</b> Total Safing Time was """ + str(calcSafeStats.cycleTimeSafe) + """ seconds.<br>""")
            f.write("""<b>Step (c):</b> Visual Check is """ + str(visualSafeCheck.safedCondition) + """, checked Manually.<br><br>""")

            f.write("""<b>Step (d):</b> Safe Monitor #2 Resistance after Safing is """ + str(
                getResSafe.aResistance) + """ Ohms.<br>""")
            f.write("""<b>Step (d):</b> Arm Monitor #2 Resistance after Safing is""" + str(
                getResSafe.bResistance) + " Ohms.<br>""")
            f.write("""<b>Step (d):</b> Safe Monitor #1 Resistance after Safing is """ + str(
                getResSafe.cResistance) + """ Ohms.<br>""")
            f.write("""<b>Step (d):</b> Arm Monitor #1 Resistance after Safing is """ + str(
                getResSafe.dResistance) + """ Ohms.<br>""")

            f.write("""<h2>PASS/FAIL RESULTS</h2>""")

            f.write(str(
                "Max Arming Current....... = PASS<br>" if calcArmStats.maxCurrent < maxCurrentSpec else "Max Arming Current....... = FAIL<br>"))
            f.write(str(
                "Max Arming Cycle Time.... = PASS<br>" if calcArmStats.cycleTimeArm < maxCycTimeSpec else "Max Arming Cycle Time.... = FAIL<br>"))
            f.write(str(
                "Visual Armed Inspection...= PASS<br>" if int(visualArmCheck.armedCondition) == 1 else "Visual Armed Inspection...= FAIL<br>"))
            f.write(str(
                "Safe Monitor 2 Resistance = PASS<br>" if getResArm.aResistance > minResSpec else "Safe Monitor 2 Resistance = FAIL<br>"))
            f.write(str(
                "Arm  Monitor 2 Resistance = PASS<br>" if getResArm.bResistance < maxResSpec else "Arm  Monitor 2 Resistance = FAIL<br>"))
            f.write(str(
                "Safe Monitor 1 Resistance = PASS<br>" if getResArm.cResistance > minResSpec else "Safe Monitor 2 Resistance = FAIL<br>"))
            f.write(str(
                "Arm  Monitor 1 Resistance = PASS<br><br>" if getResArm.dResistance < maxResSpec else "Arm  Monitor 2 Resistance = FAIL<br>"))

            f.write(str(
                "Max Safing Current....... = PASS<br>" if calcSafeStats.maxCurrent < maxCurrentSpec else "Max Safing Current....... = FAIL<br>"))
            f.write(str(
                "Max Safing Cycle Time.... = PASS<br>" if calcSafeStats.cycleTimeSafe < maxCycTimeSpec else "Max Safing Cycle Time.... = FAIL<br>"))
            f.write(str(
                "Visual Safed Inspection...= PASS<br>" if int(visualSafeCheck.safedCondition) == 2 else "Visual Safed Inspection...= FAIL<br>"))
            f.write(str(
                "Safe Monitor 2 Resistance = PASS<br>" if getResSafe.aResistance < maxResSpec else "Safe Monitor 2 Resistance = FAIL<br>"))
            f.write(str(
                "Arm  Monitor 2 Resistance = PASS<br>" if getResSafe.bResistance > minResSpec else "Arm  Monitor 2 Resistance = FAIL<br>"))
            f.write(str(
                "Safe Monitor 1 Resistance = PASS<br>" if getResSafe.cResistance < maxResSpec else "Safe Monitor 1 Resistance = FAIL<br>"))
            f.write(str(
                "Arm  Monitor 1 Resistance = PASS<br><br>" if getResSafe.dResistance > minResSpec else "Arm  Monitor 1 Resistance = FAIL<br>"))

            f.write("""<h2>TIME PLOTS</h2>""")

            f.write("""<h4>Safe/Arm Circuit During Arming Cycle</h4>""")
            f.write("""<img src="img\Limited_Arming_Cycle_"""  + 'SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime("%Y-%m-%d-%H-%M") + """.png" alt="ArmCurrent" style="width:800px;height:600px;">""")


            f.write("""<h4>Safe/Arm Circuit During Safing Cycle</h4>""")
            f.write("""<img src="img\Limited_Safing_Cycle_"""  + 'SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime("%Y-%m-%d-%H-%M") + """.png" alt="ArmCurrent" style="width:800px;height:600px;">""")
            f.write("""  <script src="js/scripts.js"></script>""")
            f.write("</body>")
            f.write("</html>")

            f.close()
        getUserInitialData()
        simpleSafingCycle()
        configurePowerSupplyJupiterArming()
        configurePowerSupplyJupiterSafing()
        configurePowerSupplyGalileo()
        setupDMM()
        startTimerArming()
        armingCyclePower()
        getDmmVoltageData()
        collectArmingDMM()
        stopTimerArming()
        visualArmCheck()
        configureArmedResistanceMeasure()
        getResArm()
        getArmingDB()
        armPlot()
        calcArmStats()
        # saveArmData()

        setupDMM()
        startTimerSafing()
        safingCyclePower()
        getDmmVoltageData()
        collectSafingDMM()
        stopTimerSafing()
        visualSafeCheck()
        configureSafedResistanceMeasure()
        getResSafe()
        getSafingDB()
        safePlot()
        calcSafeStats()
        # saveSafeData()
        writeLimitedReport()
        closePowerSupplies()
        closeDMM()

    def limitedArmToSafe(psVoltageLevel):
        def getUserInitialData():
            getUserInitialData.operatorsName = input("What is your name (First, Last)?     ")
            getUserInitialData.serialNumber = input("What is the serial number stamped into the base of this Ordnance Interrupter?    ")
        def visualArmCheck():
            visualArmCheck.armedCondition = input("Can you see the Armed Indicator?:\n (Please respond with:\n 1. Armed\n 2. Safed\n\n")

            if visualArmCheck.armedCondition == 1 or 2:
               visualArmCheck.armedCondition = visualArmCheck.armedCondition
               print("Thank you. Now continuing test.....")
            else:
              print("Please respond with '1' or '2'")
        def visualSafeCheck():
            visualSafeCheck.safedCondition = input("Can you see the Safed Indicator?:\n (Please respond with:\n 1. Armed\n 2. Safed\n\n")

            if visualSafeCheck.safedCondition == 1 or 2:
               visualSafeCheck.safedCondition = visualSafeCheck.safedCondition
               print("Thank you. Now continuing test.....")
            else:
              print("Please respond with '1' or '2'")
        def simpleSafingCycle():
            print("Safing the Device...")
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_SAFING_E3634A.write('*CLS')
            JUPITER_SAFING_E3634A.write('*RST')
            JUPITER_SAFING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_SAFING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % ('MAXimum'))
            JUPITER_SAFING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (1))
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (1))
            time.sleep(0.256)
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            print("...finished safing the device")
        def configurePowerSupplyJupiterArming():
            print("Setting up Jupiter Arming...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            print("Jupiter-Arming Power Supply is now Configured")
        def configurePowerSupplyJupiterSafing():
            print("Setting up Jupiter Safing...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (psVoltageLevel))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_ARMING_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            print("Jupiter-Safing Power Supply is now Configured")
        def configurePowerSupplyGalileo():
            print("Setting up Galileo...")
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write('*CLS')
            JUPITER_GALILEO_E3634A.write('*RST')
            JUPITER_GALILEO_E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (5.0))
            JUPITER_GALILEO_E3634A.write(':SOURce:CURRent:PROTection:LEVel %s' % (current))
            JUPITER_GALILEO_E3634A.write(':SOURce:CURRent:PROTection:STATe %d' % (state))
            #JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            time.sleep(0.512)
            print("Galileo Power Supply is now Configured and Output is On")
        def setupDMM():
            METIS_06676.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_DC_CURRENT.sta'))
            METIS_06676.write(':TRIGger:SOURce %s' % ('IMMediate'))
            METIS_06676.write(':TRIGger:COUNt %G' % (1.0))
            METIS_06676.write(':SENSe:CURRent:DC:RANGe %G' % (0.01))
            METIS_06676.write(':SENSe:CURRent:DC:TERMinals %d' % (10))
            METIS_06676.write(':SAMPle:COUNt %d' % (16384))
            print("Metis is Configured")

            CALLISTO_01437.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_DC_CURRENT.sta'))
            CALLISTO_01437.write(':TRIGger:SOURce %s' % ('IMMediate'))
            CALLISTO_01437.write(':TRIGger:COUNt %G' % (1.0))
            CALLISTO_01437.write(':SENSe:CURRent:DC:RANGe %G' % (0.01))
            CALLISTO_01437.write(':SENSe:CURRent:DC:TERMinals %d' % (10))
            CALLISTO_01437.write(':SAMPle:COUNt %d' % (16384))
            print("Callisto is Configured")

            # Load DMM Voltage Configuration State Files
            GANYMEDE_03625.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            THEBE_00599.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            IO_06446.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))
            EUROPA_00866.write(':MMEMory:LOAD:STATe "%s"' % ('INT:\\STATE_100V.sta'))

            # Configure DMM for Voltage or Resistance on Safe Monitor #2
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            GANYMEDE_03625.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            GANYMEDE_03625.write(':TRIGger:COUNt %G' % (1.0))
            GANYMEDE_03625.write(':SAMPle:COUNt %d' % (16384))
            print("Ganymede is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            THEBE_00599.write(':TRIGger:COUNt %G' % (1.0))
            THEBE_00599.write(':SAMPle:COUNt %d' % (16384))
            print("Thebe is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            IO_06446.write(':TRIGger:COUNt %G' % (1.0))
            IO_06446.write(':SAMPle:COUNt %d' % (16384))
            print("Io is Configured")

            # Configure DMM for Voltage or Resistance on Arm Monitor #2
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':SENSe:VOLTage:DC:RANGe:AUTO %d' % (0))
            EUROPA_00866.write(':TRIGger:COUNt %G' % (1.0))
            EUROPA_00866.write(':SAMPle:COUNt %d' % (16384))
            time.sleep(0.128)
            print("Europa is Configured")
        def startTimerArming():
            startTimerArming.start = time.time()
            startTimerArming.startTime = datetime.datetime.now().time()
            startTimerArming.startMS = datetime.datetime.now().strftime('%S.%f')
            print("Arming Timer is started at {}".format(startTimerArming.start))
        def startTimerSafing():
            startTimerSafing.start = time.time()
            startTimerSafing.startTime = datetime.datetime.now().time()
            startTimerSafing.startMS = datetime.datetime.now().strftime('%S.%f')
            print("Safing Timer is started at {}".format(startTimerSafing.start))
        def getDmmVoltageData():
            print("Initiate all DMMs...")
            METIS_06676.write(':INITiate:IMMediate')
            CALLISTO_01437.write(':INITiate:IMMediate')
            GANYMEDE_03625.write(':INITiate:IMMediate')
            THEBE_00599.write(':INITiate:IMMediate')
            IO_06446.write(':INITiate:IMMediate')
            EUROPA_00866.write(':INITiate:IMMediate')
            print("...DMMs are all Intitiated.")
        def armingCyclePower():
            print("Turning Jupiter-Arming Output to 'ON'... ")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (1))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            print("...Jupiter-Arming is now ON")
        def safingCyclePower():
            print("Turning Jupiter-Safing Output to 'ON'... ")
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (1))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (1))
            print("...Jupiter-Safing is now ON")
        def collectArmingDMM():
            collectArmingDMM.arming_current_values = METIS_06676.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_current_readings = collectArmingDMM.arming_current_values[0]
            collectArmingDMM.arming_safeMon2_values = GANYMEDE_03625.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_safeMon2_readings = collectArmingDMM.arming_safeMon2_values[0]
            collectArmingDMM.arming_armMon2_values = THEBE_00599.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_armMon2_readings = collectArmingDMM.arming_armMon2_values[0]
            collectArmingDMM.arming_safeMon1_values = IO_06446.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_safeMon1_readings = collectArmingDMM.arming_safeMon1_values[0]
            collectArmingDMM.arming_armMon1_values = EUROPA_00866.query_ascii_values(':FETCh?')
            collectArmingDMM.arming_armMon1_readings = collectArmingDMM.arming_armMon1_values[0]
        def collectSafingDMM():
            collectSafingDMM.safing_current_values = CALLISTO_01437.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_current_readings = collectSafingDMM.safing_current_values[0]
            collectSafingDMM.safing_safeMon2_values = GANYMEDE_03625.query_ascii_values(':FETCh?')
            collectSafingDMM.asafing_safeMon2_readings = collectSafingDMM.safing_safeMon2_values[0]
            collectSafingDMM.safing_armMon2_values = THEBE_00599.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_armMon2_readings = collectSafingDMM.safing_armMon2_values[0]
            collectSafingDMM.safing_safeMon1_values = IO_06446.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_safeMon1_readings = collectSafingDMM.safing_safeMon1_values[0]
            collectSafingDMM.safing_armMon1_values = EUROPA_00866.query_ascii_values(':FETCh?')
            collectSafingDMM.safing_armMon1_readings = collectSafingDMM.safing_armMon1_values[0]
        def stopTimerArming():
            stopTimerArming.end = time.time()
            stopTimerArming.endTime = datetime.datetime.now().time()
            stopTimerArming.endMS = datetime.datetime.now().strftime('%S.%f')
            print("Arming Timer stopped at {} ".format(stopTimerArming.end))
            time.sleep(0.128)
        def stopTimerSafing():
            stopTimerSafing.end = time.time()
            stopTimerSafing.endTime = datetime.datetime.now().time()
            stopTimerSafing.endMS = datetime.datetime.now().strftime('%S.%f')
            print("Safing Timer stopped at {} ".format(stopTimerSafing.end))
            time.sleep(0.128)
        def configureArmedResistanceMeasure():
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            time.sleep(0.128)
        def configureSafedResistanceMeasure():
            GANYMEDE_03625.write(':TRIGger:SOURce %s' % ('IMMediate'))
            THEBE_00599.write(':TRIGger:SOURce %s' % ('IMMediate'))
            IO_06446.write(':TRIGger:SOURce %s' % ('IMMediate'))
            EUROPA_00866.write(':TRIGger:SOURce %s' % ('IMMediate'))
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            time.sleep(0.128)
        def getResArm():
            getResArm.temp_valuesR = GANYMEDE_03625.query_ascii_values(':MEASure:RESistance?')
            getResArm.aResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = THEBE_00599.query_ascii_values(':MEASure:RESistance?')
            getResArm.bResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = IO_06446.query_ascii_values(':MEASure:RESistance?')
            getResArm.cResistance = getResArm.temp_valuesR[0]
            getResArm.temp_valuesR = EUROPA_00866.query_ascii_values(':MEASure:RESistance?')
            getResArm.dResistance = getResArm.temp_valuesR[0]
        def getResSafe():
            getResSafe.temp_valuesR = GANYMEDE_03625.query_ascii_values(':MEASure:RESistance?')
            getResSafe.aResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = THEBE_00599.query_ascii_values(':MEASure:RESistance?')
            getResSafe.bResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = IO_06446.query_ascii_values(':MEASure:RESistance?')
            getResSafe.cResistance = getResSafe.temp_valuesR[0]
            getResSafe.temp_valuesR = EUROPA_00866.query_ascii_values(':MEASure:RESistance?')
            getResSafe.dResistance = getResSafe.temp_valuesR[0]
        def getArmingDB():
            testID = str(getUserInitialData.serialNumber + "-" + testDate.strftime('%b-%d-%H-%M-%S'))
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.arming_current_values))

            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()

            cur.execute('DROP TABLE IF EXISTS ArmingCurrentTable')
            cur.execute('DROP TABLE IF EXISTS ArmingSafeMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS ArmingArmMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS ArmingSafeMonOneTable')
            cur.execute('DROP TABLE IF EXISTS ArmingArmMonOneTable')
            cur.execute('CREATE TABLE ArmingCurrentTable (testID TEXT, timeID FLOAT, currentLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingSafeMonTwoTable (testID TEXT, timeID FLOAT, safeMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingArmMonTwoTable (testID TEXT, timeID FLOAT, armMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingSafeMonOneTable (testID TEXT, timeID FLOAT, safeMon1VoltLevel FLOAT)')
            cur.execute('CREATE TABLE ArmingArmMonOneTable (testID TEXT, timeID FLOAT, armMon1VoltLevel FLOAT)')

            stepCurrent = collectArmingDMM.arming_current_values
            arm = dict(zip(time, stepCurrent))
            for key in arm:
                cur.execute('INSERT INTO ArmingCurrentTable (testID,timeID,currentLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key)), ('{}'.format(arm[key]))))

            stepSafeMon2 = collectArmingDMM.arming_safeMon2_values
            arm2 = dict(zip(time, stepSafeMon2))
            for key2 in arm2:
                cur.execute('INSERT INTO ArmingSafeMonTwoTable (testID,timeID,safeMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key2)), ('{}'.format(arm2[key2]))))

            stepArmMon2 = collectArmingDMM.arming_armMon2_values
            arm3 = dict(zip(time, stepArmMon2))
            for key3 in arm3:
                cur.execute('INSERT INTO ArmingArmMonTwoTable (testID,timeID,armMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key3)), ('{}'.format(arm3[key3]))))

            stepSafeMon1 = collectArmingDMM.arming_safeMon1_values
            arm4 = dict(zip(time, stepSafeMon1))
            for key4 in arm4:
                cur.execute('INSERT INTO ArmingSafeMonOneTable (testID,timeID,safeMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key4)), ('{}'.format(arm4[key4]))))

            stepArmMon1 = collectArmingDMM.arming_armMon1_values
            arm5 = dict(zip(time, stepArmMon1))
            for key5 in arm5:
                cur.execute('INSERT INTO ArmingArmMonOneTable (testID,timeID,armMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key5)), ('{}'.format(arm5[key5]))))
            conn.commit()
            conn.close()
        def getSafingDB():
            testID = str(getUserInitialData.serialNumber + "-" + testDate.strftime('%b-%d-%H-%M-%S'))
            time = np.linspace(float(startTimerSafing.start), float(stopTimerSafing.end), len(collectSafingDMM.safing_current_values))

            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()

            cur.execute('DROP TABLE IF EXISTS SafingCurrentTable')
            cur.execute('DROP TABLE IF EXISTS SafingSafeMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS SafingArmMonTwoTable')
            cur.execute('DROP TABLE IF EXISTS SafingSafeMonOneTable')
            cur.execute('DROP TABLE IF EXISTS SafingArmMonOneTable')
            cur.execute('CREATE TABLE SafingCurrentTable (testID TEXT, timeID FLOAT, currentLevel FLOAT)')
            cur.execute('CREATE TABLE SafingSafeMonTwoTable (testID TEXT, timeID FLOAT, safeMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingArmMonTwoTable (testID TEXT, timeID FLOAT, armMon2VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingSafeMonOneTable (testID TEXT, timeID FLOAT, safeMon1VoltLevel FLOAT)')
            cur.execute('CREATE TABLE SafingArmMonOneTable (testID TEXT, timeID FLOAT, armMon1VoltLevel FLOAT)')

            stepCurrentS = collectSafingDMM.safing_current_values
            arm = dict(zip(time, stepCurrentS))
            for key in arm:
                cur.execute('INSERT INTO SafingCurrentTable (testID,timeID,currentLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key)), ('{}'.format(arm[key]))))

            stepSafeMon2S = collectSafingDMM.safing_safeMon2_values
            arm2 = dict(zip(time, stepSafeMon2S))
            for key2 in arm2:
                cur.execute('INSERT INTO SafingSafeMonTwoTable (testID,timeID,safeMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key2)), ('{}'.format(arm2[key2]))))

            stepArmMon2S = collectSafingDMM.safing_armMon2_values
            arm3 = dict(zip(time, stepArmMon2S))
            for key3 in arm3:
                cur.execute('INSERT INTO SafingArmMonTwoTable (testID,timeID,armMon2VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key3)), ('{}'.format(arm3[key3]))))

            stepSafeMon1S = collectSafingDMM.safing_safeMon1_values
            arm4 = dict(zip(time, stepSafeMon1S))
            for key4 in arm4:
                cur.execute('INSERT INTO SafingSafeMonOneTable (testID,timeID,safeMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key4)), ('{}'.format(arm4[key4]))))

            stepArmMon1S = collectSafingDMM.safing_armMon1_values
            arm5 = dict(zip(time, stepArmMon1S))
            for key5 in arm5:
                cur.execute('INSERT INTO SafingArmMonOneTable (testID,timeID,armMon1VoltLevel) VALUES (?,?,?)', (('{}'.format(testID)), ('{}'.format(key5)), ('{}'.format(arm5[key5]))))
            conn.commit()
            conn.close()
        def armPlot():
            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM interrupterArmingQry')
            armingSummary = cur.fetchall()

            fileData = open('SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M") + '.csv', 'w')
            fileData.write("testID,timeID,currentLevel,armMon1VoltLevel,safeMon1VoltLevel,armMon2VoltLevel,safeMon2VoltLevel\n")
            for row in armingSummary:
                fileData.write(str(row).replace('(','').replace(')','') + '\n')
            fileData.close()

            timeArmingIndex = []
            armingCurrentLevel = []
            armingArmMon1Level = []
            armingSafeMon1Level = []
            armingArmMon2Level = []
            armingSafeMon2Level = []

            for inner in armingSummary:
                timeArmingIndex.append(inner[1])
                armingCurrentLevel.append(inner[2])
                armingArmMon1Level.append(inner[3])
                armingSafeMon1Level.append(inner[4])
                armingArmMon2Level.append(inner[5])
                armingSafeMon2Level.append(inner[6])
            plt.figure(1)
            plt.plot(timeArmingIndex, armingCurrentLevel, label="Current (Amperes)")
            plt.plot(timeArmingIndex, armingArmMon1Level, label = "Arm Monitor #1 (Volts)")
            plt.plot(timeArmingIndex, armingSafeMon1Level, label = "Safe Monitor #1 (Volts)")
            plt.plot(timeArmingIndex, armingArmMon2Level, label = "Arm Monitor #2 (Volts)")
            plt.plot(timeArmingIndex, armingSafeMon2Level, label = "Safe Monitor #2 (Volts)")
            plt.xlabel('Time-stamp (s)')
            plt.ylabel('Measurement Level (Volts/Amperes)')
            plt.title('Arming Cycle Performance')
            plt.legend(loc='upper right', bbox_to_anchor=(1.00, 0.94), fontsize='x-small')
            plt.savefig('C:/repos/ortint/img/Limited_Arming_Cycle_' + 'SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M"))
            #plt.show()

            conn.commit()
            conn.close()
        def safePlot():
            conn = sqlite3.connect('interrupter.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM interrupterSafingQry')
            safingSummary = cur.fetchall()

            fileData = open('SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M") + '.csv', 'w')
            fileData.write("testID,timeID,currentLevel,armMon1VoltLevel,safeMon1VoltLevel,armMon2VoltLevel,safeMon2VoltLevel\n")
            for row in safingSummary:
                fileData.write(str(row).replace('(','').replace(')','') + '\n')
            fileData.close()

            timeSafingIndex = []
            safingCurrentLevel = []
            safingArmMon1Level = []
            safingSafeMon1Level = []
            safingArmMon2Level = []
            safingSafeMon2Level = []

            for inner in safingSummary:
                timeSafingIndex.append(inner[1])
                safingCurrentLevel.append(inner[2])
                safingArmMon1Level.append(inner[3])
                safingSafeMon1Level.append(inner[4])
                safingArmMon2Level.append(inner[5])
                safingSafeMon2Level.append(inner[6])
            plt.figure(2)
            plt.plot(timeSafingIndex, safingCurrentLevel, label="Current (Amperes)")
            plt.plot(timeSafingIndex, safingArmMon1Level, label = "Arm Monitor #1 (Volts)")
            plt.plot(timeSafingIndex, safingSafeMon1Level, label = "Safe Monitor #1 (Volts)")
            plt.plot(timeSafingIndex, safingArmMon2Level, label = "Arm Monitor #2 (Volts)")
            plt.plot(timeSafingIndex, safingSafeMon2Level, label = "Safe Monitor #2 (Volts)")
            plt.xlabel('Time-stamp (s)')
            plt.ylabel('Measurement Level (Volts/Amperes)')
            plt.title('Safing Cycle Performance')
            plt.legend(loc='upper right', bbox_to_anchor=(1.00, 0.93), fontsize='x-small')
            plt.savefig(
                'C:/repos/ortint/img/Limited_Safing_Cycle_' + 'SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                    "%Y-%m-%d-%H-%M"))
            #plt.show()

            conn.commit()
            conn.close()
        def calcArmStats():
            calcArmStats.maxCurrent = max(collectArmingDMM.arming_current_values)

            # Make a dictionary from two lists
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.arming_current_values))
            voltStep = collectArmingDMM.arming_armMon2_values
            arm = dict(zip(time, voltStep))
            # The first time stamp
            startArmCycleTimeIdx = next(iter(arm))

            # After the first eight consecutive high voltages, print the last one as endCycleTime
            timeIdxArm = 8
            for key in arm:
                if arm[key] > 4 and timeIdxArm > 0:
                    armCycleEndTime = key
                    timeIdxArm = timeIdxArm -1
            endArmCycleTimeIdx = armCycleEndTime
            # Calculate Cycle Time
            calcArmStats.cycleTimeArm = endArmCycleTimeIdx - startArmCycleTimeIdx
        def saveArmData():
            # Make a dictionary from two lists
            time = np.linspace(float(startTimerArming.start), float(stopTimerArming.end), len(collectArmingDMM.temp_values3))

            fileData = open(str('current-arming-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            current = collectArmingDMM.temp_values
            arm = dict(zip(time, current))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-safe-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS2 = collectArmingDMM.temp_values2
            arm = dict(zip(time, voltStepS2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-arm-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA2 = collectArmingDMM.temp_values3
            arm = dict(zip(time, voltStepA2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-safe-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS1 = collectArmingDMM.temp_values4
            arm = dict(zip(time, voltStepS1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-arming-arm-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA1 = collectArmingDMM.temp_values5
            arm = dict(zip(time, voltStepA1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()
        def saveSafeData():
            # Make a dictionary from two lists
            time = np.linspace(float(startTimerSafing.startMS), float(stopTimerSafing.endMS), len(collectSafingDMM.temp_values4_S))

            fileData = open(str('current-safing-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            current = collectSafingDMM.temp_values_S
            arm = dict(zip(time, current))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-safe-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS2 = collectSafingDMM.temp_values2_S
            arm = dict(zip(time, voltStepS2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-arm-mon2-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA2 = collectSafingDMM.temp_values3_S
            arm = dict(zip(time, voltStepA2))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safeing-safe-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepS1 = collectSafingDMM.temp_values4_S
            arm = dict(zip(time, voltStepS1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()

            fileData = open(str('volts-safing-arm-mon-1-'+ testDate.strftime("%Y-%m-%d-%H%M") +'.csv'), 'w')
            fileData.write("time,level\n")
            voltStepA1 = collectSafingDMM.temp_values5_S
            arm = dict(zip(time, voltStepA1))
            for key in arm:
                dataLine = str("{}".format(key) + ",{}\n".format(arm[key]))
                fileData.write(dataLine)
            fileData.close()
        def calcSafeStats():
            calcSafeStats.maxCurrent = max(collectSafingDMM.safing_current_values)

            # Make a dictionary from two lists
            time = np.linspace(float(startTimerSafing.start), float(stopTimerSafing.end), len(collectSafingDMM.safing_safeMon1_values))
            voltStepSafe = collectSafingDMM.safing_safeMon1_values
            safe = dict(zip(time, voltStepSafe))
            # The first time stamp
            startSafeCycleTimeIdx = next(iter(safe))

            # After the first eight consecutive high voltages, print the last one as endCycleTime
            timeIdx = 8
            for key in safe:
                if safe[key] > 4 and timeIdx > 0:
                    safeCycleEndTime = key
                    timeIdx = timeIdx -1
            endSafeCycleTimeIdx = safeCycleEndTime
            # Calculate Cycle Time
            calcSafeStats.cycleTimeSafe = endSafeCycleTimeIdx - startSafeCycleTimeIdx
        def closePowerSupplies():
            print("Turning off Jupiter-Arming and Jupiter-Safing Power Supplies...")
            JUPITER_ARMING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_ARMING_E3634A.write('*CLS')
            JUPITER_ARMING_E3634A.write('*RST')
            JUPITER_ARMING_E3634A.close()
            JUPITER_SAFING_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_SAFING_E3634A.write('*CLS')
            JUPITER_SAFING_E3634A.write('*RST')
            JUPITER_SAFING_E3634A.close()
            JUPITER_GALILEO_E3634A.write(':OUTPut:STATe %d' % (0))
            JUPITER_GALILEO_E3634A.write('*CLS')
            JUPITER_GALILEO_E3634A.write('*RST')
            JUPITER_GALILEO_E3634A.close()
            print("...Jupiter-Arming and Jupiter-Safing are new off and reset.")
        def closeDMM():
            METIS_06676.close()
            CALLISTO_01437.close()
            GANYMEDE_03625.close()
            IO_06446.close()
            EUROPA_00866.close()
            rm.close()
            print("DMMs are now Closed")
        def printToScreen():
            print("Step (a): The maximum Current reached during the Arming cycle was {} Amperes".format(
                calcArmStats.maxCurrent))
            print("Step (a): Total Arming Time = {} seconds".format(calcArmStats.cycleTimeArm))
            print("Step (b): Safe Monitor2 Resistance after Arming is = {} Ohms".format(getResArm.aResistance))
            print("Step (b): Arm Monitor2 Resistance after Arming is = {} Ohms".format(getResArm.bResistance))
            print("Step (b): Safe Monitor1 Resistance after Arming is = {} Ohms".format(getResArm.cResistance))
            print("Step (b): Arm Monitor1 Resistance after Arming is = {} Ohms".format(getResArm.dResistance))

            print("Step (c): The maximum Current reached during the Safing cycle was {} Amperes".format(
                calcSafeStats.maxCurrent))
            print("Step (c): Total Safing Time = {} seconds".format(calcSafeStats.cycleTimeSafe))
            print("Step (d): Safe Monitor2 Resistance after Arming is = {} Ohms".format(getResSafe.aResistance))
            print("Step (d): Arm Monitor2 Resistance after Arming is = {} Ohms".format(getResSafe.bResistance))
            print("Step (d): Safe Monitor1 Resistance after Arming is = {} Ohms".format(getResSafe.cResistance))
            print("Step (d): Arm Monitor1 Resistance after Arming is = {} Ohms".format(getResSafe.dResistance))
        def writeFullHReport():
            f = open('SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime(
                "%Y-%m-%d-%H-%M") + '.html', 'w')
            f.write("""<html lang="en">""")
            f.write("""<head>""")
            f.write("""  <meta charset="utf-8">""")
            f.write("""    <title>ULA Ordnance Interrupter Bench Test Report</title>""")
            f.write("""  <meta name="description" content="Systima Ordnance Interrupter Test Bench">""")
            f.write("""  <meta name="author" content="SitePoint">""")
            f.write("""  <link rel="stylesheet" href="simple.css" type="text/css"/>""")
            f.write("</head>")
            f.write("<!doctype html>")
            f.write("<body>")

            f.write("""<h1>Ordnance Interrupter Test Report</h1>""")
            f.write("""<h2>Test Type:""" + interrupterApp.testType + """ </h2>""")
            f.write("""<h4>ULA Specification:  """ + numSpecULA + """</h4>""")
            f.write("""<h4>Test Date:  """ + testDate.strftime("%Y-%m-%d %H:%M") + """</h4>""")
            f.write("""<h4>Part Number:  """ + partNumber + """</h4>""")
            f.write("""<h4>Serial Number:  """ + getUserInitialData.serialNumber + """</h4>""")
            f.write("""<h4>Name of Systima Test Engineer:  """ + getUserInitialData.operatorsName + """</h4>""")

            f.write("""<h2>RAW RESULTS</h2>""")

            f.write("""<b>Step (h):</b> The maximum Current reached during the Arming cycle was """ + str(
                calcArmStats.maxCurrent) + """ Amperes.<br>""")
            f.write("""<b>Step (h):</b> Total Arming Time was """ + str(calcArmStats.cycleTimeArm) + """ seconds.<br>""")
            f.write("""<b>Step (h):</b> Visual Check is """ + str(visualArmCheck.armedCondition) + """, checked Manually.<br><br>""")

            f.write("""<h2>PASS/FAIL RESULTS</h2>""")

            f.write(str(
                "Max Arming Current....... = PASS<br>" if calcArmStats.maxCurrent < maxCurrentSpec else "Max Arming Current....... = FAIL<br>"))
            f.write(str(
                "Max Arming Cycle Time.... = PASS<br>" if calcArmStats.cycleTimeArm < maxCycTimeSpec else "Max Arming Cycle Time.... = FAIL<br>"))
            f.write(str(
                "Visual Armed Inspection...= PASS<br>" if int(visualArmCheck.armedCondition) == 1 else "Visual Armed Inspection...= FAIL<br>"))

            f.write("""<h2>TIME PLOTS</h2>""")

            f.write("""<h4>Safe/Arm Circuit During Arming Cycle</h4>""")
            f.write("""<img src="img\Limited_Arming_Cycle_"""  + 'SN-' + getUserInitialData.serialNumber + '-' + interrupterApp.testType + '-' + testDate.strftime("%Y-%m-%d-%H-%M") + """.png" alt="ArmCurrent" style="width:800px;height:600px;">""")


            f.write("""  <script src="js/scripts.js"></script>""")
            f.write("</body>")
            f.write("</html>")

            f.close()
        getUserInitialData()
        simpleSafingCycle()
        configurePowerSupplyJupiterArming()
        configurePowerSupplyJupiterSafing()
        configurePowerSupplyGalileo()
        setupDMM()
        startTimerArming()
        armingCyclePower()
        getDmmVoltageData()
        collectArmingDMM()
        stopTimerArming()
        visualArmCheck()
        configureArmedResistanceMeasure()
        getResArm()
        getArmingDB()
        armPlot()
        calcArmStats()
        # saveArmData()

        writeFullHReport()
        closePowerSupplies()
        closeDMM()

    interrupterApp()
if __name__ == "__main__": main()
