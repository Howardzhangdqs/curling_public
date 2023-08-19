<template>
    <div ref="artRef" class="main" style="height: calc(v-blind);"></div>
</template>
  
<script lang="ts">
import Artplayer from "artplayer";
import { type Option } from "artplayer/types/option";

export default {
    data() {
        return {
            instance: undefined as Artplayer | undefined,
            width: 0,
            height: 0,
        };
    },
    watch: {
    },
    props: {
        option: {
            type: Option,
            required: false,
        },
        url: {
            type: String,
            required: true,
        },
    },
    mounted() {
        this.resize();

        this.instance = new Artplayer({
            ...(this.option),
            url: this.url,
            container: this.$refs.artRef as HTMLDivElement,
            setting: true,
            flip: true,
            playbackRate: true,
            aspectRatio: true,
            subtitleOffset: true,
            fullscreen: true,
            fullscreenWeb: true,
        });

        this.$nextTick(() => {
            this.$emit("get-instance", this.instance);
        });

        this.instance.on("resize", () => {
            this.resize();
        });
    },
    methods: {
        resize() {
            this.width = (this.$refs.artRef as HTMLDivElement).clientWidth as number;
            this.height = this.width / 864 * 486;

            console.log(this.width, this.height);
        },
    },
    beforeUnmount() {
        if (this.instance && this.instance.destroy) {
            this.instance.destroy(false);
        }
    },
};
</script>

<style scoped>
.main {
    width: 100%;
    height: 500px;
}
</style>