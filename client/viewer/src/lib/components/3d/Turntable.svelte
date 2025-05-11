<script lang="ts">
    import * as Context from "@threlte/core"; //{ T, useTask }
    import * as ContextExtra from "@threlte/extras"; //{ interactivity }
    import * as Motion from "svelte/motion"; //{ Spring }
    import { context } from "three/tsl";
    import * as djquery from "$lib/hooks/django-query.js";
    
    ContextExtra.interactivity();
    const scale = $state(new Motion.Spring(1));
    let rotation = $state(0);
    Context.useTask((delta) => {
        rotation += delta;
    });

    export function loadSTL(id: number) {
        
    };
    
</script>

<Context.T.PerspectiveCamera
    makeDefault
    position={[10, 10, 10]}
    oncreate={(ref) => {
        ref.lookAt(0, 1, 0);
    }}
/>
<Context.T.DirectionalLight position={[0, 10, 10]} />
<Context.T.Mesh
    rotation.y={rotation}
    position.y={1}
    scale={scale.current}
    onpointerenter={() => {
        scale.target = 1.5;
    }}
    onpointerleave={() => {
        scale.target = 1;
    }}
>
    <Context.T.BoxGeometry args={[1, 2, 1]} />
    <Context.T.MeshStandardMaterial color="hotpink" />
    <!-- <Context.T. -->
</Context.T.Mesh>
