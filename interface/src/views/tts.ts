export const TTS = (text: string, rate?: number, pitch?: number, voice?: SpeechSynthesisVoice): void => {
    if (text === "") {
        console.error("请输入一些文本");
        return;
    }

    const utterThis = new SpeechSynthesisUtterance(text);

    console.log(window.speechSynthesis.getVoices());
    window.speechSynthesis.getVoices();

    setTimeout(() => {
        // console.log(window.speechSynthesis.getVoices());

        utterThis.voice = voice || window.speechSynthesis.getVoices()[63];
        utterThis.rate = rate || 1;
        utterThis.pitch = pitch || 1;

        window.speechSynthesis.speak(utterThis);
    }, 100);

};