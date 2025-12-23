class Battery:
    def __init__(
        self,
        capacity_kwh,
        soc_init=0.5,
        eta_charge=0.95,
        eta_discharge=0.95,
        soc_min=0.1,
        soc_max=0.9,
        p_charge_max=2.0,     # kW
        p_discharge_max=2.0,  # kW
        battery_health_init=1.0,
        temperature_init=25.0,  # °C
        degradation_rate=0.001  # per cycle
    ):
        self.capacity = capacity_kwh
        self.soc = soc_init
        self.eta_c = eta_charge
        self.eta_d = eta_discharge
        self.soc_min = soc_min
        self.soc_max = soc_max
        self.p_c_max = p_charge_max
        self.p_d_max = p_discharge_max
        self.health = battery_health_init
        self.temperature = temperature_init
        self.degradation_rate = degradation_rate

    @property
    def energy(self):
        return self.soc * self.capacity * self.health

    def step(self, p_charge, p_discharge, dt):
        # Adjust efficiencies based on temperature (simplified model)
        temp_factor = max(0.8, min(1.0, 1 - abs(self.temperature - 25) * 0.01))
        eta_c_eff = self.eta_c * temp_factor
        eta_d_eff = self.eta_d * temp_factor

        p_charge = min(p_charge, self.p_c_max)
        p_discharge = min(p_discharge, self.p_d_max)

        e = self.energy
        e += eta_c_eff * p_charge * dt
        e -= (1 / eta_d_eff) * p_discharge * dt

        e = max(self.soc_min * self.capacity * self.health,
                min(e, self.soc_max * self.capacity * self.health))

        self.soc = e / (self.capacity * self.health)

        # Update health and temperature (simplified)
        self.health = max(0.5, self.health - self.degradation_rate * (p_charge + p_discharge) * dt)
        self.temperature += 0.1 * (p_charge + p_discharge) * dt  # Heat up
        self.temperature = max(0, self.temperature - 0.05 * dt)  # Cool down

        return self.energy
