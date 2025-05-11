<script lang="ts">
    import * as Context from "@threlte/core"; //{ T, useTask }
    import * as ContextExtra from "@threlte/extras"; //{ interactivity }
    import { Gizmo, OrbitControls } from "@threlte/extras";

    import * as Motion from "svelte/motion"; //{ Spring }
    // import { context } from "three/tsl";
    import * as djquery from "$lib/hooks/django-query.js";

    import { useLoader } from "@threlte/core";
    import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
    import { BufferGeometry, Color } from "three";
    // import { useFrame } from "@threlte/core";
    import { getContext, setContext } from "svelte";

    import Button from "../ui/button/button.svelte";

    setContext("canvas", { loadSTL });

    ContextExtra.interactivity();
    const scale = $state(new Motion.Spring(1));
    let rotation = $state(0);
    Context.useTask((delta) => {
        rotation += delta;
    });

    let loading = $state(true);
    // let StlFile = $state(null);
    const geometry = useLoader(STLLoader);
    let current_model = $state(); // = $state(null);
    let newScaleVal = $state(0);
    let currentGeo = $state();
    let currentCenter = $state();
    export async function loadSTL(id: number): Promise<void> {
        loading = true;
        const StlFile = await djquery.getSTLfile(id);

        // , StlFile);
        try {
            // current_model = await geometry.load(StlFile);
            const loader = new STLLoader();
            const arrayBuffer = await StlFile.arrayBuffer(); // Convert blob to array buffer
            current_model = loader.parse(arrayBuffer);
        } catch (error) {
            console.error("Error loading STL file:", error);
            loading = true;
            return;
        }
        current_model.computeVertexNormals();
        current_model.computeBoundingBox();
        // current_model.computeCenter();

        // console.log("STL Blob:", StlFile);
        loading = false;
        const min = Math.min(
            ...[
                current_model.boundingBox.min.x,
                current_model.boundingBox.min.y,
                current_model.boundingBox.min.z,
            ],
        );
        const max = Math.max(
            ...[
                current_model.boundingBox.max.x,
                current_model.boundingBox.max.y,
                current_model.boundingBox.max.z,
            ],
        );

        const max2 = Math.max(
            ...[
                current_model.boundingBox.max.x - current_model.boundingBox.min.x,
                current_model.boundingBox.max.y - current_model.boundingBox.min.y,
                current_model.boundingBox.max.z - current_model.boundingBox.min.z,
            ],
        );

        
        const center = max2;//max - min;
        newScaleVal = 2.0 / center;
        const actualCenter = [
            -(
                current_model.boundingBox.max.x +
                current_model.boundingBox.min.x
            ) / 2,
            -(
                current_model.boundingBox.max.y +
                current_model.boundingBox.min.y
            ) / 2,
            -(
                current_model.boundingBox.max.z +
                current_model.boundingBox.min.z
            ) / 2,
        ];

        // current_model.translateX(actualCenter[0]);
        // current_model.translateY(actualCenter[1]);
        // current_model.translateZ(actualCenter[2]);
        // let G = new BufferGeometry();
        // G.
        current_model.translate(
            actualCenter[0],
            actualCenter[1],
            actualCenter[2],
        );

        const actualCenter2 = [
            0, //-(current_model.boundingBox.max.x + current_model.boundingBox.min.x) / 2,
            0, //-(current_model.boundingBox.max.y + current_model.boundingBox.min.y) / 2,
            0,
        ]; //-(current_model.boundingBox.max.z + current_model.boundingBox.min.z) / 2]
        currentCenter = actualCenter2;
        // console.log("STL file loaded:", current_model);
        // console.log("STL file Center   :", current_model.boundingBox);
        // console.log("STL file Center   :", actualCenter);
    }
    export function rotateCurrentModel() {
        // console.log("Rotating model");
        // let G = new BufferGeometry();
        if(loading) {
            return;
        }
        // current_model.rotateX(-Math.PI / 2);
        current_model.rotateY(Math.PI / 2);
        current_model.rotateZ(Math.PI / 2);
    }
    let autoRotate: boolean = false;
    let enableDamping: boolean = true;
    let rotateSpeed: number = 1;
    let zoomToCursor: boolean = false;
    let zoomSpeed: number = 1;
    let minPolarAngle: number = 0;
    let maxPolarAngle: number = Math.PI;
    let enableZoom: boolean = true;
</script>

<Context.T.PerspectiveCamera
    makeDefault
    position={[2, 2, 2]}
    oncreate={(ref) => {
        ref.lookAt(0, 1, 0);
    }}
>
    <OrbitControls
        {autoRotate}
        {enableDamping}
        {rotateSpeed}
        {zoomToCursor}
        {zoomSpeed}
        {minPolarAngle}
        {maxPolarAngle}
        {enableZoom}
    >
        <Gizmo />
    </OrbitControls>
</Context.T.PerspectiveCamera>
<Context.T.DirectionalLight position={[0, 10, 10]} />
{#if loading}
    <Context.T.Mesh position.y={0} scale={scale.current}>
        <Context.T.BoxGeometry args={[1, 1, 1]} />
        <Context.T.MeshStandardMaterial />
        <Context.T.ShaderMaterial
            uniforms={{
                color: { value: new Color(0xe0e0e0) },
                time: { value: 1.0 },
            }}
            vertexShader={`
                varying vec3 vNormal;
                void main() {
                    vNormal = normalize(normalMatrix * normal);
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `}
            fragmentShader={`
                uniform vec3 color;
                varying vec3 vNormal;
                void main() {
                    // lowp
                    vec3 light  = vec3(-0.2, 1.0,  1.0);
                    // vec3 light2 = vec3(-1.0, 1.0 , -1.0);
                    lowp float dProd = max(dot(vNormal, light), 0.0)*0.6;
                    lowp vec3 diffuse = dProd * color;
                    lowp vec3 ambient = vec3(0.4, 0.4, 0.4) * color;
                    lowp vec3 specular = vec3(0.1, 0.1, 0.1);
                    lowp float shininess = 0.2;
                    lowp vec3 specularColor = pow(max(dot(reflect(light, vNormal), vec3(0.0, 0.0, 1.0)), 0.0), shininess) * specular;
                    lowp vec3 finalColor = ambient + diffuse;// + specularColor;
                    gl_FragColor = vec4(finalColor, 1.0);
                    // gl_FragColor = vec4(color, 1.0);
                }
            `}
        />
    </Context.T.Mesh>
{:else}
    <Context.T.Mesh
        position={currentCenter}
        scale={newScaleVal}
        geometry={current_model}
    >
        <Context.T.MeshStandardMaterial />
        <Context.T.ShaderMaterial
            uniforms={{
                color: { value: new Color(0xe0e0e0) },
                time: { value: 1.0 },
            }}
            vertexShader={`
                varying vec3 vNormal;
                void main() {
                    vNormal = normalize(normalMatrix * normal);
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `}
            fragmentShader={`
                uniform vec3 color;
                varying vec3 vNormal;
                void main() {
                    // lowp
                    vec3 light  = vec3(-0.2, 1.0,  1.0);
                    // vec3 light2 = vec3(-1.0, 1.0 , -1.0);
                    lowp float dProd = max(dot(vNormal, light), 0.0)*0.6;
                    lowp vec3 diffuse = dProd * color;
                    lowp vec3 ambient = vec3(0.4, 0.4, 0.4) * color;
                    lowp vec3 specular = vec3(0.1, 0.1, 0.1);
                    lowp float shininess = 0.2;
                    lowp vec3 specularColor = pow(max(dot(reflect(light, vNormal), vec3(0.0, 0.0, 1.0)), 0.0), shininess) * specular;
                    lowp vec3 finalColor = ambient + diffuse;// + specularColor;
                    gl_FragColor = vec4(finalColor, 1.0);
                    // gl_FragColor = vec4(color, 1.0);
                }
            `}
        />
    </Context.T.Mesh>
    
{/if}