#!/usr/bin/env python3
"""
Concrete Mixer Auger Physics Simulation

This module provides physics-based simulation of the shaftless helical auger
concrete mixer, including:
- Material flow dynamics (Bingham plastic model for concrete)
- Torque and power calculations
- Throughput estimation
- Thermal analysis for continuous operation
- Particle-based aggregate simulation

Designed for bagged concrete mix products (Sakrete, Quikrete)
with maximum aggregate size of 1/2" (12.7mm)

Author: Claude Code
Date: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum
import json


# =============================================================================
# CONSTANTS AND SPECIFICATIONS
# =============================================================================

@dataclass
class AugerSpecs:
    """Auger design specifications from DATA_REQUIREMENTS.md"""
    outer_diameter: float = 4.0          # inches
    inner_diameter: float = 3.0          # inches (flight inner edge)
    flight_thickness: float = 0.1875     # inches (3/16")
    total_length: float = 48.0           # inches
    hopper_length: float = 24.0          # inches
    chute_length: float = 24.0           # inches
    pitch_hopper: float = 2.0            # inches (P/D = 0.5)
    pitch_chute: float = 3.5             # inches (P/D = 0.875)
    finger_count: int = 8
    finger_diameter: float = 0.375       # inches
    finger_length: float = 1.5           # inches


@dataclass
class HousingSpecs:
    """Housing/chute specifications"""
    outer_diameter: float = 5.563        # 5" Sch 40 pipe OD (inches)
    inner_diameter: float = 5.047        # 5" Sch 40 pipe ID (inches)
    length: float = 50.0                 # inches

    @property
    def clearance(self) -> float:
        """Clearance between auger and housing per side"""
        return (self.inner_diameter - 4.0) / 2  # Auger OD = 4"


@dataclass
class MotorSpecs:
    """Motor specifications"""
    power_hp: float = 0.5                # HP
    power_watts: float = 373.0           # Watts
    rpm: float = 27.0                    # Output RPM
    voltage: float = 120.0               # VAC input
    current: float = 2.6                 # Amps

    @property
    def torque_nm(self) -> float:
        """Calculate torque in N·m"""
        return self.power_watts / (2 * np.pi * self.rpm / 60)

    @property
    def torque_ftlb(self) -> float:
        """Calculate torque in ft-lb"""
        return self.torque_nm * 0.7376


class ConcreteType(Enum):
    """Bagged concrete product types"""
    STANDARD_MIX = "standard"        # Quikrete 1101, Sakrete Concrete Mix
    HIGH_STRENGTH = "high_strength"  # Quikrete 5000, Sakrete High-Strength
    FAST_SETTING = "fast_setting"    # Quikrete 1004, Sakrete Fast-Setting
    MORTAR = "mortar"                # Type S, Type N mortars
    SAND_MIX = "sand_mix"            # Topping/bedding mixes
    GROUT = "grout"                  # Non-shrink grouts


@dataclass
class ConcreteProperties:
    """Concrete rheological properties (Bingham plastic model)"""
    name: str
    density: float                    # kg/m³
    yield_stress: float               # Pa (τ₀)
    plastic_viscosity: float          # Pa·s (μ)
    max_aggregate_size: float         # inches
    water_per_80lb_bag: float         # pints
    working_time_minutes: float       # minutes
    strength_psi: float               # 28-day compressive strength

    @classmethod
    def get_properties(cls, concrete_type: ConcreteType) -> 'ConcreteProperties':
        """Get properties for a specific concrete type"""
        properties = {
            ConcreteType.STANDARD_MIX: cls(
                name="Standard Concrete Mix",
                density=2400,
                yield_stress=200,
                plastic_viscosity=30,
                max_aggregate_size=0.5,
                water_per_80lb_bag=6.0,
                working_time_minutes=60,
                strength_psi=4000
            ),
            ConcreteType.HIGH_STRENGTH: cls(
                name="High-Strength Concrete Mix",
                density=2450,
                yield_stress=250,
                plastic_viscosity=35,
                max_aggregate_size=0.5,
                water_per_80lb_bag=5.5,
                working_time_minutes=60,
                strength_psi=5000
            ),
            ConcreteType.FAST_SETTING: cls(
                name="Fast-Setting Concrete Mix",
                density=2400,
                yield_stress=300,
                plastic_viscosity=40,
                max_aggregate_size=0.375,
                water_per_80lb_bag=5.0,
                working_time_minutes=20,
                strength_psi=4000
            ),
            ConcreteType.MORTAR: cls(
                name="Mortar Mix (Type S)",
                density=2100,
                yield_stress=150,
                plastic_viscosity=20,
                max_aggregate_size=0.125,  # Fine sand only
                water_per_80lb_bag=5.0,
                working_time_minutes=90,
                strength_psi=1800
            ),
            ConcreteType.SAND_MIX: cls(
                name="Sand Mix",
                density=2200,
                yield_stress=180,
                plastic_viscosity=25,
                max_aggregate_size=0.0625,  # Very fine sand
                water_per_80lb_bag=4.0,
                working_time_minutes=60,
                strength_psi=5000
            ),
            ConcreteType.GROUT: cls(
                name="Non-Shrink Grout",
                density=2300,
                yield_stress=100,
                plastic_viscosity=15,
                max_aggregate_size=0.125,
                water_per_80lb_bag=3.75,
                working_time_minutes=30,
                strength_psi=7000
            ),
        }
        return properties[concrete_type]


# =============================================================================
# PHYSICS SIMULATION CLASSES
# =============================================================================

class AugerFlowSimulation:
    """
    Simulates material flow through the shaftless helical auger.

    Uses volumetric flow equations for screw conveyors with
    Bingham plastic fluid corrections for wet concrete.
    """

    def __init__(self, auger: AugerSpecs, housing: HousingSpecs,
                 motor: MotorSpecs, concrete_type: ConcreteType):
        self.auger = auger
        self.housing = housing
        self.motor = motor
        self.concrete = ConcreteProperties.get_properties(concrete_type)

        # Convert to SI units for calculations
        self.od_m = auger.outer_diameter * 0.0254
        self.id_m = auger.inner_diameter * 0.0254
        self.pitch_hopper_m = auger.pitch_hopper * 0.0254
        self.pitch_chute_m = auger.pitch_chute * 0.0254
        self.housing_id_m = housing.inner_diameter * 0.0254

    def calculate_volumetric_flow(self, fill_efficiency: float = 0.35) -> float:
        """
        Calculate volumetric flow rate (m³/s).

        For shaftless augers:
        Q = (π × D² × P × N × η) / 4

        Where:
            D = Inner diameter (material passage)
            P = Pitch
            N = RPM
            η = Fill efficiency (0.3-0.45 for inclined)
        """
        # Use average pitch
        avg_pitch = (self.pitch_hopper_m + self.pitch_chute_m) / 2

        # Flow area (annular for shaftless auger)
        flow_area = np.pi * (self.od_m**2 - self.id_m**2) / 4

        # Volumetric flow
        rps = self.motor.rpm / 60
        Q = flow_area * avg_pitch * rps * fill_efficiency

        return Q

    def calculate_mass_flow(self, fill_efficiency: float = 0.35) -> float:
        """Calculate mass flow rate (kg/s)"""
        Q = self.calculate_volumetric_flow(fill_efficiency)
        return Q * self.concrete.density

    def calculate_throughput_bags_per_hour(self, bag_weight_lb: float = 80) -> float:
        """Calculate throughput in bags per hour"""
        mass_flow_kg_s = self.calculate_mass_flow()
        mass_flow_lb_hr = mass_flow_kg_s * 2.205 * 3600
        return mass_flow_lb_hr / bag_weight_lb

    def calculate_shear_rate(self) -> float:
        """
        Calculate shear rate in the mixing zone (1/s).

        γ̇ = π × D × N / gap
        """
        clearance_m = (self.housing_id_m - self.od_m) / 2
        circumference = np.pi * self.od_m
        velocity = circumference * self.motor.rpm / 60

        return velocity / clearance_m

    def calculate_apparent_viscosity(self) -> float:
        """
        Calculate apparent viscosity using Bingham plastic model.

        μ_apparent = τ₀/γ̇ + μ_plastic
        """
        shear_rate = self.calculate_shear_rate()
        if shear_rate > 0:
            return self.concrete.yield_stress / shear_rate + self.concrete.plastic_viscosity
        return self.concrete.plastic_viscosity

    def calculate_required_torque(self) -> Tuple[float, float]:
        """
        Calculate required torque (N·m) and power (W).

        Includes:
        - Material conveying torque
        - Viscous shear torque
        - Friction losses
        """
        # Material weight torque (gravity component for inclined operation)
        mass_in_auger = self.calculate_mass_flow() * (self.auger.total_length * 0.0254 / 0.5)  # ~residence time
        gravity_torque = mass_in_auger * 9.81 * (self.od_m / 2) * np.sin(np.radians(15))  # 15° incline

        # Shear torque (Bingham fluid)
        shear_rate = self.calculate_shear_rate()
        shear_stress = self.concrete.yield_stress + self.concrete.plastic_viscosity * shear_rate

        # Shear area (auger surface)
        auger_length_m = self.auger.total_length * 0.0254
        shear_area = np.pi * self.od_m * auger_length_m

        shear_force = shear_stress * shear_area
        shear_torque = shear_force * (self.od_m / 2)

        # Friction factor (bearing + seal losses)
        friction_torque = 5.0  # N·m estimated

        total_torque = gravity_torque + shear_torque + friction_torque

        # Required power
        angular_velocity = 2 * np.pi * self.motor.rpm / 60
        required_power = total_torque * angular_velocity

        return total_torque, required_power

    def check_motor_adequacy(self) -> dict:
        """Check if motor is adequate for the application"""
        required_torque, required_power = self.calculate_required_torque()
        available_torque = self.motor.torque_nm
        available_power = self.motor.power_watts

        return {
            "required_torque_nm": required_torque,
            "available_torque_nm": available_torque,
            "torque_margin": (available_torque - required_torque) / available_torque * 100,
            "required_power_w": required_power,
            "available_power_w": available_power,
            "power_margin": (available_power - required_power) / available_power * 100,
            "adequate": required_torque < available_torque and required_power < available_power
        }


class ThermalSimulation:
    """
    Thermal analysis for continuous operation duty cycle.

    Models heat generation from:
    - Motor losses
    - Friction between auger and concrete
    - Viscous dissipation in concrete
    """

    def __init__(self, flow_sim: AugerFlowSimulation):
        self.flow_sim = flow_sim

    def calculate_heat_generation(self) -> dict:
        """Calculate heat sources (W)"""
        # Motor efficiency losses (assuming 80% efficient)
        motor_efficiency = 0.80
        motor_heat = self.flow_sim.motor.power_watts * (1 - motor_efficiency)

        # Viscous dissipation
        shear_rate = self.flow_sim.calculate_shear_rate()
        apparent_viscosity = self.flow_sim.calculate_apparent_viscosity()

        # Dissipation = μ × γ̇² × Volume
        clearance_m = (self.flow_sim.housing_id_m - self.flow_sim.od_m) / 2
        auger_length_m = self.flow_sim.auger.total_length * 0.0254
        shear_volume = np.pi * self.flow_sim.od_m * auger_length_m * clearance_m

        viscous_heat = apparent_viscosity * shear_rate**2 * shear_volume

        # Friction heat (mechanical)
        _, required_power = self.flow_sim.calculate_required_torque()
        friction_heat = required_power * 0.1  # ~10% of power to friction

        return {
            "motor_heat_w": motor_heat,
            "viscous_heat_w": viscous_heat,
            "friction_heat_w": friction_heat,
            "total_heat_w": motor_heat + viscous_heat + friction_heat
        }

    def estimate_temperature_rise(self, ambient_temp_c: float = 25,
                                   operation_hours: float = 1.0) -> float:
        """
        Estimate temperature rise during operation.

        Simplified lumped-capacitance model.
        """
        heat_gen = self.calculate_heat_generation()

        # Thermal mass (steel + concrete)
        steel_mass = 20  # kg estimated
        concrete_mass = self.flow_sim.calculate_mass_flow() * 60  # 1 minute residence

        steel_cp = 500   # J/(kg·K)
        concrete_cp = 880  # J/(kg·K)

        thermal_mass = steel_mass * steel_cp + concrete_mass * concrete_cp

        # Heat dissipation (natural convection)
        surface_area = 0.5  # m² estimated
        h_conv = 10  # W/(m²·K) natural convection

        # Steady-state temperature rise
        Q_gen = heat_gen["total_heat_w"]
        delta_T = Q_gen / (h_conv * surface_area)

        return ambient_temp_c + delta_T


class ParticleSimulation:
    """
    Discrete Element Method (DEM) style particle simulation
    for aggregate behavior in the auger.
    """

    def __init__(self, auger: AugerSpecs, housing: HousingSpecs,
                 num_particles: int = 100):
        self.auger = auger
        self.housing = housing
        self.num_particles = num_particles
        self.particles: List[dict] = []

        self._initialize_particles()

    def _initialize_particles(self):
        """Initialize particles with random positions and sizes"""
        np.random.seed(42)

        for i in range(self.num_particles):
            # Random size between 0.125" and 0.5" (aggregate range)
            size = np.random.uniform(0.125, 0.5)

            # Random position in hopper
            r = np.random.uniform(0, self.housing.inner_diameter / 2 - size)
            theta = np.random.uniform(0, 2 * np.pi)
            z = np.random.uniform(0, 10)  # In hopper

            self.particles.append({
                "id": i,
                "size": size,
                "x": r * np.cos(theta),
                "y": r * np.sin(theta),
                "z": z,
                "vx": 0, "vy": 0, "vz": 0,
                "in_system": True
            })

    def step(self, dt: float, auger_rpm: float):
        """
        Advance simulation by one time step.

        Simplified physics:
        - Gravity
        - Auger conveying (drag with auger motion)
        - Wall collisions
        """
        auger_angular_vel = 2 * np.pi * auger_rpm / 60

        for p in self.particles:
            if not p["in_system"]:
                continue

            r = np.sqrt(p["x"]**2 + p["y"]**2)

            # Gravity
            p["vz"] -= 386.4 * dt  # in/s² to in/s

            # Auger drag (simplified)
            if r < self.auger.outer_diameter / 2:
                # Particle being conveyed
                tangential_vel = auger_angular_vel * r

                # Add axial velocity from auger pitch
                avg_pitch = (self.auger.pitch_hopper + self.auger.pitch_chute) / 2
                axial_vel = avg_pitch * auger_rpm / 60

                p["vz"] += axial_vel * dt * 10  # Drag coefficient
                p["vx"] += (tangential_vel * np.sin(np.arctan2(p["y"], p["x"]))) * dt
                p["vy"] -= (tangential_vel * np.cos(np.arctan2(p["y"], p["x"]))) * dt

            # Update position
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["z"] += p["vz"] * dt

            # Wall collisions
            r_new = np.sqrt(p["x"]**2 + p["y"]**2)
            max_r = (self.housing.inner_diameter - p["size"]) / 2

            if r_new > max_r:
                # Reflect velocity
                normal = np.array([p["x"], p["y"]]) / r_new
                vel_normal = p["vx"] * normal[0] + p["vy"] * normal[1]
                p["vx"] -= 1.8 * vel_normal * normal[0]  # Coefficient of restitution
                p["vy"] -= 1.8 * vel_normal * normal[1]

                # Move inside
                p["x"] = max_r * normal[0]
                p["y"] = max_r * normal[1]

            # Check if discharged
            if p["z"] > self.auger.total_length:
                p["in_system"] = False

            # Floor
            if p["z"] < 0:
                p["z"] = 0
                p["vz"] = abs(p["vz"]) * 0.3

    def get_particle_positions(self) -> np.ndarray:
        """Get current particle positions as numpy array"""
        active = [p for p in self.particles if p["in_system"]]
        if not active:
            return np.array([]).reshape(0, 3)
        return np.array([[p["x"], p["y"], p["z"]] for p in active])


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_simulation_results(flow_sim: AugerFlowSimulation):
    """Generate visualization of simulation results"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Concrete Mixer Auger Physics Simulation", fontsize=14, fontweight='bold')

    # 1. Throughput vs Fill Efficiency
    ax1 = axes[0, 0]
    fill_efficiencies = np.linspace(0.2, 0.5, 50)
    throughputs = [flow_sim.calculate_throughput_bags_per_hour(80)
                   for _ in fill_efficiencies]

    # Recalculate for each efficiency
    throughputs = []
    for eta in fill_efficiencies:
        mass_flow = flow_sim.calculate_volumetric_flow(eta) * flow_sim.concrete.density
        throughputs.append(mass_flow * 2.205 * 3600 / 80)

    ax1.plot(fill_efficiencies * 100, throughputs, 'b-', linewidth=2)
    ax1.axhline(y=45, color='r', linestyle='--', label='Target: 45 bags/hr')
    ax1.axvline(x=35, color='g', linestyle='--', label='Typical η=35%')
    ax1.set_xlabel('Fill Efficiency (%)')
    ax1.set_ylabel('Throughput (80-lb bags/hr)')
    ax1.set_title('Throughput vs Fill Efficiency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Torque/Power Analysis
    ax2 = axes[0, 1]
    motor_check = flow_sim.check_motor_adequacy()

    categories = ['Torque (N·m)', 'Power (W)']
    required = [motor_check['required_torque_nm'], motor_check['required_power_w']]
    available = [motor_check['available_torque_nm'], motor_check['available_power_w']]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax2.bar(x - width/2, required, width, label='Required', color='orange')
    bars2 = ax2.bar(x + width/2, available, width, label='Available', color='green')

    ax2.set_ylabel('Value')
    ax2.set_title('Motor Torque & Power Analysis')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    # Add margin percentages
    for i, (req, avail) in enumerate(zip(required, available)):
        margin = (avail - req) / avail * 100
        ax2.annotate(f'+{margin:.1f}%', xy=(i, max(req, avail)),
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

    # 3. Shear Rate Profile
    ax3 = axes[1, 0]
    rpms = np.linspace(10, 50, 50)
    shear_rates = []
    for rpm in rpms:
        clearance_m = (flow_sim.housing_id_m - flow_sim.od_m) / 2
        circumference = np.pi * flow_sim.od_m
        velocity = circumference * rpm / 60
        shear_rates.append(velocity / clearance_m)

    ax3.plot(rpms, shear_rates, 'b-', linewidth=2)
    ax3.axvline(x=27, color='r', linestyle='--', label='Operating RPM: 27')
    ax3.set_xlabel('Auger RPM')
    ax3.set_ylabel('Shear Rate (1/s)')
    ax3.set_title('Shear Rate vs Auger Speed')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. Concrete Type Comparison
    ax4 = axes[1, 1]
    concrete_types = list(ConcreteType)
    viscosities = []
    yields = []
    names = []

    for ct in concrete_types:
        props = ConcreteProperties.get_properties(ct)
        viscosities.append(props.plastic_viscosity)
        yields.append(props.yield_stress)
        names.append(props.name.replace(' Mix', '').replace(' Concrete', ''))

    x = np.arange(len(names))
    width = 0.35

    ax4_twin = ax4.twinx()
    bars1 = ax4.bar(x - width/2, yields, width, label='Yield Stress (Pa)', color='steelblue')
    bars2 = ax4_twin.bar(x + width/2, viscosities, width, label='Viscosity (Pa·s)', color='coral')

    ax4.set_ylabel('Yield Stress (Pa)', color='steelblue')
    ax4_twin.set_ylabel('Plastic Viscosity (Pa·s)', color='coral')
    ax4.set_title('Concrete Product Rheological Properties')
    ax4.set_xticks(x)
    ax4.set_xticklabels(names, rotation=45, ha='right')

    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    plt.tight_layout()
    return fig


def plot_particle_simulation(particle_sim: ParticleSimulation, steps: int = 100):
    """Animate particle simulation"""
    fig = plt.figure(figsize=(12, 5))

    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122)

    particle_counts = []

    for step in range(steps):
        particle_sim.step(dt=0.01, auger_rpm=27)

        positions = particle_sim.get_particle_positions()
        particle_counts.append(len(positions))

        if step == steps - 1:  # Final frame
            if len(positions) > 0:
                ax1.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                           c=positions[:, 2], cmap='viridis', s=50, alpha=0.6)

            # Draw auger outline
            theta = np.linspace(0, 2*np.pi, 50)
            z_line = np.linspace(0, particle_sim.auger.total_length, 50)

            for z in [0, particle_sim.auger.total_length]:
                ax1.plot(particle_sim.auger.outer_diameter/2 * np.cos(theta),
                        particle_sim.auger.outer_diameter/2 * np.sin(theta),
                        [z] * len(theta), 'r-', alpha=0.3)

    ax1.set_xlabel('X (inches)')
    ax1.set_ylabel('Y (inches)')
    ax1.set_zlabel('Z (inches)')
    ax1.set_title('Particle Positions (Final Frame)')

    ax2.plot(particle_counts, 'b-', linewidth=2)
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('Particles in System')
    ax2.set_title('Particle Count Over Time')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


# =============================================================================
# MAIN SIMULATION RUNNER
# =============================================================================

def run_full_simulation(concrete_type: ConcreteType = ConcreteType.STANDARD_MIX,
                        save_plots: bool = True,
                        output_dir: str = "."):
    """
    Run complete physics simulation and generate report.
    """
    print("=" * 60)
    print("CONCRETE MIXER AUGER PHYSICS SIMULATION")
    print("=" * 60)

    # Initialize specifications
    auger = AugerSpecs()
    housing = HousingSpecs()
    motor = MotorSpecs()

    print(f"\n[1] Specifications:")
    print(f"    Auger OD: {auger.outer_diameter}\" | Housing ID: {housing.inner_diameter}\"")
    print(f"    Clearance: {housing.clearance:.3f}\" per side")
    print(f"    Motor: {motor.power_hp} HP @ {motor.rpm} RPM")
    print(f"    Torque: {motor.torque_nm:.1f} N·m ({motor.torque_ftlb:.1f} ft-lb)")

    # Flow simulation
    print(f"\n[2] Flow Simulation ({concrete_type.value}):")
    flow_sim = AugerFlowSimulation(auger, housing, motor, concrete_type)
    concrete = flow_sim.concrete

    print(f"    Concrete: {concrete.name}")
    print(f"    Density: {concrete.density} kg/m³")
    print(f"    Max Aggregate: {concrete.max_aggregate_size}\"")

    vol_flow = flow_sim.calculate_volumetric_flow()
    mass_flow = flow_sim.calculate_mass_flow()
    throughput = flow_sim.calculate_throughput_bags_per_hour()

    print(f"\n    Volumetric Flow: {vol_flow*1e6:.2f} cm³/s")
    print(f"    Mass Flow: {mass_flow:.3f} kg/s ({mass_flow*2.205*60:.1f} lb/min)")
    print(f"    Throughput: {throughput:.1f} bags/hr (80 lb bags)")

    # Motor adequacy check
    print(f"\n[3] Motor Analysis:")
    motor_check = flow_sim.check_motor_adequacy()
    print(f"    Required Torque: {motor_check['required_torque_nm']:.1f} N·m")
    print(f"    Available Torque: {motor_check['available_torque_nm']:.1f} N·m")
    print(f"    Torque Margin: {motor_check['torque_margin']:.1f}%")
    print(f"    Motor Adequate: {'YES ✓' if motor_check['adequate'] else 'NO ✗'}")

    # Thermal analysis
    print(f"\n[4] Thermal Analysis:")
    thermal_sim = ThermalSimulation(flow_sim)
    heat = thermal_sim.calculate_heat_generation()
    temp_rise = thermal_sim.estimate_temperature_rise()

    print(f"    Motor Heat: {heat['motor_heat_w']:.1f} W")
    print(f"    Viscous Dissipation: {heat['viscous_heat_w']:.1f} W")
    print(f"    Total Heat: {heat['total_heat_w']:.1f} W")
    print(f"    Estimated Temp Rise: {temp_rise - 25:.1f}°C above ambient")

    # Shear analysis
    print(f"\n[5] Shear Analysis:")
    shear_rate = flow_sim.calculate_shear_rate()
    apparent_visc = flow_sim.calculate_apparent_viscosity()

    print(f"    Shear Rate: {shear_rate:.1f} 1/s")
    print(f"    Apparent Viscosity: {apparent_visc:.1f} Pa·s")
    print(f"    Yield Stress: {concrete.yield_stress} Pa")

    # Generate plots
    if save_plots:
        print(f"\n[6] Generating Plots...")
        fig1 = plot_simulation_results(flow_sim)
        fig1.savefig(f"{output_dir}/simulation_results.png", dpi=150, bbox_inches='tight')
        print(f"    Saved: simulation_results.png")

        # Particle simulation
        print(f"\n[7] Running Particle Simulation...")
        particle_sim = ParticleSimulation(auger, housing, num_particles=50)
        fig2 = plot_particle_simulation(particle_sim, steps=200)
        fig2.savefig(f"{output_dir}/particle_simulation.png", dpi=150, bbox_inches='tight')
        print(f"    Saved: particle_simulation.png")

        plt.close('all')

    # Summary
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)

    return {
        "throughput_bags_per_hour": throughput,
        "motor_adequate": motor_check['adequate'],
        "torque_margin_percent": motor_check['torque_margin'],
        "temperature_rise_c": temp_rise - 25,
        "shear_rate": shear_rate
    }


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import sys

    # Run simulation for all concrete types
    results = {}

    for ct in ConcreteType:
        print(f"\n{'#' * 60}")
        print(f"# Testing: {ct.value}")
        print(f"{'#' * 60}")

        results[ct.value] = run_full_simulation(
            concrete_type=ct,
            save_plots=(ct == ConcreteType.STANDARD_MIX),  # Only save plots for standard
            output_dir="/home/user/concretemixer/simulation"
        )

    # Print comparison summary
    print("\n\n" + "=" * 70)
    print("COMPARISON SUMMARY - ALL CONCRETE TYPES")
    print("=" * 70)
    print(f"{'Type':<20} {'Throughput':>12} {'Torque Margin':>15} {'Temp Rise':>12}")
    print("-" * 70)
    for name, data in results.items():
        print(f"{name:<20} {data['throughput_bags_per_hour']:>10.1f} b/h "
              f"{data['torque_margin_percent']:>12.1f}% "
              f"{data['temperature_rise_c']:>10.1f}°C")
