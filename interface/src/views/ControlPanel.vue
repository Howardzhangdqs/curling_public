<template>
	<v-row>

		<v-col>
			<v-sheet cols="8" class="covery">
				<ArtPlayer url="/final1.mp4" @get-instance="getArtPlayerInstance"></ArtPlayer>
				<!-- <video-player controls :options="player_config" class="video-player vjs-custom-skin" 
					ref="video_player"></video-player> -->
			</v-sheet>
		</v-col>

		<v-col cols="4" class="left-column">
			<v-sheet rounded="lg" elevation="10" class="left-sheet">
				<v-list rounded="lg">
					<v-list-item>
						<v-list-item-title>
							{{ timer }}s（{{ curling_status }}）
						</v-list-item-title>
					</v-list-item>
					<template v-for="n in curling_data" :key="n">
						<v-list-item link class="font-consolas">
							<v-list-item-title>
								{{ n.tag }}: {{ `${n.data}±${n.err} ${n.unit}` }}
							</v-list-item-title>
						</v-list-item>
					</template>

					<template v-if="PhysicalSimulation">

						<v-divider class="my-2"></v-divider>

						<v-list-item link color="grey-lighten-4">
							<v-sheet rounded="lg" elevation="10" class="left-sheet">
								<v-img :src="PhysicalSimulation"></v-img>
							</v-sheet>
						</v-list-item>

					</template>

					<template v-if="alert">

						<v-divider class="my-2"></v-divider>
						<v-alert v-for="item in alert" type="error" title="出现错误" :text="item" variant="tonal"></v-alert>

					</template>

					<v-divider class="my-2"></v-divider>

					<v-list-item link color="grey-lighten-4">
						<v-list-item-text><v-btn variant="tonal">刷新</v-btn></v-list-item-text>
					</v-list-item>
				</v-list>
			</v-sheet>
		</v-col>
	</v-row>
	<v-row>
		<v-col>
			<v-sheet rounded="lg" elevation="10">
				<v-card rounded="lg" min-height="5em" :loading="msg_loading">
					<v-card-title>自然语言建议</v-card-title>
					<v-card-text>{{ answer_msg }}</v-card-text>
					<v-divider></v-divider>
					<v-card rounded="lg" class="float-right">
						<v-card-text>内容为AI生成，可能有误，请注意甄别</v-card-text>
					</v-card>
				</v-card>
			</v-sheet>
		</v-col>
	</v-row>
</template>
  
<script setup lang="ts">

import { reactive, ref, onMounted } from "vue";
import type { Ref } from "vue";

import Artplayer from "artplayer";

import axios from "axios";

import { TTS } from "./tts";

import ArtPlayer from "@/components/ArtPlayer.vue";
import type { ReactiveVariable } from "vue/macros";

import * as Hook from "./hook";

import { type NLPType, type PhysicalType } from "./typing";

const sleep = (delay: number) => new Promise((resolve) => setTimeout(resolve, delay));

const PhysicalSimulation: Ref<string> = ref("");


axios.get("/data.json").then(({ data }) => {
	console.log(data);
	datals = reactive(data.data);

	const nlps = data.nlp as NLPType[];
	for (const nlp of nlps) {
		Hook.AddHook(nlp.time, () => {
			TTS(nlp.content);

			(async () => {
				let i = 0;
				while ((i) <= nlp.content.length) {
					// console.log(new Date());

					i += Math.round(Math.random() * 10);
					answer_msg.value = nlp.content.slice(0, i);
					// console.log(new Date());

					await sleep(100);

					// console.log(new Date());
				}
			})();
		});
	}

	const physicals = data.physical as PhysicalType[];

	for (const physical of physicals) {
		Hook.AddHook(physical.time, () => {
			PhysicalSimulation.value = physical.src;
			console.log(PhysicalSimulation.value);
		});
	}
});

const msg_loading: Ref<boolean> = ref(false);
const answer_msg: Ref<string> = ref("");


const curling_data = reactive([
	{
		tag: "壶速",
		data: 0,
		err: 0,
		unit: "m/s"
	},
	{
		tag: "位置",
		data: 0,
		err: 0,
		unit: "m"
	},
	{
		tag: "角速度",
		data: 0,
		err: 0,
		unit: "转/s"
	}
]);

const curling_status = ref("间隙");


onMounted(() => {
	fake_handle();
});

// 3.24开始

var datals: ReactiveVariable<[number, number, number, number][]>;

const timer = ref(0);

const fake_handle = () => {

	// msg_handle();


	console.log("good");

	setInterval(() => {

		const currentTime = Math.round(ArtPlayerInstance.currentTime);
		console.log(ArtPlayerInstance.currentTime);

		Hook.ExecuteHook(currentTime);

		timer.value = currentTime;
		// console.log($video.currentTime);

		if (currentTime > datals.length) {
			curling_status.value = "间隙";
			return;
		}

		for (let j = 0; j <= 2; j++) {
			curling_data[j].data = datals[currentTime][j];
			curling_data[j].err = Math.round(datals[currentTime][j] * 0.2 * 1000) / 1000;
		}

		if (datals[currentTime][3] == 0) curling_status.value = "间隙";
		if (datals[currentTime][3] == 1) curling_status.value = "投掷中";
		if (datals[currentTime][3] == 2) curling_status.value = "已出手，磕碰";
		if (datals[currentTime][3] == 3) curling_status.value = "已出手，大力击打";
	}, 500);
};

let ArtPlayerInstance: Artplayer;

const getArtPlayerInstance = (ArtPlayer: Artplayer) => {
	ArtPlayerInstance = ArtPlayer;
	console.log(ArtPlayer);
	console.log(ArtPlayer.currentTime);

	ArtPlayerInstance.on("seek", () => {
		Hook.InitHook();
	});
};

const alert: Ref<string[]> = ref([]);

// setTimeout(() => {
// 	ArtPlayerInstance.pause()
// 	alert.value.push("模块 `数据平滑` 掉线");
// 	alert.value.push("模块 `阵型识别` 掉线");
// }, 10000);


</script>

<style scoped>
.root {
	--covery-border-radius: 8px;
}

.left-column {
	text-align: left;
	/* font-family: Consolas; */
}

.font-consolas {
	font-family: Consolas;
}

.covery {
	border-radius: var(--covery-border-radius);
}

.covery>img {
	/* width: 100%; */
	height: 100%;
	border-radius: var(--covery-border-radius);
}

.float-right {
	float: right;
	color: rgb(255, 67, 67);
}
</style>