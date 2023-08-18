import { createApp } from "vue";
import { createPinia } from "pinia";

// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

import App from "./App.vue";
import router from "./router";

import "@mdi/font/css/materialdesignicons.css";

import "video.js/dist/video-js.css";

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: "mdi"
    },
    theme: {
        defaultTheme: "dark"
    }
});


const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(vuetify);
app.mount("#app");