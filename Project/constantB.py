import log
import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt
import copy
from EMField import EMField
from ProtonBunch import ProtonBunch

field = EMField([500*10**3,0,0], [0,0,2.82], [-0.05,0.05]) 
protons = ProtonBunch(120*10**(6),1)

log.logger.info('Initial average kinetic energy: %s eV' % protons.KineticEnergy())
log.logger.info('Initial average momentum: %s kg m/s' % protons.momentum())
log.logger.info('Initial average position %s m' % protons.averagePosition())
log.logger.info('Initial bunch position spread: %s m' % protons.positionSpread())
log.logger.info('Initial bunch energy spread: %s eV' % protons.energySpread())

time, deltaT, duration = 0, 10**(-10), 2.78*10**(-8)

inital_bunch = copy.deepcopy(protons)

timeSeries = [0.]
Data = [inital_bunch]

log.logger.info('starting simulation')
while time <= duration:
    dt = protons.adaptiveStep(deltaT,field)
    time += dt
    timeSeries.append(time)
    field.getAcceleration(protons.bunch, time, dt)
    protons.update(dt,field,time,3)
    temp_bunch = copy.deepcopy(protons)
    Data.append(temp_bunch)

log.logger.info('simulation finished')
log.logger.info('building lists')

x,y = [],[]
for bunch in Data:
    x.append(bunch.averagePosition()[0])
    y.append(bunch.averagePosition()[1])

final = [x[-1], y[-1]]
magneticX, magneticY = np.meshgrid(list(range(-3,4,1)), list(range(-3,3,1)))

log.logger.info('Final average kinetic energy: %s eV' % protons.KineticEnergy())
log.logger.info('Final average momentum: %s kg m/s' % protons.momentum())
log.logger.info('Final average position %s m' % protons.averagePosition())
log.logger.info('Final bunch position spread: %s m' % protons.positionSpread())
log.logger.info('Final bunch energy spread: %s eV' % protons.energySpread())

log.logger.info('creating plots')

plt.figure('RK4 vs Exact')
plt.plot(x,y,label=protons.bunchName,color='blue')
plt.scatter(x,y,marker='.',color='red')
plt.axvspan(field.electricLowerBound, field.electricUpperBound, color='grey', alpha=0.5 ,zorder=1, label='Electric Field')
plt.scatter(final[0], final[1],color='blue')
plt.xlabel(r'x  position  [m]')
plt.ylabel(r'y  position [m]')
plt.legend(loc='upper left',framealpha=1)

plt.show()