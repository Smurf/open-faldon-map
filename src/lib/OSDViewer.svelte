<script lang="ts">
    import OpenSeadragon from 'openseadragon?client';
    import { onMount } from "svelte";
    export let config = {};
    export let currentMap = 7;
    onMount(() => {
        console.log("OSD Viewer mounted...");
        let viewer = OpenSeadragon(config);
        viewer.goToPage(currentMap-1);
    });

</script>


<div id="toolbar-div">
</div>

<div id="faldon-map">
</div>
