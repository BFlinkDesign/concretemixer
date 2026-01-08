/**
 * Concrete Mixer Digital Twin - Main Application
 *
 * Integrates product selector, physics engine, and 3D viewer
 */

class MixerApp {
    constructor() {
        // Core components
        this.productSelector = new ProductSelector();
        this.physics = new PhysicsEngine();
        this.viewer = null;

        // UI state
        this.running = false;
        this.simResults = null;

        // Bind methods
        this.onProductChange = this.onProductChange.bind(this);
        this.updateSimulation = this.updateSimulation.bind(this);
    }

    /**
     * Initialize application
     */
    init() {
        // Initialize 3D viewer
        this.viewer = new MixerViewer('viewer-canvas');

        // Setup UI event listeners
        this.setupBrandSelector();
        this.setupProductCards();
        this.setupControls();
        this.setupMotorControls();

        // Register for product changes
        this.productSelector.addListener(this.onProductChange);

        // Initial state
        this.updateUI();

        // Start simulation loop
        this.startSimulationLoop();

        console.log('Concrete Mixer Digital Twin initialized');
    }

    // =========================================================================
    // BRAND & PRODUCT SELECTION
    // =========================================================================

    setupBrandSelector() {
        const brandBtns = document.querySelectorAll('.brand-btn');
        brandBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active state
                brandBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Select brand
                const brand = btn.dataset.brand;
                this.productSelector.selectBrand(brand);
                this.populateProducts();
            });
        });
    }

    populateProducts() {
        const grid = document.getElementById('product-grid');
        if (!grid) return;

        grid.innerHTML = '';
        const products = this.productSelector.getProducts();

        for (const [id, product] of Object.entries(products)) {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.dataset.productId = id;

            card.innerHTML = `
                <div class="product-name">${product.name}</div>
                <div class="product-specs">
                    <span>${product.specs.compressiveStrength} PSI</span>
                    <span>${product.specs.aggregateSize}" agg</span>
                </div>
                <div class="product-bags">
                    ${product.bagSizes.map(s => `<span class="bag-size">${s}lb</span>`).join('')}
                </div>
            `;

            card.addEventListener('click', () => {
                // Update selection
                document.querySelectorAll('.product-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                this.productSelector.selectProduct(id);
                this.updateBagSizeSelector(product);
            });

            grid.appendChild(card);
        }
    }

    setupProductCards() {
        // Initial population
        this.populateProducts();
    }

    updateBagSizeSelector(product) {
        const container = document.getElementById('bag-size-selector');
        if (!container) return;

        container.innerHTML = '';
        product.bagSizes.forEach(size => {
            const btn = document.createElement('button');
            btn.className = 'bag-btn' + (size === this.productSelector.currentBagSize ? ' active' : '');
            btn.textContent = `${size} lb`;
            btn.addEventListener('click', () => {
                container.querySelectorAll('.bag-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.productSelector.selectBagSize(size);
            });
            container.appendChild(btn);
        });
    }

    onProductChange(eventType, selection) {
        this.updateSimulation();
        this.updateProductDisplay();
    }

    updateProductDisplay() {
        const selection = this.productSelector.getCurrentSelection();
        const display = document.getElementById('selected-product-display');

        if (display && selection) {
            display.innerHTML = `
                <div class="selected-brand">${selection.brand}</div>
                <div class="selected-name">${selection.product.name}</div>
                <div class="selected-details">
                    ${selection.bagSize}lb bag | ${selection.waterRequired} pints water
                </div>
            `;
        }
    }

    // =========================================================================
    // CONTROLS
    // =========================================================================

    setupControls() {
        // Water dial
        const waterDial = document.getElementById('water-dial');
        const waterValue = document.getElementById('water-dial-value');
        if (waterDial) {
            waterDial.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                this.physics.setWaterDial(value);
                if (waterValue) waterValue.textContent = `${value}%`;
                this.updateSimulation();
            });
        }

        // Water pressure
        const pressureInput = document.getElementById('water-pressure');
        const pressureValue = document.getElementById('pressure-value');
        if (pressureInput) {
            pressureInput.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                this.physics.setWaterPressure(value);
                if (pressureValue) pressureValue.textContent = `${value} PSI`;
                this.updateSimulation();
            });
        }

        // Explode slider
        const explodeSlider = document.getElementById('explode-slider');
        const explodeValue = document.getElementById('explode-value');
        if (explodeSlider) {
            explodeSlider.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                this.viewer.setExplode(value);
                if (explodeValue) explodeValue.textContent = `${Math.round(value * 100)}%`;
            });
        }

        // Camera views
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.viewer.setCameraView(btn.dataset.view);
            });
        });
    }

    setupMotorControls() {
        // Start/Stop button
        const motorBtn = document.getElementById('motor-toggle');
        const motorStatus = document.getElementById('motor-status');
        const rpmDisplay = document.getElementById('rpm-display');

        if (motorBtn) {
            motorBtn.addEventListener('click', () => {
                this.running = !this.running;

                if (this.running) {
                    motorBtn.textContent = 'STOP';
                    motorBtn.classList.add('running');
                    if (motorStatus) motorStatus.textContent = 'RUNNING';
                    this.startMotor();
                } else {
                    motorBtn.textContent = 'START';
                    motorBtn.classList.remove('running');
                    if (motorStatus) motorStatus.textContent = 'STOPPED';
                    this.stopMotor();
                }
            });
        }

        // RPM adjustment
        const rpmSlider = document.getElementById('rpm-slider');
        if (rpmSlider) {
            rpmSlider.addEventListener('input', (e) => {
                const rpm = parseInt(e.target.value);
                if (this.running) {
                    this.physics.setRPM(rpm);
                    this.viewer.setRPM(rpm);
                    if (rpmDisplay) rpmDisplay.textContent = rpm;
                    this.updateSimulation();
                }
            });
        }
    }

    startMotor() {
        const targetRPM = parseInt(document.getElementById('rpm-slider')?.value || 27);
        let currentRPM = 0;

        // Ramp up animation
        const rampUp = setInterval(() => {
            currentRPM += 2;
            if (currentRPM >= targetRPM) {
                currentRPM = targetRPM;
                clearInterval(rampUp);
            }

            this.physics.setRPM(currentRPM);
            this.viewer.setRPM(currentRPM);
            const rpmDisplay = document.getElementById('rpm-display');
            if (rpmDisplay) rpmDisplay.textContent = currentRPM;
            this.updateSimulation();
        }, 50);
    }

    stopMotor() {
        let currentRPM = this.physics.state.rpm;

        // Ramp down animation
        const rampDown = setInterval(() => {
            currentRPM -= 3;
            if (currentRPM <= 0) {
                currentRPM = 0;
                clearInterval(rampDown);
            }

            this.physics.setRPM(currentRPM);
            this.viewer.setRPM(currentRPM);
            const rpmDisplay = document.getElementById('rpm-display');
            if (rpmDisplay) rpmDisplay.textContent = currentRPM;
            this.updateSimulation();
        }, 50);
    }

    // =========================================================================
    // SIMULATION
    // =========================================================================

    updateSimulation() {
        const selection = this.productSelector.getCurrentSelection();
        this.simResults = this.physics.simulate(selection);
        this.updateDisplays();
    }

    startSimulationLoop() {
        setInterval(() => {
            if (this.running) {
                this.updateSimulation();
            }
        }, 100);  // 10 Hz update
    }

    updateDisplays() {
        const r = this.simResults;
        if (!r) return;

        // Motor displays
        this.updateGauge('torque-gauge', r.torqueFtLb, 150);
        this.updateGauge('power-gauge', r.powerHP, 0.75);
        this.updateValue('motor-load', `${r.motorLoad.toFixed(1)}%`);

        // Flow displays
        this.updateValue('bags-per-hour', r.bagsPerHour.toFixed(1));
        this.updateValue('mass-flow', `${r.massFlowKgMin.toFixed(2)} kg/min`);

        // Water displays
        this.updateValue('water-flow', `${r.waterFlowGPM.toFixed(2)} GPM`);
        this.updateValue('wc-ratio', r.actualWCRatio.toFixed(3));
        this.updateValue('target-wc', r.targetWCRatio.toFixed(2));

        // Optimal dial indicator
        const optimalIndicator = document.getElementById('optimal-dial');
        if (optimalIndicator) {
            optimalIndicator.style.left = `${r.optimalWaterDial}%`;
            optimalIndicator.title = `Optimal: ${r.optimalWaterDial.toFixed(0)}%`;
        }

        // Mixing quality
        this.updateValue('residence-time', `${r.residenceTime.toFixed(1)}s`);
        this.updateValue('mix-intensity', `${(r.mixingIntensity * 100).toFixed(0)}%`);
        this.updateValue('homogeneity', `${(r.homogeneity * 100).toFixed(1)}%`);

        // Rheology
        this.updateValue('shear-rate', `${r.shearRate.toFixed(1)} /s`);
        this.updateValue('shear-stress', `${r.shearStress.toFixed(0)} Pa`);

        // Status bar
        this.updateStatusBar(r);
    }

    updateGauge(id, value, max) {
        const gauge = document.getElementById(id);
        if (gauge) {
            const percentage = Math.min(100, (value / max) * 100);
            const fill = gauge.querySelector('.gauge-fill');
            if (fill) {
                fill.style.width = `${percentage}%`;

                // Color based on percentage
                if (percentage > 90) {
                    fill.style.background = '#ff4444';
                } else if (percentage > 70) {
                    fill.style.background = '#ffaa00';
                } else {
                    fill.style.background = '#00cc66';
                }
            }

            const valueEl = gauge.querySelector('.gauge-value');
            if (valueEl) {
                valueEl.textContent = value.toFixed(1);
            }
        }
    }

    updateValue(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }

    updateStatusBar(results) {
        // Status indicators
        const motorIndicator = document.getElementById('status-motor');
        const waterIndicator = document.getElementById('status-water');
        const mixIndicator = document.getElementById('status-mix');

        if (motorIndicator) {
            motorIndicator.className = 'status-indicator ' + (results.running ? 'active' : 'inactive');
        }

        if (waterIndicator) {
            const waterActive = results.waterFlowGPM > 0.1;
            waterIndicator.className = 'status-indicator ' + (waterActive ? 'active' : 'inactive');
        }

        if (mixIndicator) {
            const mixGood = results.homogeneity > 0.8;
            const mixOk = results.homogeneity > 0.5;
            mixIndicator.className = 'status-indicator ' + (mixGood ? 'good' : mixOk ? 'warning' : 'inactive');
        }

        // W/C ratio indicator
        const wcIndicator = document.getElementById('status-wc');
        if (wcIndicator && results.targetWCRatio > 0) {
            const wcDiff = Math.abs(results.actualWCRatio - results.targetWCRatio);
            const wcGood = wcDiff < 0.05;
            const wcOk = wcDiff < 0.10;
            wcIndicator.className = 'status-indicator ' + (wcGood ? 'good' : wcOk ? 'warning' : 'error');
        }
    }

    // =========================================================================
    // UI UPDATES
    // =========================================================================

    updateUI() {
        // Set initial values
        const waterDial = document.getElementById('water-dial');
        const waterValue = document.getElementById('water-dial-value');
        if (waterDial) {
            waterDial.value = this.physics.state.waterDialSetting;
            if (waterValue) waterValue.textContent = `${this.physics.state.waterDialSetting}%`;
        }

        const pressureInput = document.getElementById('water-pressure');
        const pressureValue = document.getElementById('pressure-value');
        if (pressureInput) {
            pressureInput.value = this.physics.state.waterPressure;
            if (pressureValue) pressureValue.textContent = `${this.physics.state.waterPressure} PSI`;
        }

        // Initial simulation
        this.updateSimulation();
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new MixerApp();
    window.app.init();
});
