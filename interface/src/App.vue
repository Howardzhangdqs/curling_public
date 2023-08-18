<template>
	<v-app class="root">
		<v-app-bar flat :class="$style.unselectable">
			<v-container class="fill-height d-flex align-center">

				<template v-for="link in links" :key="(link as string)">
					<router-link :to="link.router">
						<v-btn variant="text" class="router-btn">
							{{ link.name }}
						</v-btn>
					</router-link>
				</template>

				<v-spacer></v-spacer>

				<v-responsive max-width="260">
					<v-text-field density="compact" hide-details variant="solo"></v-text-field>
				</v-responsive>
			</v-container>
		</v-app-bar>

		<v-main class="bg-grey-lighten-3 main">
			<v-container>
				<router-view></router-view>
			</v-container>
		</v-main>
	</v-app>
</template>
  
<script lang="ts">

export default {
    data: () => {
        return {
            links: [{
                name: "控制面板",
                router: "panel"
            }, {
                name: "模块管理",
                router: "module"
            }],
        };
    }
};

</script>

<style module scoped src="./assets/style/main.module.css"></style>

<style scoped>
.root {
	--covery-border-radius: 8px;
}

.left-column {
	text-align: left;
}

.font-consolas {
	font-family: Consolas;
}

.covery {
	border-radius: var(--covery-border-radius);
}

.covery>img {
	width: 100%;
	height: 100%;
	border-radius: var(--covery-border-radius);
}

.float-right {
	float: right;
	color: rgb(255, 67, 67);
}

.main {
	width: 100vw;
}

.router-btn {
	color: #ccc
}
</style>