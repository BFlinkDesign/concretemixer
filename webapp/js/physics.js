/**
 * Concrete Mixer Physics Engine
 *
 * Implements Bingham plastic flow model for concrete rheology
 * and auger mechanics calculations.
 *
 * Based on simulation/auger_physics.py
 */

/**
 * Auger specifications (from DATA_REQUIREMENTS.md)
 */
const AugerSpecs = {
    outerDiameter: 4.0,          // inches
    innerDiameter: 0,            // shaftless
    housingID: 5.047,            // 5" Schedule 40
    housingOD: 5.563,
    clearance: 0.52,             // radial clearance
    length: 44,                  // active length inches

    // Variable pitch (P/D ratios)
    pitchRatios: {
        intake: 1.0,              // 4" pitch at intake
        transition: 0.75,         // 3" pitch middle
        mixing: 0.5               // 2" pitch at discharge
    },

    // Motor specs
    motorHP: 0.5,
    targetRPM: 27,
    gearRatio: 64,                // 1725 / 27

    // Material
    material: '304 Stainless Steel',
    thickness: 0.25               // flight thickness inches
};

/**
 * Water system specifications
 */
const WaterSpecs = {
    nozzleCount: 2,
    minPressurePSI: 30,
    recommendedPressurePSI: 40,
    nozzleCv: 0.5,                // Flow coefficient
    nozzleOrifice: 0.125,         // 1/8"
    sprayAngle: 65                // degrees
};

/**
 * Physics engine class
 */
class PhysicsEngine {
    constructor() {
        this.auger = { ...AugerSpecs };
        this.water = { ...WaterSpecs };

        // Operating state
        this.state = {
            rpm: 0,
            waterPressure: 40,
            waterDialSetting: 50,    // 0-100%
            materialLoaded: false,
            running: false
        };

        // Calculated values cache
        this.calculated = {};
    }

    // =========================================================================
    // BINGHAM PLASTIC MODEL
    // =========================================================================

    /**
     * Calculate apparent viscosity for Bingham plastic
     * @param {number} shearRate - Shear rate (1/s)
     * @param {number} yieldStress - Yield stress (Pa)
     * @param {number} plasticViscosity - Plastic viscosity (Pa·s)
     */
    apparentViscosity(shearRate, yieldStress, plasticViscosity) {
        if (shearRate < 0.01) return Infinity;
        return plasticViscosity + yieldStress / shearRate;
    }

    /**
     * Calculate shear stress
     * @param {number} shearRate - Shear rate (1/s)
     * @param {number} yieldStress - Yield stress (Pa)
     * @param {number} plasticViscosity - Plastic viscosity (Pa·s)
     */
    shearStress(shearRate, yieldStress, plasticViscosity) {
        if (shearRate < 0.01) return yieldStress;
        return yieldStress + plasticViscosity * shearRate;
    }

    /**
     * Calculate shear rate at auger surface
     * @param {number} rpm - Auger rotation speed
     */
    calculateShearRate(rpm) {
        const omega = rpm * 2 * Math.PI / 60;  // rad/s
        const radius = (this.auger.outerDiameter / 2) * 0.0254;  // m
        const gap = this.auger.clearance * 0.0254;  // m

        // Shear rate = v / gap
        const surfaceVelocity = omega * radius;
        return surfaceVelocity / gap;
    }

    // =========================================================================
    // TORQUE AND POWER
    // =========================================================================

    /**
     * Calculate required torque
     * @param {Object} materialProps - Material rheological properties
     * @param {number} rpm - Operating RPM
     * @returns {Object} Torque breakdown
     */
    calculateTorque(materialProps, rpm = this.state.rpm) {
        if (!materialProps || rpm <= 0) {
            return { total: 0, viscous: 0, friction: 0, acceleration: 0 };
        }

        const { yieldStress, plasticViscosity, density, frictionCoeff } = materialProps;

        // Convert dimensions to meters
        const D = this.auger.outerDiameter * 0.0254;
        const L = this.auger.length * 0.0254;
        const housingD = this.auger.housingID * 0.0254;

        // Angular velocity
        const omega = rpm * 2 * Math.PI / 60;

        // Average pitch (weighted)
        const avgPitch = D * 0.75;  // Average P/D ratio

        // Shear rate
        const shearRate = this.calculateShearRate(rpm);

        // Viscous torque (Bingham model)
        const tau = this.shearStress(shearRate, yieldStress, plasticViscosity);
        const surfaceArea = Math.PI * D * L;
        const viscousTorque = tau * surfaceArea * (D / 2);

        // Friction torque (material against housing)
        const materialWeight = density * Math.PI * (housingD/2)**2 * L * 0.5;  // Half fill
        const frictionTorque = frictionCoeff * materialWeight * 9.81 * (housingD / 2);

        // Acceleration torque (startup transient)
        const moment = density * Math.PI * (D/2)**4 * L / 2;
        const accelTorque = moment * (omega / 2);  // Assume 2 second ramp

        const totalTorque = viscousTorque + frictionTorque + accelTorque;

        return {
            total: totalTorque,
            viscous: viscousTorque,
            friction: frictionTorque,
            acceleration: accelTorque,
            shearRate: shearRate,
            shearStress: tau
        };
    }

    /**
     * Calculate required power
     * @param {Object} materialProps - Material properties
     * @param {number} rpm - Operating RPM
     * @returns {Object} Power calculations
     */
    calculatePower(materialProps, rpm = this.state.rpm) {
        const torque = this.calculateTorque(materialProps, rpm);
        const omega = rpm * 2 * Math.PI / 60;

        const powerWatts = torque.total * omega;
        const powerHP = powerWatts / 745.7;

        // Safety factor
        const safetyFactor = 1.25;
        const requiredHP = powerHP * safetyFactor;

        return {
            torqueNm: torque.total,
            torqueFtLb: torque.total * 0.7376,
            powerWatts: powerWatts,
            powerHP: powerHP,
            requiredHP: requiredHP,
            motorCapacity: (requiredHP / this.auger.motorHP) * 100,  // % of motor capacity
            breakdown: torque
        };
    }

    // =========================================================================
    // FLOW AND THROUGHPUT
    // =========================================================================

    /**
     * Calculate material flow rate
     * @param {Object} materialProps - Material properties
     * @param {number} rpm - Operating RPM
     * @returns {Object} Flow calculations
     */
    calculateFlowRate(materialProps, rpm = this.state.rpm) {
        if (!materialProps || rpm <= 0) {
            return { volumetric: 0, mass: 0, bagsPerHour: 0 };
        }

        // Auger dimensions in meters
        const D = this.auger.outerDiameter * 0.0254;
        const housingD = this.auger.housingID * 0.0254;

        // Average pitch
        const avgPitchRatio = 0.75;
        const pitch = D * avgPitchRatio;

        // Theoretical volumetric flow
        const annularArea = Math.PI * ((housingD/2)**2 - (D/2)**2 * 0.1);  // Accounting for flight
        const axialVelocity = pitch * rpm / 60;  // m/s

        // Volumetric efficiency (accounting for slip, fill factor)
        const fillFactor = 0.45;  // 45% fill typical
        const slipFactor = 0.85;  // 15% slip

        const volumetricFlow = annularArea * axialVelocity * fillFactor * slipFactor;  // m³/s
        const massFlow = volumetricFlow * materialProps.density;  // kg/s

        // Convert to bags per hour (assuming 80 lb bags = 36.3 kg)
        const bagsPerHour = (massFlow * 3600) / 36.3;

        return {
            volumetric: volumetricFlow,
            volumetricLPM: volumetricFlow * 60000,  // L/min
            volumetricCFM: volumetricFlow * 2118.88,  // CFM
            mass: massFlow,
            massKgMin: massFlow * 60,
            bagsPerHour: bagsPerHour,
            fillFactor: fillFactor,
            efficiency: slipFactor
        };
    }

    /**
     * Calculate residence time in mixing zone
     * @param {number} rpm - Operating RPM
     */
    calculateResidenceTime(rpm = this.state.rpm) {
        if (rpm <= 0) return 0;

        const D = this.auger.outerDiameter;  // inches
        const avgPitch = D * 0.75;            // Average P/D ratio
        const axialVelocity = avgPitch * rpm / 60;  // in/s
        return this.auger.length / axialVelocity;   // seconds
    }

    // =========================================================================
    // WATER SYSTEM
    // =========================================================================

    /**
     * Calculate water flow rate from nozzles
     * @param {number} pressure - Water pressure PSI
     * @param {number} dialSetting - Dial setting 0-100%
     */
    calculateWaterFlow(pressure = this.state.waterPressure, dialSetting = this.state.waterDialSetting) {
        // Flow per nozzle: Q = Cv * sqrt(P)
        const flowPerNozzle = this.water.nozzleCv * Math.sqrt(pressure);
        const totalMaxFlow = flowPerNozzle * this.water.nozzleCount;

        // Dial controls flow linearly
        const actualFlow = totalMaxFlow * (dialSetting / 100);

        return {
            maxFlowGPM: totalMaxFlow,
            actualFlowGPM: actualFlow,
            actualFlowLPM: actualFlow * 3.78541,
            perNozzleGPM: flowPerNozzle * (dialSetting / 100)
        };
    }

    /**
     * Calculate required water for given throughput
     * @param {Object} productData - Product data with water requirements
     * @param {number} bagsPerHour - Target throughput
     */
    calculateWaterRequirement(productData, bagsPerHour) {
        if (!productData) return null;

        const waterPerBag = productData.waterRequired;  // pints
        const gallonsPerBag = waterPerBag / 8;
        const requiredGPH = gallonsPerBag * bagsPerHour;
        const requiredGPM = requiredGPH / 60;

        return {
            waterPerBag: waterPerBag,
            requiredGPM: requiredGPM,
            requiredGPH: requiredGPH
        };
    }

    /**
     * Calculate optimal dial setting
     * @param {Object} productData - Product data
     * @param {number} bagsPerHour - Target throughput
     * @param {number} pressure - Water pressure
     */
    calculateOptimalDialSetting(productData, bagsPerHour, pressure = this.state.waterPressure) {
        const waterReq = this.calculateWaterRequirement(productData, bagsPerHour);
        const maxFlow = this.water.nozzleCv * Math.sqrt(pressure) * this.water.nozzleCount;

        const optimalSetting = (waterReq.requiredGPM / maxFlow) * 100;

        return {
            optimalSetting: Math.min(100, Math.max(0, optimalSetting)),
            requiredGPM: waterReq.requiredGPM,
            maxFlowGPM: maxFlow,
            achievable: optimalSetting <= 100
        };
    }

    /**
     * Calculate actual W/C ratio
     * @param {Object} materialProps - Material properties
     * @param {number} dialSetting - Water dial setting
     * @param {number} massFlowKgMin - Material mass flow kg/min
     */
    calculateActualWCRatio(materialProps, dialSetting, massFlowKgMin) {
        const waterFlow = this.calculateWaterFlow(this.state.waterPressure, dialSetting);
        const waterMassFlow = waterFlow.actualFlowLPM;  // L/min ≈ kg/min for water

        // Cement content of mix
        const cementMassFlow = massFlowKgMin * materialProps.cementContent;

        if (cementMassFlow <= 0) return 0;
        return waterMassFlow / cementMassFlow;
    }

    // =========================================================================
    // MIXING QUALITY
    // =========================================================================

    /**
     * Calculate mixing intensity index
     * @param {number} rpm - Operating RPM
     */
    calculateMixingIntensity(rpm = this.state.rpm) {
        // Based on shear events per second
        const fingerCount = 8;  // Mixing fingers in design
        const eventsPerSec = fingerCount * rpm / 60;

        // Normalize to 0-1 (100 events/sec = 1.0)
        return Math.min(1.0, eventsPerSec / 100);
    }

    /**
     * Calculate homogeneity index
     * @param {Object} materialProps - Material properties
     * @param {number} rpm - Operating RPM
     */
    calculateHomogeneity(materialProps, rpm = this.state.rpm) {
        if (!materialProps || rpm <= 0) return 0;

        const residenceTime = this.calculateResidenceTime(rpm);
        const mixingIntensity = this.calculateMixingIntensity(rpm);

        // Time factor (10 seconds for full mixing)
        const timeFactor = Math.min(1.0, residenceTime / 10);

        // Aggregate factor (smaller aggregates mix faster)
        const aggFactor = 1.0 - (materialProps.aggregateSize * 0.5);

        // Combined homogeneity
        const homogeneity = timeFactor * mixingIntensity * aggFactor * 0.95;

        return Math.min(1.0, homogeneity);
    }

    // =========================================================================
    // SIMULATION STATE
    // =========================================================================

    /**
     * Set operating RPM
     */
    setRPM(rpm) {
        this.state.rpm = Math.max(0, Math.min(rpm, this.auger.targetRPM * 1.1));
        this.state.running = rpm > 0;
    }

    /**
     * Set water pressure
     */
    setWaterPressure(psi) {
        this.state.waterPressure = Math.max(0, Math.min(psi, 80));
    }

    /**
     * Set water dial setting
     */
    setWaterDial(setting) {
        this.state.waterDialSetting = Math.max(0, Math.min(setting, 100));
    }

    /**
     * Run full simulation
     * @param {Object} productData - From ProductSelector.getCurrentSelection()
     * @returns {Object} Complete simulation results
     */
    simulate(productData) {
        if (!productData) {
            return this.getIdleState();
        }

        const materialProps = {
            yieldStress: productData.product.rheology.yieldStress,
            plasticViscosity: productData.product.rheology.plasticViscosity,
            density: productData.product.rheology.density,
            frictionCoeff: productData.product.rheology.frictionCoeff,
            aggregateSize: productData.product.specs.aggregateSize,
            cementContent: productData.product.specs.cementContent
        };

        const rpm = this.state.rpm;
        const power = this.calculatePower(materialProps, rpm);
        const flow = this.calculateFlowRate(materialProps, rpm);
        const waterFlow = this.calculateWaterFlow();
        const residenceTime = this.calculateResidenceTime(rpm);
        const mixingIntensity = this.calculateMixingIntensity(rpm);
        const homogeneity = this.calculateHomogeneity(materialProps, rpm);

        const optimalDial = this.calculateOptimalDialSetting(
            productData,
            flow.bagsPerHour,
            this.state.waterPressure
        );

        const actualWC = this.calculateActualWCRatio(
            materialProps,
            this.state.waterDialSetting,
            flow.massKgMin
        );

        return {
            // Operating state
            running: this.state.running,
            rpm: rpm,

            // Power
            torqueFtLb: power.torqueFtLb,
            powerHP: power.powerHP,
            motorLoad: power.motorCapacity,

            // Flow
            bagsPerHour: flow.bagsPerHour,
            massFlowKgMin: flow.massKgMin,
            volumetricLPM: flow.volumetricLPM,

            // Water
            waterFlowGPM: waterFlow.actualFlowGPM,
            waterPressure: this.state.waterPressure,
            waterDial: this.state.waterDialSetting,
            optimalWaterDial: optimalDial.optimalSetting,
            actualWCRatio: actualWC,
            targetWCRatio: productData.product.specs.wcRatio,

            // Mixing quality
            residenceTime: residenceTime,
            mixingIntensity: mixingIntensity,
            homogeneity: homogeneity,

            // Rheology
            shearRate: power.breakdown.shearRate,
            shearStress: power.breakdown.shearStress,

            // Material
            product: productData.product.name,
            brand: productData.brand,
            bagSize: productData.bagSize
        };
    }

    /**
     * Get idle state results
     */
    getIdleState() {
        return {
            running: false,
            rpm: 0,
            torqueFtLb: 0,
            powerHP: 0,
            motorLoad: 0,
            bagsPerHour: 0,
            massFlowKgMin: 0,
            volumetricLPM: 0,
            waterFlowGPM: 0,
            waterPressure: this.state.waterPressure,
            waterDial: this.state.waterDialSetting,
            optimalWaterDial: 0,
            actualWCRatio: 0,
            targetWCRatio: 0,
            residenceTime: 0,
            mixingIntensity: 0,
            homogeneity: 0,
            shearRate: 0,
            shearStress: 0,
            product: 'None',
            brand: '',
            bagSize: 0
        };
    }
}

// Export
window.AugerSpecs = AugerSpecs;
window.WaterSpecs = WaterSpecs;
window.PhysicsEngine = PhysicsEngine;
