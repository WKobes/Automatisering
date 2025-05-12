require("./js/config.js");
const {pubDomain, shortName, publishVersion} = globalThis.respecConfig;

console.log(`${pubDomain}/${shortName}/${publishVersion}`);
