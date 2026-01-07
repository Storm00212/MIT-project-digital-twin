import numpy as np

class EnergySimulator:
    """
    Simulates energy system with battery and generator, tracking power flows and battery state.
    """
    def __init__(self, battery, generator, dt=1.0):
        """
        Initialize the energy simulator.

        Args:
            battery: Battery object.
            generator: Generator object (e.g., BiogasGenerator).
            dt (float): Time step in hours.
        """
        self.battery = battery
        self.generator = generator
        self.dt = dt

        # Initialize history dictionary to store simulation data
        self.history = {
            "time": [],
            "battery_energy": [],
            "generated_power": [],
            "load_power": [],
            "battery_soc": [],
            "battery_health": [],
            "battery_temperature": [],
            "unmet_load": []
        }

    def step(self, biogas_flow, load_power, t):
        """
        Perform one simulation step.

        Args:
            biogas_flow (float): Biogas flow rate in m³/hr.
            load_power (float): Load power demand in kW.
            t (int): Time step index.
        """
        # Calculate power generated from biogas
        p_gen = self.generator.power_output(biogas_flow)

        # Determine deficit (load > generation) or surplus (generation > load)
        deficit = max(0.0, load_power - p_gen)
        surplus = max(0.0, p_gen - load_power)

        # Request battery to charge with surplus or discharge for deficit
        p_charge_req = surplus
        p_discharge_req = deficit

        # Battery step: update battery state
        p_charge, p_discharge, _ = self.battery.step(
            p_charge_req,
            p_discharge_req,
            self.dt
        )

        # Total supplied power: generation + battery discharge
        supplied_power = p_gen + p_discharge
        # Unmet load if supplied < demanded
        unmet_load = max(0.0, load_power - supplied_power)

        # Record data in history
        self.history["time"].append(t)
        self.history["battery_energy"].append(self.battery.energy)
        self.history["battery_soc"].append(self.battery.soc)
        self.history["battery_health"].append(self.battery.health)
        self.history["battery_temperature"].append(self.battery.temperature)
        self.history["generated_power"].append(p_gen)
        self.history["load_power"].append(load_power)
        self.history["unmet_load"].append(unmet_load)

    def run(self, biogas_profile, load_profile):
        """
        Run the simulation over the given profiles.

        Args:
            biogas_profile (list): List of biogas flow rates.
            load_profile (list): List of load power demands.

        Returns:
            dict: Simulation history.
        """
        assert len(biogas_profile) == len(load_profile), "Profiles must have the same length"

        # Simulate each time step
        for t in range(len(biogas_profile)):
            self.step(
                biogas_flow=biogas_profile[t],
                load_power=load_profile[t],
                t=t
            )

        return self.history

    def run_vectorized(self, biogas_profile, load_profile):
        """
        Run the simulation in a vectorized manner using numpy for efficiency.

        Args:
            biogas_profile (np.ndarray): Array of biogas flow rates (m³/hr).
            load_profile (np.ndarray): Array of load power demands (kW).

        Returns:
            dict: Simulation history with numpy arrays.
        """
        assert len(biogas_profile) == len(load_profile), "Profiles must have the same length"

        T = len(biogas_profile)

        # Calculate generated power from biogas
        P_gen = np.array([self.generator.power_output(flow) for flow in biogas_profile])

        # Battery energy limits
        E_max = self.battery.soc_max * self.battery.capacity
        E_min = self.battery.soc_min * self.battery.capacity
        E_init = self.battery.energy

        # Initialize battery energy array
        E_batt = np.zeros(T)
        E_batt[0] = E_init

        # Initialize unmet load
        P_unmet = np.zeros(T)

        # Simulation loop (vectorized where possible)
        for t in range(1, T):
            P_net = P_gen[t] - load_profile[t]

            # CASE 1: Excess power → charge battery
            if P_net > 0:
                E_charge = P_net * self.dt * self.battery.eta_c
                E_batt[t] = min(E_batt[t-1] + E_charge, E_max)
            # CASE 2: Power deficit → discharge battery
            else:
                E_required = abs(P_net) * self.dt / self.battery.eta_d
                E_available = E_batt[t-1] - E_min

                if E_available >= E_required:
                    E_batt[t] = E_batt[t-1] - E_required
                else:
                    E_batt[t] = E_min
                    unmet_energy = E_required - E_available
                    P_unmet[t] = unmet_energy / self.dt

        # Update battery SOC
        soc_batt = E_batt / self.battery.capacity

        # Return history in similar format
        history = {
            "time": np.arange(T),
            "battery_energy": E_batt,
            "generated_power": P_gen,
            "load_power": load_profile,
            "battery_soc": soc_batt,
            "battery_health": np.full(T, self.battery.health),  # Assuming constant
            "battery_temperature": np.full(T, self.battery.temperature),  # Assuming constant
            "unmet_load": P_unmet
        }

        return history
