import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from energy_model.battery import Battery
from energy_model.biogas import BiogasGenerator
from energy_model.simulator import EnergySimulator

battery = Battery(capacity_kwh=10.0, soc_init=0.4)
generator = BiogasGenerator()

sim = EnergySimulator(battery, generator, dt=1.0)

biogas_profile = [0.8]*10 + [0.3]*10 + [1.0]*10
load_profile = [1.0]*30

history = sim.run(biogas_profile, load_profile)

plt.plot(history["battery_energy"], label="Battery Energy (kWh)")
plt.plot(history["generated_power"], label="Generated Power (kW)")
plt.plot(history["load_power"], label="Load Power (kW)")
plt.legend()
plt.xlabel("Time step")
plt.show()
