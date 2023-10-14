<script lang="ts">
    import { mobState, mobInfo } from '$lib/store.ts';
    import * as jq from 'jquery?client';
    import { onMount, getContext } from "svelte";
    import { get, writable } from 'svelte/store';

    let mobData = new Array();
    let sortedMobs = new Array();
    onMount(async () => {
        console.log("Mob selector mounted...");
        var mobFile = await fetch("monsters.txt");
        var lines = await mobFile.text();
        lines = lines.split('\n');

        for (var i = 0; i < lines.length - 1; i++) {
            var mData = lines[i].split(",");

            var monster = new Object();
            monster.id = parseInt(mData[0]);
            monster.name = mData[1].toLowerCase()
                            .split(' ')
                            .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
                            .join(' ');
            mobData.push(monster);
        }
        mobData = [...mobData];
        mobInfo.set(mobData);
        //Sort and draw the monster selection separately
        //Weird shit here due to copy by ref vs value and svelte
        var extraSelections = new Array();
        extraSelections.push({name: "-NONE-", id: 0});
        extraSelections.push({name: "-ALL-", id: -1});
        var mobDataCopy = [...mobData];
        sortedMobs = mobDataCopy.sort((a, b) => ((a.name > b.name) ? 1 : (a.name < b.name) ? -1 : 0));

        //svelte does not see push or sort as a mutate
        //to get around this concat the extra options
        sortedMobs = extraSelections.concat(sortedMobs);

    });
    mobState.subscribe((value) => {
            console.log("MobId changed to: "+JSON.stringify(value.mobId));
            if(value.mobId > 0){            
                console.log(get(mobInfo)[value.mobId-1].name)
            }
    });


</script>


<select name="monster_select" id="monster_select" bind:value={$mobState.mobId}>
{#if sortedMobs && sortedMobs.length}
    {#each sortedMobs as { name, id }, i}
        <option value={id}>{name}</option>
    {/each}
{/if}
</select>