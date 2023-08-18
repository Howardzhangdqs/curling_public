<template>
	<v-row>

		<v-col>
			<v-sheet cols="8" class="covery">
				<ArtPlayer url="/target.tiny.mp4" @get-instance="getArtPlayerInstance"></ArtPlayer>
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

					<v-divider class="my-2"></v-divider>

					<v-list-item link color="grey-lighten-4">
						<v-sheet rounded="lg" elevation="10" class="left-sheet">
							<v-img src="/5.png" v-if="timer >= 20"></v-img>
						</v-sheet>
					</v-list-item>

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

import { VideoPlayer } from "@videojs-player/vue";
import Artplayer from "artplayer";

import axios from "axios";

import { TTS } from "./tts";

import ArtPlayer from "@/components/ArtPlayer.vue";

const sleep = (delay: number) => new Promise((resolve) => setTimeout(resolve, delay));


const links: string[] = [
	"控制面板",
	"模块状况"
];



const msg: Ref<string> = ref("");

const msg_loading: Ref<boolean> = ref(false);

const answer = "场上已被清空，暂时无法很好判断场面局势，我无法根据坐标分析局势。请提供更具体的问题或信息，让我能够更好地回答您的问题。";
const answer_msg: Ref<string> = ref("");

const msg_handle = () => {
	// console.log(msg.value);
	msg_loading.value = true;

	answer_msg.value = "";

	let i = 0;

	setTimeout(() => {
		msg_loading.value = false;


		TTS(answer);

		(async () => {
			while ((i) <= answer.length) {
				// console.log(new Date());

				i += Math.round(Math.random() * 10);
				answer_msg.value = answer.slice(0, i);
				// console.log(new Date());

				await sleep(100);

				// console.log(new Date());
			}
		})();
	}, (5000));
};



const player_config = {
	playbackRates: [0.5, 0.75, 1, 1.5, 1.75, 2],
	autoplay: true,
	muted: false,
	loop: false,
	preload: "auto",
	language: "zh-CN",
	// aspectRatio: '16:9',
	fluid: true,
	sources: [{
		type: "video/mp4",
		src: "/target.tiny.mp4"
	}],
	poster: "",
	notSupportedMessage: "此视频暂无法播放，请稍后再试",
	controlBar: {
		timeDivider: true,
		durationDisplay: true,
		remainingTimeDisplay: true,
		fullscreenToggle: true
	},
	width: 100
};


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

const video_player = ref();


onMounted(() => {
	fake_handle();
})

// 3.24开始

const datals = [
	[0, 0, 0, 0],// 17
	[0, 0, 0, 0],// 18
	[0, 0, 0, 0],// 19
	[0, 3.1, 0, 0],// 19
	[0, 6.2, 0, 0],// 19
	[0, 9.2, 0, 0],// 19
	[0, 12, 0, 0],// 20
	[0, 15., 0, 0],// 21
	[0, 33.2, 0, 0],// 22
	[1.7, 29, 0.57, 2],// 23
	[1.6, 25, 0.55, 2],// 24
	[1.5, 21, 0.53, 2],// 25
	[1.4, 16, 0.56, 2],// 26
	[1.3, 11, 0.59, 2],// 27
	[1.6, 25, 0.55, 2],// 24
	[1.5, 31, 0.53, 2],// 25
	[1.4, 36, 0.56, 2],// 26
	[1.6, 38, 0.55, 2],// 24
	[1.5, 48, 0.53, 2],// 25
	[1.4, 50, 0.56, 2],// 26
	[0, 0, 0, 0],// 28
	[0, 0, 0, 0],// 28
	[0, 0, 0, 0],// 28
	[0, 0, 0, 0],// 28
	[0, 0, 0, 0]// 28
];

const timer = ref(0);

const fake_handle = () => {

	msg_handle();

	console.log("good");

	setInterval(() => {

		const currentTime = Math.round(ArtPlayerInstance.currentTime);
		console.log(ArtPlayerInstance.currentTime)

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
	}, 500);
};

let ArtPlayerInstance: Artplayer;

const getArtPlayerInstance = (ArtPlayer: Artplayer) => {
	ArtPlayerInstance = ArtPlayer
	console.log(ArtPlayer);
	console.log(ArtPlayer.currentTime);
};


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