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
        # Power limits
        p_charge = min(p_charge, self.p_c_max)
        p_discharge = min(p_discharge, self.p_d_max)

        # Energy-availability constraint
        max_possible_discharge = (self.energy - self.soc_min * self.capacity) * self.eta_d / dt
        p_discharge = max(0.0, min(p_discharge, max_possible_discharge))

        e = self.energy
        e += self.eta_c * p_charge * dt
        e -= (1 / self.eta_d) * p_discharge * dt

        self.soc = e / self.capacity
        return p_charge, p_discharge, self.energy
