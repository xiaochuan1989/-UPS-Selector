#!/usr/bin/env node
"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const projectRoot = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(projectRoot, "index.html"), "utf8");

function extractFunction(name) {
  const pattern = new RegExp(`function\\s+${name}\\s*\\([^)]*\\)\\s*\\{`);
  const match = pattern.exec(source);
  assert(match, `未找到函数 ${name}`);

  let depth = 1;
  let index = match.index + match[0].length;
  let quote = null;
  let escaped = false;
  while (index < source.length && depth > 0) {
    const char = source[index];
    if (quote) {
      if (escaped) escaped = false;
      else if (char === "\\") escaped = true;
      else if (char === quote) quote = null;
    } else if (char === "'" || char === '"' || char === "`") {
      quote = char;
    } else if (char === "{") {
      depth += 1;
    } else if (char === "}") {
      depth -= 1;
    }
    index += 1;
  }
  assert.equal(depth, 0, `函数 ${name} 花括号不平衡`);
  return source.slice(match.index, index);
}

function extractConst(name) {
  const marker = `const ${name} =`;
  const start = source.indexOf(marker);
  assert(start >= 0, `未找到常量 ${name}`);

  let index = start + marker.length;
  let quote = null;
  let escaped = false;
  let round = 0;
  let square = 0;
  let curly = 0;
  while (index < source.length) {
    const char = source[index];
    if (quote) {
      if (escaped) escaped = false;
      else if (char === "\\") escaped = true;
      else if (char === quote) quote = null;
    } else if (char === "'" || char === '"' || char === "`") {
      quote = char;
    } else if (char === "(") round += 1;
    else if (char === ")") round -= 1;
    else if (char === "[") square += 1;
    else if (char === "]") square -= 1;
    else if (char === "{") curly += 1;
    else if (char === "}") curly -= 1;
    else if (char === ";" && round === 0 && square === 0 && curly === 0) {
      return source.slice(start, index + 1);
    }
    index += 1;
  }
  throw new Error(`常量 ${name} 未找到结束分号`);
}

const names = [
  "getNextBreakerSize",
  "getBatteryCellMultiplier",
  "calculateBatteryElectricals",
  "selectCurrentSensor",
  "getVoltLevel",
];
const program = [
  extractConst("STANDARD_BREAKER_SIZES"),
  extractConst("CURRENT_SENSOR_OPTIONS"),
  ...names.map(extractFunction),
  `globalThis.rules = { ${names.join(", ")} };`,
].join("\n");

const context = {};
vm.createContext(context);
vm.runInContext(program, context);
const rules = context.rules;

assert.equal(rules.getNextBreakerSize(62), 63);
assert.equal(rules.getNextBreakerSize(63), 80);
assert.equal(rules.getNextBreakerSize(100), 125);
assert.equal(rules.getNextBreakerSize(2000), 1600);
assert.throws(() => rules.getNextBreakerSize(-1), /非负/);

assert.equal(rules.getBatteryCellMultiplier("2v"), 1);
assert.equal(rules.getBatteryCellMultiplier("normal"), 6);
assert.equal(rules.getBatteryCellMultiplier("custom"), 6);

const twoGroups = rules.calculateBatteryElectricals({
  loadW: 180000,
  switchW: 180000,
  cellsPerGroup: 32,
  groups: 2,
  battType: "normal",
  endV: 1.75,
  eff: 0.95,
});
assert.ok(Math.abs(twoGroups.reqPower - 493.4210526) < 1e-6);
assert.ok(Math.abs(twoGroups.maxCurrent - 563.9097744) < 1e-6);
assert.equal(twoGroups.groupCurrent, twoGroups.maxCurrent);
assert.equal(twoGroups.sensorCurrent, twoGroups.groupCurrent);

const oneGroup = rules.calculateBatteryElectricals({
  loadW: 90000,
  switchW: 90000,
  cellsPerGroup: 32,
  groups: 1,
  battType: "2v",
  endV: 1.75,
  eff: 0.95,
});
assert.equal(oneGroup.groupCurrent, 0);
assert.equal(oneGroup.sensorCurrent, oneGroup.maxCurrent);
assert.throws(
  () => rules.calculateBatteryElectricals({
    loadW: 1, switchW: 1, cellsPerGroup: 0, groups: 1,
    battType: "normal", endV: 1.75, eff: 0.95,
  }),
  /cellsPerGroup/
);

assert.equal(rules.selectCurrentSensor(100).code, "88091139");
assert.equal(rules.selectCurrentSensor(100.01).code, "88091140");
assert.equal(rules.selectCurrentSensor(800).code, "88091143");
assert.equal(rules.selectCurrentSensor(801).code, "88091144");

assert.equal(rules.getVoltLevel(16, "normal").level, "250VDC");
assert.equal(rules.getVoltLevel(32, "normal").level, "500VDC");
assert.equal(rules.getVoltLevel(40, "normal").level, "750VDC");
assert.equal(rules.getVoltLevel(100, "2v").level, "250VDC");

console.log("✅ 核心业务规则测试通过（断路器、电池电气量、传感器、电压等级）");
