<script lang="ts">
    import OsdViewer from "$lib/OSDViewer.svelte";
    import MobSelector from "$lib/MobSelector.svelte";
    import MapSelector from "$lib/MapSelector.svelte";
    import App from "$lib/App.svelte";
    import { onMount } from "svelte";
    var config = {
        id: "faldon-map",
        showNavigator: true,
        navigatorPosition: "BOTTOM_LEFT",
        toolbarDiv: "toolbar-div",
        preserveViewport: true,
        tileSources: [
            'map/huge/1.dzi', 
            'map/huge/2.dzi',
            'map/huge/3.dzi',
            'map/huge/4.dzi',
            'map/huge/5.dzi',
            'map/huge/6.dzi',
            'map/huge/7.dzi', 
            'map/huge/8.dzi',
            'map/huge/9.dzi',
        ]
    }
</script>

<h1>Faldon Monster Map</h1>
<App>
<MobSelector />
<MapSelector />
<OsdViewer {config} />
</App>