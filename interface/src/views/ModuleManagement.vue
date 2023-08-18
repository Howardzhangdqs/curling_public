<template>
    <v-row :class="$style.unselectable">
        <template v-for="(n, index) in modules" :key="n">
            <v-col :cols="n.cols">
                <v-card rounded="lg" :title="n.name" class="v-card-center"
                    :color="n.status == 2 ? '#060' : (n.status == 3 ? '#600' : '')" @click="connect(index)"
                    :loading="n.status == 1">

                    <v-card-text>
                        <p>{{ machines[n.machine || 0] }}</p>
                        <p>{{ statuses[n.status] }}</p>
                    </v-card-text>
                </v-card>
            </v-col>
        </template>
    </v-row>
</template>

<script setup lang="ts">

import { reactive } from "vue";

const links: string[] = [
    "控制面板",
    "模块状况"
];

const statuses = [
    "重启中",
    "重连中",
    "正常",
    "失联",
    "所包含的模块错误",
    "已被遗弃"
];

const connect = (index: number) => {
    if (modules[index].status != 5) {
        modules[index].status = 1;
        setTimeout(() => {
            modules[index].status = 2;
        }, modules[index].delay || 1000);
    }
};

const machines = [
    "Default",
    "3060 Laptop 1",
    "3060 Laptop 2",
    "3060 Laptop 3",
];

const modules = reactive<{
    name: string;
    status: number;
    cols: number;
    machine?: number;
    delay?: number;
}[]>([
    {
        name: "服务器",
        status: 2,
        cols: 8,
        delay: 100,
        machine: 0
    },

    {
        name: "Nodejs进程",
        status: 2,
        cols: 4,
        delay: 100
    },
    {
        name: "Core 核心",
        status: 2,
        cols: 12,
        delay: 100
    },

    {
        name: "Electron进程",
        status: 5,
        cols: 12
    },

    {
        name: "场景识别",
        status: 2,
        cols: 2,
        machine: 1
    },
    {
        name: "赛道矫正",
        status: 2,
        cols: 3,
        machine: 1
    },
    {
        name: "目标检测",
        status: 3,
        cols: 3,
        machine: 3
    },
    {
        name: "数据平滑",
        status: 1,
        cols: 2,
        machine: 2
    },
    {
        name: "阵型识别",
        status: 1,
        cols: 2,
        machine: 2
    },
    {
        name: "感官增强",
        status: 2,
        cols: 6
    },
    {
        name: "视频超分辨率",
        status: 2,
        cols: 3
    },
    {
        name: "TTS",
        status: 2,
        cols: 3
    }
]);

const loading = reactive(new Array(modules.length).fill(true));

</script>

<style module scoped src="@/assets/style/main.module.css"></style>

<style scoped>
.v-card-center {
    text-align: center;
}
</style>