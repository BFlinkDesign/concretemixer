/**
 * Three.js 3D Viewer for Concrete Mixer Digital Twin
 *
 * Renders the complete mixer assembly with animation controls.
 */

class MixerViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;

        // Mixer parts
        this.parts = {
            housing: null,
            auger: null,
            hopper: null,
            frame: null,
            wheels: [],
            waterSystem: null,
            motor: null,
            chute: null
        };

        // Animation state
        this.animating = false;
        this.augerRotation = 0;
        this.rpm = 0;

        // Explode state
        this.explodeAmount = 0;

        // Colors (matching OpenSCAD models)
        this.colors = {
            housing: 0x4a4a50,
            auger: 0xa8a8b0,
            hopper: 0x3a3a40,
            frame: 0x333333,
            wheel: 0x1a1a1a,
            water: 0x4080c0,
            motor: 0x505055,
            concrete: 0x8B8682
        };

        this.init();
    }

    init() {
        // Scene setup
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1d23);

        // Camera
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 1000);
        this.camera.position.set(80, 40, 60);

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);

        // Orbit controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.target.set(0, 10, 0);

        // Lighting
        this.setupLighting();

        // Ground plane
        this.createGround();

        // Build mixer model
        this.buildMixer();

        // Handle resize
        window.addEventListener('resize', () => this.onResize());

        // Start render loop
        this.animate();
    }

    setupLighting() {
        // Ambient light
        const ambient = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambient);

        // Main directional light (sun)
        const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
        dirLight.position.set(50, 80, 30);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 2048;
        dirLight.shadow.mapSize.height = 2048;
        dirLight.shadow.camera.near = 0.5;
        dirLight.shadow.camera.far = 200;
        dirLight.shadow.camera.left = -60;
        dirLight.shadow.camera.right = 60;
        dirLight.shadow.camera.top = 60;
        dirLight.shadow.camera.bottom = -60;
        this.scene.add(dirLight);

        // Fill light
        const fillLight = new THREE.DirectionalLight(0x8090a0, 0.3);
        fillLight.position.set(-30, 20, -20);
        this.scene.add(fillLight);

        // Rim light
        const rimLight = new THREE.DirectionalLight(0xffffff, 0.2);
        rimLight.position.set(-20, 30, 50);
        this.scene.add(rimLight);
    }

    createGround() {
        // Ground plane
        const groundGeo = new THREE.PlaneGeometry(200, 200);
        const groundMat = new THREE.MeshStandardMaterial({
            color: 0x2a2d33,
            roughness: 0.9,
            metalness: 0.1
        });
        const ground = new THREE.Mesh(groundGeo, groundMat);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        this.scene.add(ground);

        // Grid
        const grid = new THREE.GridHelper(200, 40, 0x3a3d43, 0x2a2d33);
        grid.position.y = 0.01;
        this.scene.add(grid);
    }

    buildMixer() {
        // Create mixer group
        this.mixer = new THREE.Group();
        this.scene.add(this.mixer);

        // Build each component
        this.buildFrame();
        this.buildHousing();
        this.buildAuger();
        this.buildHopper();
        this.buildWheels();
        this.buildMotor();
        this.buildWaterSystem();
        this.buildChute();

        // Position mixer
        this.mixer.position.set(0, 8, 0);
    }

    buildFrame() {
        const frame = new THREE.Group();
        const tubeMat = new THREE.MeshStandardMaterial({
            color: this.colors.frame,
            roughness: 0.6,
            metalness: 0.8
        });

        // Main longitudinal rails
        const railGeo = new THREE.CylinderGeometry(0.5, 0.5, 55, 16);
        for (let y of [-10, 10]) {
            const rail = new THREE.Mesh(railGeo, tubeMat);
            rail.rotation.z = Math.PI / 2;
            rail.position.set(0, 0, y);
            rail.castShadow = true;
            frame.add(rail);
        }

        // Cross members
        const crossGeo = new THREE.CylinderGeometry(0.5, 0.5, 20, 16);
        for (let x of [-20, 0, 20]) {
            const cross = new THREE.Mesh(crossGeo, tubeMat);
            cross.position.set(x, 0, 0);
            cross.castShadow = true;
            frame.add(cross);
        }

        // Vertical supports
        const vertGeo = new THREE.CylinderGeometry(0.5, 0.5, 8, 16);
        for (let pos of [[-18, 5], [-18, -5], [15, 5], [15, -5]]) {
            const vert = new THREE.Mesh(vertGeo, tubeMat);
            vert.position.set(pos[0], 4, pos[1]);
            vert.castShadow = true;
            frame.add(vert);
        }

        // Upper rails (housing support)
        const upperGeo = new THREE.CylinderGeometry(0.5, 0.5, 45, 16);
        for (let y of [-4, 4]) {
            const upper = new THREE.Mesh(upperGeo, tubeMat);
            upper.rotation.z = Math.PI / 2;
            upper.position.set(-2, 8, y);
            upper.castShadow = true;
            frame.add(upper);
        }

        this.parts.frame = frame;
        this.mixer.add(frame);
    }

    buildHousing() {
        const housingGroup = new THREE.Group();

        // Main housing tube (Schedule 40 pipe)
        const housingGeo = new THREE.CylinderGeometry(2.78, 2.78, 50, 32);
        const housingMat = new THREE.MeshStandardMaterial({
            color: this.colors.housing,
            roughness: 0.4,
            metalness: 0.9
        });
        const housing = new THREE.Mesh(housingGeo, housingMat);
        housing.rotation.z = Math.PI / 2;
        housing.castShadow = true;
        housing.receiveShadow = true;
        housingGroup.add(housing);

        // End flanges
        const flangeGeo = new THREE.CylinderGeometry(3.5, 3.5, 0.5, 32);
        const flangeMat = new THREE.MeshStandardMaterial({
            color: 0x3a3a40,
            roughness: 0.5,
            metalness: 0.8
        });

        const flange1 = new THREE.Mesh(flangeGeo, flangeMat);
        flange1.rotation.z = Math.PI / 2;
        flange1.position.x = -25;
        flange1.castShadow = true;
        housingGroup.add(flange1);

        const flange2 = new THREE.Mesh(flangeGeo, flangeMat);
        flange2.rotation.z = Math.PI / 2;
        flange2.position.x = 25;
        flange2.castShadow = true;
        housingGroup.add(flange2);

        housingGroup.position.set(-2, 8, 0);

        this.parts.housing = housingGroup;
        this.mixer.add(housingGroup);
    }

    buildAuger() {
        const augerGroup = new THREE.Group();

        // Helical auger flight (simplified as segments)
        const augerMat = new THREE.MeshStandardMaterial({
            color: this.colors.auger,
            roughness: 0.3,
            metalness: 0.95,
            side: THREE.DoubleSide
        });

        // Create helix geometry
        const helixPath = new THREE.CurvePath();
        const segments = 60;
        const turns = 12;
        const radius = 2.0;
        const length = 44;

        // Build helix as torus segments
        for (let i = 0; i < segments; i++) {
            const t = i / segments;
            const angle = t * turns * Math.PI * 2;
            const x = -22 + t * length;

            // Auger flight segment
            const flightGeo = new THREE.TorusGeometry(radius, 0.12, 8, 16, Math.PI / 6);
            const flight = new THREE.Mesh(flightGeo, augerMat);
            flight.position.set(x, 0, 0);
            flight.rotation.x = angle;
            flight.rotation.y = Math.PI / 2;
            flight.castShadow = true;
            augerGroup.add(flight);
        }

        // Central ribbon (shaftless design)
        const ribbonGeo = new THREE.CylinderGeometry(0.3, 0.3, 44, 16);
        const ribbon = new THREE.Mesh(ribbonGeo, augerMat);
        ribbon.rotation.z = Math.PI / 2;
        ribbon.castShadow = true;
        augerGroup.add(ribbon);

        augerGroup.position.set(-2, 8, 0);

        this.parts.auger = augerGroup;
        this.mixer.add(augerGroup);
    }

    buildHopper() {
        const hopperGroup = new THREE.Group();

        // Hopper body (truncated pyramid)
        const hopperGeo = new THREE.CylinderGeometry(3, 6, 10, 4);
        const hopperMat = new THREE.MeshStandardMaterial({
            color: this.colors.hopper,
            roughness: 0.5,
            metalness: 0.8
        });
        const hopper = new THREE.Mesh(hopperGeo, hopperMat);
        hopper.rotation.y = Math.PI / 4;
        hopper.castShadow = true;
        hopperGroup.add(hopper);

        // Hopper rim
        const rimGeo = new THREE.TorusGeometry(6.5, 0.3, 8, 4);
        const rim = new THREE.Mesh(rimGeo, hopperMat);
        rim.rotation.y = Math.PI / 4;
        rim.position.y = 5;
        rim.castShadow = true;
        hopperGroup.add(rim);

        hopperGroup.position.set(-18, 18, 0);
        hopperGroup.rotation.x = Math.PI;

        this.parts.hopper = hopperGroup;
        this.mixer.add(hopperGroup);
    }

    buildWheels() {
        const wheelMat = new THREE.MeshStandardMaterial({
            color: this.colors.wheel,
            roughness: 0.9,
            metalness: 0.1
        });

        const wheelGeo = new THREE.TorusGeometry(5, 1.25, 16, 32);
        const hubGeo = new THREE.CylinderGeometry(1.5, 1.5, 2, 16);

        for (let z of [-12, 12]) {
            const wheelGroup = new THREE.Group();

            const wheel = new THREE.Mesh(wheelGeo, wheelMat);
            wheel.castShadow = true;
            wheelGroup.add(wheel);

            const hub = new THREE.Mesh(hubGeo, new THREE.MeshStandardMaterial({
                color: 0x555555,
                roughness: 0.5,
                metalness: 0.8
            }));
            hub.rotation.x = Math.PI / 2;
            wheelGroup.add(hub);

            wheelGroup.position.set(22, -3, z);
            wheelGroup.rotation.y = Math.PI / 2;

            this.parts.wheels.push(wheelGroup);
            this.mixer.add(wheelGroup);
        }

        // Axle
        const axleGeo = new THREE.CylinderGeometry(0.3, 0.3, 28, 16);
        const axleMat = new THREE.MeshStandardMaterial({
            color: 0x666666,
            roughness: 0.4,
            metalness: 0.9
        });
        const axle = new THREE.Mesh(axleGeo, axleMat);
        axle.position.set(22, -3, 0);
        axle.castShadow = true;
        this.mixer.add(axle);
    }

    buildMotor() {
        const motorGroup = new THREE.Group();

        // Motor housing
        const motorGeo = new THREE.CylinderGeometry(3, 3, 8, 32);
        const motorMat = new THREE.MeshStandardMaterial({
            color: this.colors.motor,
            roughness: 0.5,
            metalness: 0.7
        });
        const motor = new THREE.Mesh(motorGeo, motorMat);
        motor.rotation.z = Math.PI / 2;
        motor.castShadow = true;
        motorGroup.add(motor);

        // Mounting flange
        const flangeGeo = new THREE.CylinderGeometry(3.5, 3.5, 0.5, 32);
        const flange = new THREE.Mesh(flangeGeo, motorMat);
        flange.rotation.z = Math.PI / 2;
        flange.position.x = -4;
        flange.castShadow = true;
        motorGroup.add(flange);

        // Ventilation fins
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const finGeo = new THREE.BoxGeometry(6, 0.2, 0.5);
            const fin = new THREE.Mesh(finGeo, motorMat);
            fin.position.set(0, Math.sin(angle) * 3, Math.cos(angle) * 3);
            fin.rotation.x = angle;
            motorGroup.add(fin);
        }

        // Electrical box
        const boxGeo = new THREE.BoxGeometry(3, 4, 2);
        const box = new THREE.Mesh(boxGeo, new THREE.MeshStandardMaterial({
            color: 0x404045,
            roughness: 0.6,
            metalness: 0.5
        }));
        box.position.set(2, 4, 0);
        box.castShadow = true;
        motorGroup.add(box);

        motorGroup.position.set(27, 8, 0);

        this.parts.motor = motorGroup;
        this.mixer.add(motorGroup);
    }

    buildWaterSystem() {
        const waterGroup = new THREE.Group();

        const pipeMat = new THREE.MeshStandardMaterial({
            color: 0xb87333,  // Copper
            roughness: 0.3,
            metalness: 0.9
        });

        // Manifold
        const manifoldGeo = new THREE.CylinderGeometry(0.375, 0.375, 14, 16);
        const manifold = new THREE.Mesh(manifoldGeo, pipeMat);
        manifold.rotation.z = Math.PI / 2;
        manifold.position.set(-2, 0, 0);
        manifold.castShadow = true;
        waterGroup.add(manifold);

        // Nozzles
        const nozzleMat = new THREE.MeshStandardMaterial({
            color: 0xc9a227,  // Brass
            roughness: 0.4,
            metalness: 0.9
        });
        const nozzleGeo = new THREE.ConeGeometry(0.2, 0.75, 16);

        for (let x of [-7, 3]) {
            const nozzle = new THREE.Mesh(nozzleGeo, nozzleMat);
            nozzle.position.set(x, -0.5, 0);
            nozzle.rotation.x = Math.PI;
            nozzle.castShadow = true;
            waterGroup.add(nozzle);
        }

        // Valve
        const valveGeo = new THREE.SphereGeometry(0.75, 16, 16);
        const valve = new THREE.Mesh(valveGeo, nozzleMat);
        valve.position.set(6, 0, 0);
        valve.castShadow = true;
        waterGroup.add(valve);

        // Handle
        const handleGeo = new THREE.CylinderGeometry(0.1, 0.1, 2.5, 8);
        const handleMat = new THREE.MeshStandardMaterial({
            color: 0x333333,
            roughness: 0.7,
            metalness: 0.3
        });
        const handle = new THREE.Mesh(handleGeo, handleMat);
        handle.position.set(6, 1.5, 0);
        handle.rotation.z = Math.PI / 4;
        waterGroup.add(handle);

        // Inlet hose connector
        const inletGeo = new THREE.CylinderGeometry(0.5, 0.5, 1.5, 16);
        const inlet = new THREE.Mesh(inletGeo, nozzleMat);
        inlet.position.set(8, 0, 0);
        inlet.rotation.z = Math.PI / 2;
        inlet.castShadow = true;
        waterGroup.add(inlet);

        waterGroup.position.set(-2, 13, 5);

        this.parts.waterSystem = waterGroup;
        this.mixer.add(waterGroup);
    }

    buildChute() {
        const chuteGroup = new THREE.Group();

        const chuteMat = new THREE.MeshStandardMaterial({
            color: this.colors.housing,
            roughness: 0.4,
            metalness: 0.8,
            side: THREE.DoubleSide
        });

        // Main chute body (half pipe)
        const chuteGeo = new THREE.CylinderGeometry(2, 2.5, 12, 16, 1, true, 0, Math.PI);
        const chute = new THREE.Mesh(chuteGeo, chuteMat);
        chute.rotation.x = -Math.PI / 6;
        chute.rotation.z = Math.PI / 2;
        chute.position.set(-6, -2, 0);
        chute.castShadow = true;
        chuteGroup.add(chute);

        // Swivel ring
        const swivelGeo = new THREE.TorusGeometry(3, 0.3, 8, 32);
        const swivel = new THREE.Mesh(swivelGeo, chuteMat);
        swivel.rotation.y = Math.PI / 2;
        swivel.castShadow = true;
        chuteGroup.add(swivel);

        chuteGroup.position.set(-27, 8, 0);

        this.parts.chute = chuteGroup;
        this.mixer.add(chuteGroup);
    }

    // =========================================================================
    // ANIMATION AND CONTROL
    // =========================================================================

    setRPM(rpm) {
        this.rpm = rpm;
    }

    setExplode(amount) {
        this.explodeAmount = Math.max(0, Math.min(1, amount));
        this.updateExplode();
    }

    updateExplode() {
        const e = this.explodeAmount * 20;  // Max 20 units explosion

        if (this.parts.housing) {
            this.parts.housing.position.y = 8 + e * 0.5;
        }
        if (this.parts.auger) {
            this.parts.auger.position.y = 8 + e * 0.3;
            this.parts.auger.position.x = -2 - e * 0.2;
        }
        if (this.parts.hopper) {
            this.parts.hopper.position.y = 18 + e;
        }
        if (this.parts.motor) {
            this.parts.motor.position.x = 27 + e;
        }
        if (this.parts.waterSystem) {
            this.parts.waterSystem.position.z = 5 + e * 0.5;
            this.parts.waterSystem.position.y = 13 + e * 0.3;
        }
        if (this.parts.chute) {
            this.parts.chute.position.x = -27 - e * 0.5;
            this.parts.chute.position.y = 8 - e * 0.3;
        }
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // Rotate auger based on RPM
        if (this.parts.auger && this.rpm > 0) {
            this.augerRotation += (this.rpm / 60) * 0.1;  // Scale for visibility
            this.parts.auger.rotation.x = this.augerRotation;
        }

        // Update controls
        this.controls.update();

        // Render
        this.renderer.render(this.scene, this.camera);
    }

    onResize() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    // Camera presets
    setCameraView(view) {
        switch (view) {
            case 'front':
                this.camera.position.set(0, 15, 80);
                break;
            case 'side':
                this.camera.position.set(80, 15, 0);
                break;
            case 'top':
                this.camera.position.set(0, 80, 0);
                break;
            case 'iso':
            default:
                this.camera.position.set(60, 40, 60);
                break;
        }
        this.controls.target.set(0, 10, 0);
        this.controls.update();
    }
}

// Export
window.MixerViewer = MixerViewer;
