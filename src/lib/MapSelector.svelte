<script lang="ts">
    import { onMount } from "svelte";
    export let mapList = new Array();
    
    onMount(async () => {
        console.log("Map selector mounted...");
        for(var i = 0; i < 9; i++){

            mapList.push({name: "Map "+(i+1).toString(), id: i});
        }
        mapList = mapList; //svelte does not detect .push as a change
    });

</script>

{#if mapList}
<select name="map_select" id="map_select">
    {#each mapList as { name, id }, i}
        <option value={id}>{name}</option>
    {/each}
</select>
{/if}