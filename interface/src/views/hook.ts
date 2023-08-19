export type HookType = {
    time: number,
    f: Function,
    executed: boolean,
}

export const hooks: HookType[] = [];

export const AddHook = (time: number, f: Function): void => {
    hooks.push({ time, f, executed: false });
};

export const ExecuteHook = (time: number): void => {
    for (const hook of hooks) {
        if (hook.time <= time + 1 && hook.time >= time && !hook.executed) {
            hook.executed = true;
            hook.f();
        }
    }
};

export const InitHook = (): void => {
    for (const i in hooks) {
        hooks[i].executed = false;
    }
};