import { defineStore } from "pinia";
import _ from "lodash";

export enum CurlingColor {
    red = 0,
    yellow = 1,
}

export type CurlingType = {
    color: CurlingColor,
    offsetX: number,
    offsetY: number,
};

export const useCurlingStore = defineStore("curling", {
    state: () => ({
        curlingList: [] as CurlingType[]
    }),
    actions: {
        push(color: CurlingColor, x: number, y: number): void {
            this.curlingList.push({
                color: color,
                offsetX: x,
                offsetY: y,
            });
        },
        copy() {
            return _.cloneDeep(this);
        }
    },
    getters: {
        getLength(): number {
            return this.curlingList.length;
        },
    }
});