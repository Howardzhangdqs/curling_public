<template>
    <div class="main" @mousedown="(e) => addCurling(e)" ref="mainDiv" @contextmenu.prevent.capture>
        <template v-for="(item, index) in $props.curlings" :key="index">
            <div :class='["curling_" + (item.color == 0 ? "red" : "yellow")]' class="curling" :style='{
                "left": (item.offsetX - curlingSize / 2) + "px",
                "top": (item.offsetY - curlingSize / 2) + "px",
                "--curling-size": curlingSize + "px"
            }'>
            </div>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { CurlingColor } from "@/stores/curling";
import type { CurlingType } from "@/stores/curling";

const curlingSize = 10;

export interface Props {
    color?: CurlingColor,
    curlings: CurlingType[]
}

const props = withDefaults(defineProps<Props>(), {
    color: CurlingColor.red,
    // curlings: () => ([] as CurlingType[])
});

watch(() => props.curlings, (val) => {
    console.log(val);
});

const mainDiv = ref();

const addCurling = (e: MouseEvent) => {
    console.log(e, e.button, e.offsetX, e.offsetY);

    if (e.target == mainDiv.value) {
        if (e.button == 0) {

            props.curlings.push({
                color: props.color == CurlingColor.red ? CurlingColor.red : CurlingColor.yellow,
                offsetX: e.offsetX,
                offsetY: e.offsetY,
            });
        } else if (e.button == 2) {
            props.curlings.push({
                color: props.color == CurlingColor.red ? CurlingColor.yellow : CurlingColor.red,
                offsetX: e.offsetX,
                offsetY: e.offsetY,
            });
        }
    }

};

</script>

<style scoped>
.main {
    background: url("/battleground.min.png");
    background-position: 0 -10px;
    height: 570px;
    width: 219px;
    margin: 0 auto;
    position: relative;
}

.curling {
    width: var(--curling-size);
    height: var(--curling-size);
    border-radius: 100%;
    position: absolute;
    border: solid 1px black;
}

.curling_red {
    background-color: red !important;
}

.curling_yellow {
    background-color: yellow !important;
}
</style>