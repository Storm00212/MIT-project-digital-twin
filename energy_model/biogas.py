class BiogasGenerator:
    def __init__(
        self,
        energy_density_kwh_per_m3=1.7,
        efficiency=0.30
    ):
        self.rho = energy_density_kwh_per_m3
        self.eta = efficiency

    def power_output(self, biogas_flow_m3_per_hr):
        """
        Returns electrical power in kW
        """
        return self.eta * self.rho * biogas_flow_m3_per_hr
