import chalk from "chalk";

const Message = {
    error: (message, from) => {
        console.log(chalk.red("[Error" + (from ? " - " + from : "") + "]") + " " + message);
    },
    info: (message) => {
        console.log(chalk.cyan("[Info]") + " " + message);
    },
    success: (message) => {
        console.log(chalk.green("[Success]") + " " + message);
    },
    warning: (message) => {
        console.log(chalk.yellow("[Warning]") + " " + message);
    },
    log: (message, from) => {
        console.log(chalk.yellow("[Log" + (from ? " - " + from : "") + "]") + " " + message);
    }
};

const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
};

(async () => {
    Message.info("Nodejs Process Started");
    Message.info("编号：Laptop 2");
    await sleep(100);
    Message.info(`运行模块：${chalk.inverse("数据平滑")}、${chalk.inverse("阵型识别")}`);
    await sleep(100);
    Message.info(`启动模块：${chalk.inverse("数据平滑")}`);
    await sleep(1000);
    Message.info(`启动成功：${chalk.inverse("数据平滑")}`);
    await sleep(100);
    Message.info(`启动模块：${chalk.inverse("阵型识别")}`);
    await sleep(1000);
    Message.error(`Cuda Error, using CPU instead.`, "Python");
    await sleep(200);
    Message.error(`Cuda Error, using CPU instead.`, "Python");
    await sleep(200);
    Message.error(`Cuda Error, using CPU instead.`, "Python");
    Message.log("Loading Model...", "Python");
    Message.log("Model Loaded.", "Python");
    await sleep(2000);
    Message.info(`启动成功：${chalk.inverse("阵型识别")}`);
    Message.info(`服务器 ${chalk.underline("ws://10.0.0.134:11451")} 已连接`);
    await sleep(100000000);
})();

process.on("SIGINT", async () => {
    Message.error("Nodejs Process Stopped");
    Message.warning(`Unmounting 模块 ${chalk.inverse("数据平滑")}`);
    await sleep(200);
    Message.warning(`Unmounting 模块 ${chalk.inverse("阵型识别")}`);
    await sleep(200);
    Message.warning("Exit Code: 0");

    process.exit();
});