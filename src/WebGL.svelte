<script lang="ts">
    import { onMount } from "svelte";
    import * as THREE from "three";
    import { mat4 } from "gl-matrix";

    export let thickness = 2;
    export let width = 10.5;
    export let height = 14.8;

    const SCALE = 0.01;

    type ProgramInfo = {
        program: WebGLProgram,
        attribLocations: {
            vertexPosition: number,
        },
        uniformLocations: {
            projectionMatrix: WebGLUniformLocation,
            modelViewMatrix: WebGLUniformLocation,
        },
    };

    let canvasWidth = 800;
    let canvasHeight = 600;

    let canvas: HTMLCanvasElement;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;
    let mesh: THREE.Mesh;

    onMount(() => {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, canvasWidth / canvasHeight, 0.1, 1000);
        camera.position.z = 0.2;

        renderer = new THREE.WebGLRenderer({ canvas });
        renderer.setSize(canvasWidth, canvasHeight);

        const geometry = new THREE.BoxGeometry(width * SCALE, height * SCALE, thickness * SCALE);
        const material = new THREE.MeshPhongMaterial({ color: 0xffffff });
        mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(-1, 1, 1).normalize(); // Top left forward the camera
        scene.add(light);

        const ambientLight = new THREE.AmbientLight(0x404040); // soft white light
        scene.add(ambientLight);

        animate();
    });

    $: if (mesh) {
        mesh.geometry.dispose();
        mesh.geometry = new THREE.BoxGeometry(width * SCALE, height * SCALE, thickness * SCALE);
    }

    function animate() {
        requestAnimationFrame(animate);

        mesh.rotation.x += 0.01;
        mesh.rotation.y += 0.01;

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