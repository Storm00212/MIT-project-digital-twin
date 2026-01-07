import numpy as np

class EnergySimulator:
    def __init__(self, battery, generator, dt=1.0):
        self.battery = battery
        self.generator = generator
        self.dt = dt

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
        p_gen = self.generator.power_output(biogas_flow)

        deficit = max(0.0, load_power - p_gen)
        surplus = max(0.0, p_gen - load_power)

        p_charge_req = surplus
        p_discharge_req = deficit

        p_charge, p_discharge, _ = self.battery.step(
            p_charge_req,
            p_discharge_req,
            self.dt
        )

        supplied_power = p_gen + p_discharge
        unmet_load = max(0.0, load_power - supplied_power)

        self.history["time"].append(t)
        self.history["battery_energy"].append(self.battery.energy)
        self.history["battery_soc"].append(self.battery.soc)
        self.history["battery_health"].append(self.battery.health)
        self.history["battery_temperature"].append(self.battery.temperature)
        self.history["generated_power"].append(p_gen)
        self.history["load_power"].append(load_power)
        self.history["unmet_load"].append(unmet_load)

    def run(self, biogas_profile, load_profile):
        assert len(biogas_profile) == len(load_profile)

        for t in range(len(biogas_profile)):
            self.step(
                biogas_flow=biogas_profile[t],
                load_power=load_profile[t],
                t=t
            )

        return self.history
