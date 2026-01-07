class Battery:
    """
    Represents a battery storage system with state of charge, efficiency, and degradation.
    """
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
        """
        Initialize the battery with given parameters.

        Args:
            capacity_kwh (float): Battery capacity in kWh.
            soc_init (float): Initial state of charge (0-1).
            eta_charge (float): Charging efficiency.
            eta_discharge (float): Discharging efficiency.
            soc_min (float): Minimum state of charge.
            soc_max (float): Maximum state of charge.
            p_charge_max (float): Maximum charging power in kW.
            p_discharge_max (float): Maximum discharging power in kW.
            battery_health_init (float): Initial battery health (0-1).
            temperature_init (float): Initial temperature in °C.
            degradation_rate (float): Degradation rate per cycle.
        """
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
        """
        Calculate the current energy stored in the battery.

        Returns:
            float: Energy in kWh.
        """
        return self.soc * self.capacity * self.health

    def step(self, p_charge, p_discharge, dt):
        """
        Simulate one time step of battery operation.

        Args:
            p_charge (float): Requested charging power in kW.
            p_discharge (float): Requested discharging power in kW.
            dt (float): Time step in hours.

        Returns:
            tuple: (actual_p_charge, actual_p_discharge, current_energy)
        """
        # Limit charging power to maximum allowed
        p_charge = min(p_charge, self.p_c_max)
        # Limit discharging power to maximum allowed
        p_discharge = min(p_discharge, self.p_d_max)

        # Calculate maximum possible discharge based on available energy and SOC limits
        max_possible_discharge = (self.energy - self.soc_min * self.capacity) * self.eta_d / dt
        p_discharge = max(0.0, min(p_discharge, max_possible_discharge))

        # Update energy: add charging energy, subtract discharging energy
        e = self.energy
        e += self.eta_c * p_charge * dt
        e -= (1 / self.eta_d) * p_discharge * dt

        # Update state of charge
        self.soc = e / self.capacity
        return p_charge, p_discharge, self.energy
