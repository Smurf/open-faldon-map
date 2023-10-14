import { getContext, onMount, setContext } from "svelte";
import { readable, writable } from 'svelte/store';

export let mobState = writable({   
        mobId: 0,
});

export let mobInfo = writable([])
export let mapState = writable({    
        mapId: 7,
        mapName: "Map 7"
});

export let portalState = writable({   
        active: false
});