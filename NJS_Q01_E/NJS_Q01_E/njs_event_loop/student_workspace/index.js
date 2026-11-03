// TODO: Wrap these logs inside the appropriate Event Loop hooks (setTimeout, setImmediate, process.nextTick, and Promise callbacks)
// to make them output in the correct execution order: "start" -> "end" -> "nextTick" -> "promise" -> "timeout" -> "immediate"

console.log("start");

console.log("timeout");

console.log("immediate");

console.log("promise");

console.log("nextTick");

console.log("end");
