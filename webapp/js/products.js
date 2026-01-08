/**
 * Product Database and Selector
 *
 * Real specifications from Quikrete and Sakrete product lines
 * for use with the concrete mixer digital twin.
 */

const ProductDatabase = {
    // Quikrete Products
    quikrete: {
        brand: "Quikrete",
        products: {
            "concrete-mix": {
                name: "Concrete Mix",
                sku: "1101",
                description: "Original all-purpose concrete mix",
                bagSizes: [40, 50, 60, 80],
                specs: {
                    compressiveStrength: 4000,  // PSI @ 28 days
                    aggregateSize: 0.375,        // 3/8" max
                    cementContent: 0.15,         // 15% by weight
                    waterPerBag: {               // pints per bag size
                        40: 3.0,
                        50: 3.75,
                        60: 4.5,
                        80: 6.0
                    },
                    wcRatio: 0.50,
                    slump: 3.0,                  // inches
                    setTime: 6,                  // hours initial
                    cureTime: 28                 // days full strength
                },
                rheology: {
                    yieldStress: 250,            // Pa
                    plasticViscosity: 35,        // Pa·s
                    density: 2300,               // kg/m³
                    frictionCoeff: 0.45
                },
                color: "#8B8682"
            },
            "high-strength": {
                name: "5000 High Strength",
                sku: "1007",
                description: "High early strength concrete mix",
                bagSizes: [50, 80],
                specs: {
                    compressiveStrength: 5000,
                    aggregateSize: 0.375,
                    cementContent: 0.18,
                    waterPerBag: {
                        50: 3.5,
                        80: 5.5
                    },
                    wcRatio: 0.45,
                    slump: 2.5,
                    setTime: 4,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 300,
                    plasticViscosity: 42,
                    density: 2350,
                    frictionCoeff: 0.48
                },
                color: "#7A7672"
            },
            "fast-setting": {
                name: "Fast-Setting Concrete",
                sku: "1004",
                description: "Sets in 20-40 minutes",
                bagSizes: [50],
                specs: {
                    compressiveStrength: 4000,
                    aggregateSize: 0.375,
                    cementContent: 0.20,
                    waterPerBag: {
                        50: 2.5
                    },
                    wcRatio: 0.42,
                    slump: 2.0,
                    setTime: 0.5,
                    cureTime: 1
                },
                rheology: {
                    yieldStress: 280,
                    plasticViscosity: 38,
                    density: 2320,
                    frictionCoeff: 0.46
                },
                color: "#8A8580"
            },
            "mortar-mix": {
                name: "Mortar Mix",
                sku: "1102",
                description: "Type S mortar for masonry",
                bagSizes: [40, 60, 80],
                specs: {
                    compressiveStrength: 1800,
                    aggregateSize: 0.125,        // Fine sand only
                    cementContent: 0.12,
                    waterPerBag: {
                        40: 2.5,
                        60: 3.75,
                        80: 5.0
                    },
                    wcRatio: 0.55,
                    slump: 4.0,
                    setTime: 8,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 180,
                    plasticViscosity: 28,
                    density: 2100,
                    frictionCoeff: 0.40
                },
                color: "#9A9590"
            },
            "sand-mix": {
                name: "Sand/Topping Mix",
                sku: "1103",
                description: "Fine aggregate topping mix",
                bagSizes: [40, 60, 80],
                specs: {
                    compressiveStrength: 5000,
                    aggregateSize: 0.0625,       // Fine sand
                    cementContent: 0.22,
                    waterPerBag: {
                        40: 2.0,
                        60: 3.0,
                        80: 4.0
                    },
                    wcRatio: 0.48,
                    slump: 2.0,
                    setTime: 6,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 220,
                    plasticViscosity: 32,
                    density: 2200,
                    frictionCoeff: 0.42
                },
                color: "#A5A095"
            },
            "non-shrink-grout": {
                name: "Non-Shrink Grout",
                sku: "1585",
                description: "Precision non-shrink grout",
                bagSizes: [50],
                specs: {
                    compressiveStrength: 9500,
                    aggregateSize: 0.0625,
                    cementContent: 0.35,
                    waterPerBag: {
                        50: 3.75
                    },
                    wcRatio: 0.40,
                    slump: 6.0,                  // Flowable
                    setTime: 4,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 120,
                    plasticViscosity: 18,
                    density: 2400,
                    frictionCoeff: 0.35
                },
                color: "#6B6662"
            }
        }
    },

    // Sakrete Products
    sakrete: {
        brand: "Sakrete",
        products: {
            "concrete-mix": {
                name: "Concrete Mix",
                sku: "65200940",
                description: "All-purpose concrete mix",
                bagSizes: [40, 60, 80],
                specs: {
                    compressiveStrength: 4000,
                    aggregateSize: 0.50,         // 1/2" max
                    cementContent: 0.14,
                    waterPerBag: {
                        40: 3.0,
                        60: 4.5,
                        80: 6.0
                    },
                    wcRatio: 0.50,
                    slump: 3.0,
                    setTime: 6,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 260,
                    plasticViscosity: 36,
                    density: 2280,
                    frictionCoeff: 0.46
                },
                color: "#888480"
            },
            "high-strength": {
                name: "High Strength Concrete",
                sku: "65200390",
                description: "5000 PSI concrete mix",
                bagSizes: [60, 80],
                specs: {
                    compressiveStrength: 5000,
                    aggregateSize: 0.375,
                    cementContent: 0.17,
                    waterPerBag: {
                        60: 4.0,
                        80: 5.5
                    },
                    wcRatio: 0.45,
                    slump: 2.5,
                    setTime: 5,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 290,
                    plasticViscosity: 40,
                    density: 2340,
                    frictionCoeff: 0.47
                },
                color: "#787472"
            },
            "fast-setting": {
                name: "Fast Setting Concrete",
                sku: "65200074",
                description: "Sets in 30 minutes",
                bagSizes: [50],
                specs: {
                    compressiveStrength: 3000,
                    aggregateSize: 0.375,
                    cementContent: 0.19,
                    waterPerBag: {
                        50: 2.5
                    },
                    wcRatio: 0.42,
                    slump: 2.0,
                    setTime: 0.5,
                    cureTime: 1
                },
                rheology: {
                    yieldStress: 270,
                    plasticViscosity: 36,
                    density: 2300,
                    frictionCoeff: 0.45
                },
                color: "#898582"
            },
            "mortar-mix": {
                name: "Mortar Mix Type S",
                sku: "65300083",
                description: "Type S masonry mortar",
                bagSizes: [40, 60, 80],
                specs: {
                    compressiveStrength: 1800,
                    aggregateSize: 0.125,
                    cementContent: 0.13,
                    waterPerBag: {
                        40: 2.5,
                        60: 3.75,
                        80: 5.0
                    },
                    wcRatio: 0.55,
                    slump: 4.0,
                    setTime: 8,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 175,
                    plasticViscosity: 26,
                    density: 2080,
                    frictionCoeff: 0.39
                },
                color: "#9B9792"
            },
            "sand-mix": {
                name: "Sand Mix",
                sku: "65300036",
                description: "Multi-use sand mix",
                bagSizes: [40, 60],
                specs: {
                    compressiveStrength: 5000,
                    aggregateSize: 0.0625,
                    cementContent: 0.21,
                    waterPerBag: {
                        40: 2.0,
                        60: 3.0
                    },
                    wcRatio: 0.48,
                    slump: 2.0,
                    setTime: 6,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 215,
                    plasticViscosity: 30,
                    density: 2180,
                    frictionCoeff: 0.41
                },
                color: "#A8A49A"
            },
            "non-shrink-grout": {
                name: "Non-Shrink Construction Grout",
                sku: "65306065",
                description: "High-strength non-shrink grout",
                bagSizes: [50],
                specs: {
                    compressiveStrength: 8000,
                    aggregateSize: 0.0625,
                    cementContent: 0.32,
                    waterPerBag: {
                        50: 4.0
                    },
                    wcRatio: 0.42,
                    slump: 6.0,
                    setTime: 3,
                    cureTime: 28
                },
                rheology: {
                    yieldStress: 130,
                    plasticViscosity: 20,
                    density: 2380,
                    frictionCoeff: 0.36
                },
                color: "#6D6965"
            }
        }
    }
};

/**
 * Product Selector Controller
 */
class ProductSelector {
    constructor() {
        this.currentBrand = 'quikrete';
        this.currentProduct = null;
        this.currentBagSize = 80;
        this.listeners = [];
    }

    /**
     * Get all brands
     */
    getBrands() {
        return Object.keys(ProductDatabase);
    }

    /**
     * Get products for current brand
     */
    getProducts() {
        return ProductDatabase[this.currentBrand].products;
    }

    /**
     * Select brand
     */
    selectBrand(brand) {
        if (ProductDatabase[brand]) {
            this.currentBrand = brand;
            this.currentProduct = null;
            this.notifyListeners('brandChange');
        }
    }

    /**
     * Select product
     */
    selectProduct(productId) {
        const products = this.getProducts();
        if (products[productId]) {
            this.currentProduct = productId;
            // Set default bag size
            const product = products[productId];
            if (!product.bagSizes.includes(this.currentBagSize)) {
                this.currentBagSize = product.bagSizes[product.bagSizes.length - 1];
            }
            this.notifyListeners('productChange');
        }
    }

    /**
     * Select bag size
     */
    selectBagSize(size) {
        if (this.currentProduct) {
            const product = this.getProducts()[this.currentProduct];
            if (product.bagSizes.includes(size)) {
                this.currentBagSize = size;
                this.notifyListeners('bagSizeChange');
            }
        }
    }

    /**
     * Get current selection data
     */
    getCurrentSelection() {
        if (!this.currentProduct) return null;

        const product = this.getProducts()[this.currentProduct];
        return {
            brand: ProductDatabase[this.currentBrand].brand,
            brandId: this.currentBrand,
            productId: this.currentProduct,
            product: product,
            bagSize: this.currentBagSize,
            waterRequired: product.specs.waterPerBag[this.currentBagSize]
        };
    }

    /**
     * Get physics parameters for current selection
     */
    getPhysicsParams() {
        const selection = this.getCurrentSelection();
        if (!selection) return null;

        return {
            // Material properties
            yieldStress: selection.product.rheology.yieldStress,
            plasticViscosity: selection.product.rheology.plasticViscosity,
            density: selection.product.rheology.density,
            frictionCoeff: selection.product.rheology.frictionCoeff,

            // Mix properties
            aggregateSize: selection.product.specs.aggregateSize,
            wcRatio: selection.product.specs.wcRatio,
            cementContent: selection.product.specs.cementContent,

            // Per-bag data
            bagWeight: selection.bagSize,
            waterRequired: selection.waterRequired,

            // Calculated
            dryMassKg: selection.bagSize * 0.453592,  // lb to kg
            waterMassKg: (selection.waterRequired / 8) * 3.78541  // pints to kg
        };
    }

    /**
     * Register change listener
     */
    addListener(callback) {
        this.listeners.push(callback);
    }

    /**
     * Notify listeners
     */
    notifyListeners(eventType) {
        this.listeners.forEach(cb => cb(eventType, this.getCurrentSelection()));
    }
}

// Export
window.ProductDatabase = ProductDatabase;
window.ProductSelector = ProductSelector;
