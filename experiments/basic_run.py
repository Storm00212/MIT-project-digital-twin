"""
Basic simulation run script.

This script sets up a simple energy system simulation with a battery and biogas generator,
runs it over predefined profiles, and plots the results.
"""

import sys
import os
# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from energy_model.battery import Battery
from energy_model.biogas import BiogasGenerator
from energy_model.simulator import EnergySimulator

# Initialize battery with 10 kWh capacity, initial SOC 0.4
battery = Battery(capacity_kwh=10.0, soc_init=0.4)
# Initialize biogas generator with default parameters
generator = BiogasGenerator()

# Create simulator with battery, generator, and 1-hour time steps
sim = EnergySimulator(battery, generator, dt=1.0)

# Define biogas flow profile: 0.8 for 10 steps, 0.3 for 10, 1.0 for 10
biogas_profile = np.array([0.8]*10 + [0.3]*10 + [1.0]*10)
# Constant load of 1.0 kW for 30 steps
load_profile = np.array([1.0]*30)

# Run the simulation using vectorized method
history = sim.run_vectorized(biogas_profile, load_profile)

# Plot the results
plt.figure()

plt.plot(history["battery_energy"], label="Battery Energy (kWh)")
plt.plot(history["generated_power"], label="Generated Power (kW)")
plt.plot(history["load_power"], label="Load Power (kW)")
plt.plot(history["unmet_load"], label="Unmet Load (kW)")

plt.xlabel("Time step")
plt.legend()
plt.grid(True)
plt.show()
