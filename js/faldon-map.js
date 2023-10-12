var spawnData = new Array();
var monsterData = new Array();
var portalData = new Array();

var mapWidth = 4096;
var mapHeight = 2048;
var app;
//map is 4x size of original
var tileHeight = 1;
var tileWidth = 4;

var osConfig, anno, viewer, db = {};
var selectedMob;
var currentMap = "7";
var ALL_SPAWNS = -1;
function selectMonster(monsterId) {
    selectedMob = monsterId;

    var mapsWithMob = new Array();

    for (var i = 0; i < spawnData.length; i++) {
        var spawn = spawnData[i];
        if (spawn.monster == monsterId) {
            var inlist = false;
            for (var m = 0; m < mapsWithMob.length; m++) {
                if (mapsWithMob[m] == spawn.map) {
                    inlist = true;
                    break;
                }
            }

            if (!inlist) {
                mapsWithMob.push(spawn.map);
            }
        }
    }
    clearSpawns();
    drawSpawns(currentMap, selectedMob);
    var sel = document.monster_form.map_select;
    sel.options.length = 0;

    if (selectedMob > 0) {
        var mobOnCurrentMap = false;
        for (var i = 0; i < mapsWithMob.length; i++) {
            var map = mapsWithMob[i];

            if (map == currentMap) {
                mobOnCurrentMap = true;
            }

            sel.options[sel.options.length] = new Option("Map " + map, map, false, false);
        }

        if (mobOnCurrentMap) {
            $("#map_select").val(currentMap);
        } else {

            currentMap = sel.options[0].value;
            selectMap(currentMap);
        }
    } else {

        for (var i = 1; i <= 9; i++) {
            var currentOption = sel.options.length;
            sel.options[currentOption] = new Option("Map " + i, i, false, false);
        }
        $("#map_select").val(currentMap);
    }
}

function toTitleCase(tomod) {
    return tomod.toLowerCase().split(' ').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ');

}

function loadMonsters() {
    $.get("monsters.txt", function(data) {
        var lines = data.split("\n");

        for (var i = 0; i < lines.length - 1; i++) {
            var mData = lines[i].split(",");

            var monster = new Object();
            monster.id = mData[0];
            monster.name = toTitleCase(mData[1]);

            monsterData.push(monster);
        }
        
        //Sort and draw the monster selection separately
        var sel = document.monster_form.monster_select;
        sel.options.length = 0;
        sel.options[0] = new Option("-NONE-", 0);
        sel.options[1] = new Option("-ALL-", -1);
        monsterDisplay = [...monsterData]
        monsterDisplay.shift() //Remove -NONE- at beginning
        monsterDisplay.sort((a, b) => ((a.name > b.name) ? 1 : (a.name < b.name) ? -1 : 0));
        for (var i = 0; i < monsterDisplay.length; i++) {
            var monster = monsterDisplay[i];

            sel.options[sel.options.length] = new Option(monster.name, monster.id, false, false);
        }
    });
}
function loadPortals() {
    $.get("portals.txt", function(data) {
        var lines = data.split("\n");
        // Strip headers of first line
        for (var i = 1; i < lines.length; i++){ 
            pData = lines[i].split(",");
            if(pData[0] == "") continue;

            var portal = new Object();
            
            portal.map = pData[0];
            portal.x = pData[1];
            portal.y = pData[2];
            portal.to = pData[3];
            portal.to_x = pData[4];
            portal.to_y = pData[5];

            portalData.push(portal);
        }
    });
}
function loadSpawns() {
    $.get("monster-spawns.txt", function(data) {
        var lines = data.split("\n");

        for (var i = 0; i < lines.length; i++) {
            var sData = lines[i].split(",");

            var spawn = new Object();

            spawn.x = sData[0];
            spawn.y = sData[1];
            spawn.z = sData[2];
            spawn.map = sData[3];
            spawn.monster = sData[4];
            if (monsterData[spawn.monster] != undefined) {
                spawn.name = monsterData[spawn.monster].name;
            } else {
                spawn.name = "No name for ID " + spawn.monster;
            }
            spawnData.push(spawn);
        }
    });

    //spawnData.sort((a, b) => ((a.y > b.y) ? 1 : (a.y < b.y) ? -1 : 0));
    //spawnData.sort((a, b) => ((a.x > b.x) ? -1 : (a.x < b.x) ? 1 : 0));
    spawnData.sort();
}
function drawPortals(mapNr) {
    if(document.getElementById("show_portals").checked){
        console.log("Drawing portals for map "+mapNr+"...");
        console.log("Portal Data at drawPortals:"+portalData);
        for (var i = 0; i < portalData.length; i++) {
            var portal = portalData[i];

            if(portal.map != mapNr) continue;
            var x = parseInt(portal.x);
            var y = parseInt(portal.y);

            var sx = (x - y) * tileWidth;
            sx += mapWidth / 2;
            var sy = (x + y) * tileHeight;
            var vx = sx / mapWidth; //viewport x
            var vy = sy / mapHeight; //viewport y

            var elem = document.createElement("div");
            elem.classList.add('portal-pointer');
            var svg_img = document.createElement("img");
            svg_img.src = "images/portal-pointer.png";
            svg_img.style.filter = 'hue-rotate(180deg)';
            var tooltip = document.createElement("span");
            tooltip.classList.add('tooltip');
            tooltip.innerText = "Portal to map "+portal.to_map;
            
            elem.appendChild(tooltip);
            elem.id = "spawn" + i;
            elem.appendChild(svg_img);
            viewer.addOverlay({
                element: elem,
                location: new OpenSeadragon.Point(vx, vy),
                placement: OpenSeadragon.Placement.CENTER
            });
            console.log("Portal for map" + mapNr + " found at x: " + vx + " , y: " + vy);
        }
    }
}

function clearPortals(){

    $(".portal-pointer").each( function (i) {
        viewer.removeOverlay(this);
    });
}

function drawSpawns(mapNr, monsterId) {

    for (var i = 0; i < spawnData.length; i++) {
        var spawn = spawnData[i];
        if(monsterId != ALL_SPAWNS){
            if (spawn.map != mapNr || spawn.monster != monsterId) {
                continue;
            }
        }

        if(spawn.map != mapNr) continue;

        var x = parseInt(spawn.x);
        var y = parseInt(spawn.y);

        var sx = (x - y) * tileWidth;
        sx += mapWidth / 2;
        var sy = (x + y) * tileHeight;
        var vx = sx / mapWidth; //viewport x
        var vy = sy / mapHeight; //viewport y

        var elem = document.createElement("div");
        elem.classList.add('spawn-pointer');
        var svg_img = document.createElement("img");
        svg_img.src = "images/Down_arrow_red.png";
        svg_img.style.filter = 'hue-rotate('+spawn.monster*20+'deg)';

        var tooltip = document.createElement("span");
        tooltip.classList.add('tooltip');
        tooltip.innerText = spawn.name;
        
        var image = document.createElement("img");
        
        image.classList.add('mob-image');
        image.src = "images/mob-art/"+spawn.monster+".png"
        //this does not work?!
        //image.onerror = function (){this.type.display='none;'}
        //Fix for other spawn markers overlapping tool tips
        tooltip.zindex = 5+(spawnData.length-i);
        tooltip.appendChild(image);
        elem.appendChild(tooltip);
        elem.id = "spawn" + i;
        elem.appendChild(svg_img);
        viewer.addOverlay(elem,
            new OpenSeadragon.Point(vx, vy)
        );
        console.log("Spawn for " + monsterId + " found at x: " + vx + " , y: " + vy);
    }
}

function clearSpawns() {
    $(".spawn-pointer").each( function (i) {
        viewer.removeOverlay(this);
    });
}


function startViewport() {

    osConfig = {
        id: "faldon-map",
        showNavigator: true,
        navigatorPosition: "BOTTOM_LEFT",
        prefixUrl: "images/",
        toolbarDiv: "toolbar-div",
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

    viewer = OpenSeadragon(osConfig);

    var config = {
        widgets: [
            'COMMENT', {
                widget: 'TAG',
                vocabulary: ["monster",
                    "npc",
                    "religion",
                    "easy",
                    "medium",
                    "hard",
                    "portal"
                ]
            }
        ]
    };
    anno = OpenSeadragon.Annotorious(viewer, config);
    map = document.getElementById('faldon-map');
    //loadAnnotations();
}


function selectMap(mapNum) {
    currentMap = mapNum;
    viewer.goToPage(mapNum - 1);
    drawPortals(currentMap);
    drawSpawns(currentMap, selectedMob);
}

function startApp() {
    startViewport();
    loadPortals();
    loadMonsters();
    loadSpawns();
    selectMonster(0);
    selectMap(currentMap);


    $("#monster_select").change(function(evt) {
        selectMonster(this.value);
        drawPortals($("#map_select").val())
    });

    $("#map_select").change(function(evt) {
        selectMap(this.value);
    });

    $("#show_portals").change(function(evt) {
        if(this.checked){
            drawPortals($("#map_select").val());
        }else{
            clearPortals();
        }
    });

}

window.onload = function() {
    startApp();
}

