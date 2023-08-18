import { createRouter, createWebHashHistory } from "vue-router";
import ControlPanel from "../views/ControlPanel.vue";
import ModuleManagement from "../views/ModuleManagement.vue";

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/panel",
            name: "ControlPanel",
            component: ControlPanel
        },
        {
            path: "/module",
            name: "ModuleManagement",
            component: ModuleManagement
        }
    ]
});

export default router;
