# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return (self.maxBirthProb)

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return (self.clearProb)

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        # TODO
        wahrscheinlichkeit = random.random()
        
        if wahrscheinlichkeit <= self.clearProb:
            return (True)
        else:
            return (False)

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO
        self.popDensity = popDensity
        
        wahrscheinlichkeit = random.random()
        
        if wahrscheinlichkeit <= self.maxBirthProb * (1 - self.popDensity):
            return (SimpleVirus(self.maxBirthProb, self.clearProb))
        
        else:
            raise NoChildException



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return (self.viruses)


    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return (self.maxPop)


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        # TODO
        return (len(self.viruses))
        


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        partikel = self.viruses[:]
        
        for v in partikel:
            if v.doesClear() == True:
                self.viruses.remove(v)
                
        dichte = len(self.viruses) / self.maxPop
        
        partikel_neu = self.viruses[:]
        for p in partikel_neu:
            try:
                p.reproduce(dichte)
                self.viruses.append(p)
            except NoChildException:
                continue



#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    # TODO
    import numpy as np
    
    daten = np.zeros(300)
    
    for i in range(numTrials):
        partikel = SimpleVirus(maxBirthProb, clearProb)
        Partikel = [partikel] * numViruses
        patient = Patient(Partikel, maxPop)
        virus_anzahl = []
        for n in range(300):
            patient.update()
            virus_anzahl.append(patient.getTotalPop())            
        daten += virus_anzahl
    daten_durchschnitt = daten / numTrials
    
    pylab.plot(list(daten_durchschnitt), label = "SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend (loc = "best")
    pylab.show()

 



   

#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # TODO
        super().__init__(maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return (self.resistances)

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return (self.mutProb)

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        # TODO
        try:
            return self.resistances[drug]
        except KeyError:
            return (False)


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        # TODO
        self.popDensity = popDensity
        self.activeDrugs = activeDrugs
        
        if all([self.isResistantTo(n) for n in self.activeDrugs]) == True:
            wahrscheinlichkeit = random.random()
            if wahrscheinlichkeit <= self.maxBirthProb * (1 - self.popDensity):
                immunisiert = self.resistances.copy()
                for key in self.resistances.keys():
                    Wahrscheinlichkeit = random.random()
                    if Wahrscheinlichkeit <= self.getMutProb():
                        if self.resistances[key] == True:
                            immunisiert[key] = False
                        else:
                            immunisiert[key] = True
                return (ResistantVirus(self.maxBirthProb, self.clearProb, immunisiert, self.mutProb))
            else:
                raise NoChildException
        else:
            raise NoChildException

            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        # TODO
        super().__init__(viruses, maxPop)
        self.prescription = []



    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        # TODO
        self.newDrug = newDrug
        
        if self.newDrug not in self.prescription:
            self.prescription.append(self.newDrug)
        


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return (self.prescription)


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        # TODO
        self.drugResist = drugResist
        
        widerstand = 0
        
        for a in self.viruses:
            for b in self.drugResist:
                if a.resistances.get(b, 0) == False:
                    break
                else:
                    widerstand += 1
                    
        return (widerstand)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        kopie = self.viruses[:]
        for a in kopie:
            if a.doesClear() == True:
                self.viruses.remove(a)
                
        popDensity = len(self.viruses)/self.maxPop
        
        Kopie = self.viruses[:]
        for b in Kopie:
            try:
                b.reproduce(popDensity, self.prescription)
                self.viruses.append(b)
                
            except NoChildException:
                continue



#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    # TODO
    import numpy as np
    
    daten = np.zeros(300)
    Daten = np.zeros(300)
    for a in range(numTrials):
        partikel = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
        Partikel = [partikel] * numViruses
        kranker = TreatedPatient(Partikel, maxPop)
        partikel_zaehlen, widerstand_zaehlen = [], []
        for b in range(150):
            kranker.update()
            partikel_zaehlen.append(kranker.getTotalPop())
            widerstand_zaehlen.append(kranker.getResistPop(['guttagonol']))
        kranker.addPrescription('guttagonol')
        for c in range(150):
            kranker.update()
            partikel_zaehlen.append(kranker.getTotalPop())
            widerstand_zaehlen.append(kranker.getResistPop(['guttagonol']))
        daten += partikel_zaehlen
        Daten += widerstand_zaehlen
    datendurchschnitt = daten / numTrials
    Datendurchschnitt = Daten / numTrials
    
    pylab.plot(datendurchschnitt, label = 'Non-resistant population')
    pylab.plot(Datendurchschnitt, label = 'Guttagonol Resistant population')
    pylab.xlabel('Number of steps')
    pylab.ylabel('Average Virus Population')
    pylab.title('Virus Simulation in Patient')
    pylab.legend()
    pylab.show()
 
# Test cases:  
simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)    
    
    
simulationWithDrug(numViruses = 100, maxPop = 1000, maxBirthProb = 0.2, clearProb = 0.05, resistances = {'guttagonol': False}, mutProb = 0.005, numTrials = 1)
#simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)
#simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
#simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
    
#simulationWithoutDrug(1, 10, 1.0, 0.0, 1)   
#simulationWithoutDrug(100, 200, 0.2, 0.8, 1)
#simulationWithoutDrug(1, 90, 0.8, 0.1, 1) 
#simulationWithoutDrug(1, 90, 0.8, 0.1, 1)    

