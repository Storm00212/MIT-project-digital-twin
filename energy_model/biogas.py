class BiogasGenerator:
    """
    Represents a biogas generator that converts biogas flow to electrical power.
    """
    def __init__(
        self,
        energy_density_kwh_per_m3=1.7,
        efficiency=0.30
    ):
        """
        Initialize the biogas generator.

        Args:
            energy_density_kwh_per_m3 (float): Energy density of biogas in kWh per m³.
            efficiency (float): Conversion efficiency from biogas energy to electrical power.
        """
        self.rho = energy_density_kwh_per_m3
        self.eta = efficiency

    def power_output(self, biogas_flow_m3_per_hr):
        """
        Calculate the electrical power output from biogas flow.

        Args:
            biogas_flow_m3_per_hr (float): Biogas flow rate in m³ per hour.

        Returns:
            float: Electrical power output in kW.
        """
        return self.eta * self.rho * biogas_flow_m3_per_hr
