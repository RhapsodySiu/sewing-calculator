<script lang="ts">
    import { onMount } from "svelte";
    import * as THREE from "three";
    import { mat4 } from "gl-matrix";

    export let thickness = 2;
    export let width = 10.5;
    export let height = 14.8;
    export let roundness = 2;
    export let colors = ["#ff0000", "#00ff00"];

    let prevThickness = thickness;
    let prevWidth = width;
    let prevHeight = height;
    let prevRoundness = roundness;
    let prevColors = colors;

    const SCALE = 0.01;

    type ProgramInfo = {
        program: WebGLProgram;
        attribLocations: {
            vertexPosition: number;
        };
        uniformLocations: {
            projectionMatrix: WebGLUniformLocation;
            modelViewMatrix: WebGLUniformLocation;
        };
    };

    let canvasWidth = 600;
    let canvasHeight = 600;

    let canvas: HTMLCanvasElement;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;
    let mesh: THREE.Mesh;
    let gradientMesh: THREE.Mesh;

    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };

    onMount(() => {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(
            75,
            canvasWidth / canvasHeight,
            0.1,
            1000,
        );
        camera.position.z = 0.3;

        renderer = new THREE.WebGLRenderer({ canvas });
        renderer.setSize(canvasWidth, canvasHeight);

        // Create a gradient background
        const gradientGeometry = new THREE.PlaneGeometry(2, 2);
        const gradientMaterial = new THREE.ShaderMaterial({
            uniforms: {
                color1: { value: new THREE.Color(0x8e9eab) },
                color2: { value: new THREE.Color(0xeef2f3) },
            },
            vertexShader: `
                varying vec2 vUv;
                void main() {
                vUv = uv;
                gl_Position = vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                uniform vec3 color1;
                uniform vec3 color2;
                varying vec2 vUv;
                void main() {
                gl_FragColor = vec4(mix(color1, color2, vUv.y), 1.0);
                }
            `,
            side: THREE.DoubleSide,
            depthWrite: false,
        });
        gradientMesh = new THREE.Mesh(gradientGeometry, gradientMaterial);
        scene.add(gradientMesh);

        const geometry = createRoundedBoxGeometry(
            width * SCALE,
            height * SCALE,
            thickness * SCALE,
            roundness * SCALE,
        );
        // const geometry = new THREE.BoxGeometry(width * SCALE, height * SCALE, thickness * SCALE);
        const materials = [
            new THREE.MeshPhongMaterial({ color: colors[0] }),
            new THREE.MeshPhongMaterial({ color: colors[1] }),
        ];
        mesh = new THREE.Mesh(geometry, materials);
        scene.add(mesh);

        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(-1, 1, 1).normalize(); // Top left forward the camera
        scene.add(light);

        const ambientLight = new THREE.AmbientLight(0x404040); // soft white light
        scene.add(ambientLight);

        // Add event listeners for mouse interaction
        canvas.addEventListener("mousedown", onMouseDown, false);
        canvas.addEventListener("mousemove", onMouseMove, false);
        canvas.addEventListener("mouseup", onMouseUp, false);
        canvas.addEventListener("mouseleave", onMouseUp, false);

        animate();
    });

    $: if (mesh) {
        if (
            thickness !== prevThickness ||
            width !== prevWidth ||
            height !== prevHeight ||
            roundness !== prevRoundness ||
            colors[0] !== prevColors[0] ||
            colors[1] !== prevColors[1]
        ) {
            console.log("update");
            mesh.geometry.dispose();
            mesh.geometry = createRoundedBoxGeometry(
                width * SCALE,
                height * SCALE,
                thickness * SCALE,
                roundness * SCALE,
            );

            (mesh.material as THREE.MeshPhongMaterial[]).forEach(
                (material: THREE.MeshPhongMaterial, i: number) => {
                    material.color.set(colors[i]);
                },
            );

            mesh.rotation.set(-0.48, 0.65, -2.6);
        }
    }

    function createRoundedBoxGeometry(
        w: number,
        h: number,
        d: number,
        r: number,
    ) {
        const shape = new THREE.Shape();

        shape.moveTo(r, 0);
        shape.lineTo(w - r, 0);
        shape.quadraticCurveTo(w, 0, w, r);
        shape.lineTo(w, h - r);
        shape.quadraticCurveTo(w, h, w - r, h);
        shape.lineTo(r, h);
        shape.quadraticCurveTo(0, h, 0, h - r);
        shape.lineTo(0, r);
        shape.quadraticCurveTo(0, 0, r, 0);

        const geometry = new THREE.ExtrudeGeometry(shape, {
            depth: d,
            bevelEnabled: false,
            curveSegments: 6,
        });

        const gp1 = geometry.groups[0];
        const gp2 = geometry.groups[1];

        let fabricSideOffsetCount = 36; // magic number
        let fabricSideIdxStart = gp2.start + fabricSideOffsetCount;
        let fabricSideCount = 6; // 6 vertices for the fabric side
        let fabricSideIdxEnd = fabricSideIdxStart + fabricSideCount;
        geometry.clearGroups();
        geometry.addGroup(gp1.start, gp1.count, 0);
        geometry.addGroup(gp2.start, fabricSideOffsetCount, 1);
        geometry.addGroup(fabricSideIdxStart, fabricSideCount, 0);
        geometry.addGroup(
            fabricSideIdxEnd,
            gp2.count - fabricSideCount - fabricSideOffsetCount,
            1,
        );

        geometry.center();
        return geometry;
    }

    function onMouseDown(event: MouseEvent) {
        isDragging = true;
        previousMousePosition = {
            x: event.clientX,
            y: event.clientY,
        };
    }

    function onMouseMove(event: MouseEvent) {
        if (isDragging) {
            const deltaMove = {
                x: event.clientX - previousMousePosition.x,
                y: event.clientY - previousMousePosition.y,
            };

            const deltaRotationQuaternion = new THREE.Quaternion().setFromEuler(
                new THREE.Euler(
                    toRadians(deltaMove.y * 1),
                    toRadians(deltaMove.x * 1),
                    0,
                    "XYZ",
                ),
            );

            mesh.quaternion.multiplyQuaternions(
                deltaRotationQuaternion,
                mesh.quaternion,
            );

            previousMousePosition = {
                x: event.clientX,
                y: event.clientY,
            };
        }
    }

    function onMouseUp() {
        isDragging = false;
    }

    function toRadians(angle: number) {
        return angle * (Math.PI / 180);
    }

    function animate() {
        requestAnimationFrame(animate);

        renderer.render(scene, camera);
    }
</script>

<canvas bind:this={canvas} width={canvasWidth} height={canvasHeight}></canvas>

<style>
    canvas {
        display: block;
        margin: 0 auto;
    }
</style>
