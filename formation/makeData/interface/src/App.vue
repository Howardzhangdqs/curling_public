<template>
	<main>
		<div class="curlingFieldContainer">
			<curlingField class="curlingField" :curlings='curlingList.curlingList' :color="curlingFieldColor"
				:style='{ "--curling-field-rotate": curlingFieldRotate + "deg" }' />
		</div>
		<button @click="FieldAddGroup">下一组</button>
		<button @click="FieldNextGroup">计入</button>
		<button @click="FieldShake">抖动</button>
		<button @click="FieldSwitchCurlingColor">切换颜色</button>
		<button @click="FieldClean">清空场面</button>
		<button @click="FieldUndo">撤销</button>
		<button @click="FieldUndoOutput">撤销输出</button>
		<button @click="FieldRotate">旋转</button>
		<button @click="FieldCopy">复制</button>
		<div>
			<template v-for="(val, index) in lodash.cloneDeep(output).reverse()" :key="index">
				<div><code>{{ output.length - index }}&nbsp;</code><code class="codespace">{{ JSON.stringify(val) }}</code>
				</div>
			</template>
		</div>
	</main>
</template>

<script lang="ts">
import useClipboard from "vue-clipboard3";
const { toClipboard } = useClipboard();

import curlingField from "./components/curlingField.vue";

import { useCurlingStore, type CurlingType, CurlingColor } from "@/stores/curling";

import keymaster from "keymaster";
import _ from "lodash";

const CURLING_SHAKE = 10;

export default {
    components: {
        curlingField
    },
    data() {
        return {
            curlingFieldRotate: 0,
            curlingFieldColor: CurlingColor.red,
            curlingList: useCurlingStore(),
            output: [] as CurlingType[][],
            curlingListShake: [] as [number, number][],
            lodash: _
        };
    },
    watch: {
    },
    methods: {
        /** 清空场面 */
        FieldClean() {
            this.curlingList.$reset();
            this.FieldShakeInit();
        },

        /** 下一组 */
        FieldNextGroup() {
            this.output.push(this.curlingList.copy().curlingList);
        },

        /** 增加一组，但是不清场 */
        FieldAddGroup() {
            this.FieldNextGroup(); this.FieldClean();
        },
        FieldSwitchCurlingColor() {
            if (this.curlingFieldColor == CurlingColor.red) this.curlingFieldColor = CurlingColor.yellow;
            else this.curlingFieldColor = CurlingColor.red;
        },
        FieldUndo() {
            this.curlingList.curlingList.pop();
        },
        FieldUndoOutput() {
            this.output.pop();
        },
        FieldRotate() {
            this.curlingFieldRotate += 90;
            this.curlingFieldRotate %= 360;
        },
        FieldCopy() {
            toClipboard(JSON.stringify(this.output));
        },
        FieldShake() {
            console.log("this.curlingList.curlingList", this.curlingList.curlingList);

            for (let i in this.curlingListShake) {
                this.curlingList.curlingList[i].offsetX -= this.curlingListShake[i][0];
                this.curlingList.curlingList[i].offsetY -= this.curlingListShake[i][1];
            }

            this.curlingListShake = [];

            const getRandomShake = () => _.random(-CURLING_SHAKE, CURLING_SHAKE);

            for (let i in this.curlingList.curlingList) {
                const temp: [number, number] = [getRandomShake(), getRandomShake()];
                this.curlingListShake.push(temp);
                this.curlingList.curlingList[i].offsetX += temp[0];
                this.curlingList.curlingList[i].offsetY += temp[1];
            }
        },
        FieldShakeInit() {
            this.curlingListShake = [];
        }
    },
    mounted() {
        this.FieldShakeInit();

        keymaster("z, s, w", this.FieldUndo);
        keymaster("q, a", this.FieldAddGroup);
        keymaster("c", this.FieldClean);
        keymaster("ctrl+z", this.FieldUndoOutput);
    }
};
</script>

<style scoped>
.logo {
	margin: 0 auto;
	display: block;
}

.curlingField {
	-webkit-transform: rotate(var(--curling-field-rotate));
	-moz-transform: rotate(var(--curling-field-rotate));
	-o-transform: rotate(var(--curling-field-rotate));
	transform: rotate(var(--curling-field-rotate));
}

.curlingFieldContainer {
	margin: auto 0;
	height: 600px;
}

.codespace {
	word-wrap: break-word;
	font-family: Consolas;
}
</style>
