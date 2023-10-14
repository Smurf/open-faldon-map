<script>
    import { getContext, onMount, setContext } from "svelte";
    import { readable, writable } from 'svelte/store';
    //setContext('AppState');

    const mobState = writable({mobId: 0, mobName: "-NONE-"});
</script>

<div>
    <slot />
</div>