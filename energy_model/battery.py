class Battery:
    def __init__(
        self,
        capacity_kwh,
        soc_init=0.5,
        eta_charge=0.95,
        eta_discharge=0.95,
        soc_min=0.1,
        soc_max=0.9
    ):
        self.capacity = capacity_kwh
        self.soc = soc_init
        self.eta_c = eta_charge
        self.eta_d = eta_discharge
        self.soc_min = soc_min
        self.soc_max = soc_max

    @property
    def energy(self):
        return self.soc * self.capacity

    def step(self, p_charge, p_discharge, dt):
        e = self.energy
        e += self.eta_c * p_charge * dt
        e -= (1 / self.eta_d) * p_discharge * dt

        e = max(self.soc_min * self.capacity,
                min(e, self.soc_max * self.capacity))

        self.soc = e / self.capacity
        return self.energy
