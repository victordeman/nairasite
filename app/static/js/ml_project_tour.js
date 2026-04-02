import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

class MLProjectTour {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.onStepChange = options.onStepChange || (() => {});
        this.currentStep = -1;
        this.isTouring = false;

        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, this.container.clientWidth / this.container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.container.appendChild(this.renderer.domElement);

        this.camera.position.set(0, 10, 20);

        this.components = [];
        this.steps = [
            {
                title: "Data Ingestion",
                text: "The foundation of any ML project. We collect diverse datasets, from structured logs to unstructured text and images.",
                position: { x: -10, y: 0, z: 0 },
                camera: { x: -10, y: 5, z: 10 }
            },
            {
                title: "Preprocessing",
                text: "Cleaning, normalizing, and transforming raw data into high-quality features that models can understand.",
                position: { x: -5, y: 0, z: 0 },
                camera: { x: -5, y: 5, z: 10 }
            },
            {
                title: "Model Training",
                text: "Where the magic happens. Using powerful compute to find patterns and optimize parameters.",
                position: { x: 0, y: 0, z: 0 },
                camera: { x: 0, y: 5, z: 10 }
            },
            {
                title: "Model Registry",
                text: "Version control for AI. Storing trained models with their metadata and performance metrics.",
                position: { x: 5, y: 0, z: 0 },
                camera: { x: 5, y: 5, z: 10 }
            },
            {
                title: "Deployment",
                text: "Taking models from the lab to the real world, serving predictions through scalable APIs.",
                position: { x: 10, y: 0, z: 0 },
                camera: { x: 10, y: 5, z: 10 }
            },
            {
                title: "Monitoring",
                text: "Closing the loop. Tracking model performance, drift, and bias in production to ensure reliability.",
                position: { x: 0, y: -5, z: 5 },
                camera: { x: 0, y: 2, z: 15 }
            }
        ];

        this.initLights();
        this.initControls();
        this.createGeometries();
        this.animate();

        window.addEventListener('resize', () => this.onWindowResize());
    }

    initLights() {
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
        this.scene.add(ambientLight);

        const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainLight.position.set(10, 20, 10);
        this.scene.add(mainLight);

        const pointLight = new THREE.PointLight(0x6366f1, 1);
        pointLight.position.set(-10, 10, 5);
        this.scene.add(pointLight);
    }

    initControls() {
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.maxDistance = 50;
        this.controls.minDistance = 5;
    }

    createGeometries() {
        // 1. Data Ingestion (Cylinders/Database icon)
        const dataGroup = new THREE.Group();
        const dataGeom = new THREE.CylinderGeometry(1.5, 1.5, 0.5, 32);
        const dataMat = new THREE.MeshPhongMaterial({ color: 0x4f46e5, shininess: 100 });
        for (let i = 0; i < 3; i++) {
            const disc = new THREE.Mesh(dataGeom, dataMat);
            disc.position.y = i * 0.6;
            dataGroup.add(disc);
        }
        dataGroup.position.set(-10, 0, 0);
        this.scene.add(dataGroup);
        this.components.push(dataGroup);

        // 2. Preprocessing (Gear/Cog)
        const preGeom = new THREE.TorusGeometry(1.2, 0.4, 16, 32);
        const preMat = new THREE.MeshPhongMaterial({ color: 0x10b981, shininess: 100 });
        const preMesh = new THREE.Mesh(preGeom, preMat);
        preMesh.position.set(-5, 0.5, 0);
        preMesh.rotation.x = Math.PI / 2;
        this.scene.add(preMesh);
        this.components.push(preMesh);

        // 3. Training (Sphere/Brain)
        const trainGeom = new THREE.IcosahedronGeometry(1.8, 1);
        const trainMat = new THREE.MeshPhongMaterial({ color: 0xf59e0b, wireframe: true });
        const trainMesh = new THREE.Mesh(trainGeom, trainMat);
        trainMesh.position.set(0, 1, 0);
        this.scene.add(trainMesh);
        this.components.push(trainMesh);

        // Inner core for training
        const coreGeom = new THREE.SphereGeometry(1, 32, 32);
        const coreMat = new THREE.MeshPhongMaterial({ color: 0xf59e0b, emissive: 0xf59e0b, emissiveIntensity: 0.5 });
        const coreMesh = new THREE.Mesh(coreGeom, coreMat);
        coreMesh.position.set(0, 1, 0);
        this.scene.add(coreMesh);

        // 4. Registry (Box/Package)
        const regGeom = new THREE.BoxGeometry(2, 2, 2);
        const regMat = new THREE.MeshPhongMaterial({ color: 0x8b5cf6, shininess: 100 });
        const regMesh = new THREE.Mesh(regGeom, regMat);
        regMesh.position.set(5, 1, 0);
        this.scene.add(regMesh);
        this.components.push(regMesh);

        // 5. Deployment (Rocket/Pyramid)
        const deployGeom = new THREE.ConeGeometry(1.5, 3, 4);
        const deployMat = new THREE.MeshPhongMaterial({ color: 0xec4899, shininess: 100 });
        const deployMesh = new THREE.Mesh(deployGeom, deployMat);
        deployMesh.position.set(10, 1.5, 0);
        this.scene.add(deployMesh);
        this.components.push(deployMesh);

        // 6. Monitoring (Ring/Radar)
        const monGeom = new THREE.RingGeometry(2, 2.5, 32);
        const monMat = new THREE.MeshBasicMaterial({ color: 0x06b6d4, side: THREE.DoubleSide, transparent: true, opacity: 0.5 });
        const monMesh = new THREE.Mesh(monGeom, monMat);
        monMesh.position.set(0, -2, 5);
        monMesh.rotation.x = -Math.PI / 2;
        this.scene.add(monMesh);
        this.components.push(monMesh);

        // Connections (Pipes)
        this.createConnections();
    }

    createConnections() {
        const material = new THREE.MeshBasicMaterial({ color: 0x334155, transparent: true, opacity: 0.3 });

        // Horizontal line
        const pipeGeom = new THREE.CylinderGeometry(0.1, 0.1, 20, 8);
        const pipe = new THREE.Mesh(pipeGeom, material);
        pipe.rotation.z = Math.PI / 2;
        pipe.position.set(0, 0, 0);
        this.scene.add(pipe);

        // Loop back from deployment/registry to monitoring/training
        const curve = new THREE.QuadraticBezierCurve3(
            new THREE.Vector3(10, 0, 0),
            new THREE.Vector3(5, -5, 5),
            new THREE.Vector3(0, -2, 5)
        );
        const points = curve.getPoints(20);
        const curveGeom = new THREE.BufferGeometry().setFromPoints(points);
        const curveLine = new THREE.Line(curveGeom, new THREE.LineBasicMaterial({ color: 0x334155 }));
        this.scene.add(curveLine);
    }

    onWindowResize() {
        if (!this.container) return;
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // Rotation for some objects
        if (this.components[1]) this.components[1].rotation.z += 0.01;
        if (this.components[2]) this.components[2].rotation.y += 0.005;
        if (this.components[5]) this.components[5].rotation.z += 0.02;

        if (this.controls) this.controls.update();
        this.renderer.render(this.scene, this.camera);

        if (this.isTouring && this.targetCameraPos) {
            this.camera.position.lerp(this.targetCameraPos, 0.05);
            this.controls.target.lerp(this.targetLookAt, 0.05);
        }
    }

    nextStep() {
        this.currentStep = (this.currentStep + 1) % this.steps.length;
        this.goToStep(this.currentStep);
    }

    prevStep() {
        this.currentStep = (this.currentStep - 1 + this.steps.length) % this.steps.length;
        this.goToStep(this.currentStep);
    }

    goToStep(index) {
        this.isTouring = true;
        this.currentStep = index;
        const step = this.steps[index];

        this.targetCameraPos = new THREE.Vector3(step.camera.x, step.camera.y, step.camera.z);
        this.targetLookAt = new THREE.Vector3(step.position.x, step.position.y, step.position.z);

        this.onStepChange(step);
    }

    resetView() {
        this.isTouring = false;
        this.targetCameraPos = null;
        this.targetLookAt = null;
        // Smoothly return to default if possible or just let OrbitControls take over
        this.camera.position.set(0, 10, 20);
        this.controls.target.set(0, 0, 0);
    }
}

export default MLProjectTour;
