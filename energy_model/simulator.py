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
            "battery_soc": []
        }

    def step(self, biogas_flow, load_power, t):
        p_gen = self.generator.power_output(biogas_flow)

        if p_gen >= load_power:
            surplus = p_gen - load_power
            p_charge = surplus
            p_discharge = 0.0
        else:
            deficit = load_power - p_gen
            p_charge = 0.0
            p_discharge = deficit

        self.battery.step(
            p_charge=p_charge,
            p_discharge=p_discharge,
            dt=self.dt
        )

        self.history["time"].append(t)
        self.history["battery_energy"].append(self.battery.energy)
        self.history["battery_soc"].append(self.battery.soc)
        self.history["generated_power"].append(p_gen)
        self.history["load_power"].append(load_power)

    def run(self, biogas_profile, load_profile):
        assert len(biogas_profile) == len(load_profile)

        for t in range(len(biogas_profile)):
            self.step(
                biogas_flow=biogas_profile[t],
                load_power=load_profile[t],
                t=t
            )

        return self.history
