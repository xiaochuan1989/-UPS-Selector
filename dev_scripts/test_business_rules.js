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

function extractVarDecl(name) {
  const marker = `var ${name} =`;
  const start = source.indexOf(marker);
  assert(start >= 0, `未找到变量 ${name}`);

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
  throw new Error(`变量 ${name} 未找到结束分号`);
}

const names = [
  "getNextBreakerSize",
  "isTwoVoltBatteryType",
  "getBatteryCellMultiplier",
  "getBatteryMonitorSlaveCode",
  "resolveSwitchCalculationPower",
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
assert.equal(rules.getNextBreakerSize(1600), 2000);
assert.equal(rules.getNextBreakerSize(1904.8), 2000);
assert.equal(rules.getNextBreakerSize(2000), 2500);
assert.equal(rules.getNextBreakerSize(2499.9), 2500);
assert.equal(rules.getNextBreakerSize(3199.9), 3200);
assert.equal(rules.getNextBreakerSize(3999.9), 4000);
assert.throws(() => rules.getNextBreakerSize(-1), /非负/);

assert.equal(rules.getBatteryCellMultiplier("2v"), 1);
assert.equal(rules.getBatteryCellMultiplier("jyc2v"), 1);
assert.equal(rules.getBatteryCellMultiplier("jyc2vhr"), 1);
assert.equal(rules.getBatteryCellMultiplier("normal"), 6);
assert.equal(rules.getBatteryCellMultiplier("custom"), 6);
assert.equal(rules.getBatteryMonitorSlaveCode("jyc2v"), "88091146");
assert.equal(rules.getBatteryMonitorSlaveCode("jyc2vhr"), "88091146");
assert.equal(rules.getBatteryMonitorSlaveCode("jyc"), "88091145");

const switchByUps = rules.resolveSwitchCalculationPower({
  basis: "ups", loadKw: 120, upsCap: 200, pf: 0.9,
});
assert.equal(switchByUps.watts, 180000);
assert.equal(switchByUps.label, "UPS容量 × 功率因数");
const switchByLoad = rules.resolveSwitchCalculationPower({
  basis: "load", loadKw: 120, upsCap: 200, pf: 0.9,
});
assert.equal(switchByLoad.watts, 120000);
assert.equal(switchByLoad.label, "负载功率");
assert.throws(
  () => rules.resolveSwitchCalculationPower({ basis: "load", loadKw: 0, upsCap: 200, pf: 0.9 }),
  /负载功率/
);
assert.throws(
  () => rules.resolveSwitchCalculationPower({ basis: "ups", loadKw: 120, upsCap: 0, pf: 0.9 }),
  /UPS容量/
);

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

// ===== JYC HR12V 高功率电池数据校验 =====
const dataProgram = [
  extractVarDecl("BATTERY_POWER_DATA"),
  extractVarDecl("JYC_2V_BATTERY_SPECS"),
  extractFunction("expandBatteryPowerSpec"),
  "BATTERY_POWER_DATA = BATTERY_POWER_DATA.concat(JYC_2V_BATTERY_SPECS.map(expandBatteryPowerSpec));",
  extractFunction("getBatteryVoltagesForTime"),
  extractFunction("getBatteryRecommendationsByPower"),
  "globalThis.battery = { BATTERY_POWER_DATA, getBatteryVoltagesForTime, getBatteryRecommendationsByPower };",
].join("\n");
const dataContext = {};
vm.createContext(dataContext);
vm.runInContext(dataProgram, dataContext);
const { BATTERY_POWER_DATA, getBatteryVoltagesForTime, getBatteryRecommendationsByPower } = dataContext.battery;

const jycBatteries = BATTERY_POWER_DATA.filter((b) => b.category === "jyc");
assert.equal(jycBatteries.length, 13, "JYC 型号数量应为 13");

const expectedJycVolts = [1.6, 1.67, 1.7, 1.75, 1.8];
const expectedJycTimes = [5, 10, 15, 30, 60, 90, 120, 180, 300, 600];
for (const b of jycBatteries) {
  assert.ok(/^HR12V\d+W$/.test(b.model), `JYC 型号命名异常: ${b.model}`);
  assert.ok(/^\d+Ah$/.test(b.capacity), `JYC 容量格式异常: ${b.model} ${b.capacity}`);
  assert.equal(b.voltages.length, 5, `${b.model} 应有5个终止电压`);
  const volts = b.voltages.map((v) => Number(v.endVoltage)).sort((a, c) => a - c);
  // 注意：vm 上下文里的数组与主 realm 原型不同，用 JSON 字符串比较避免跨 realm 误判
  assert.equal(JSON.stringify(volts), JSON.stringify(expectedJycVolts), `${b.model} 终止电压不匹配`);
  for (const v of b.voltages) {
    const times = v.powers.map((p) => p.time);
    assert.equal(JSON.stringify(times), JSON.stringify(expectedJycTimes), `${b.model}@${v.endVoltage}V 时间点不匹配`);
    for (const p of v.powers) {
      assert.ok(Number.isFinite(p.power) && p.power > 0, `${b.model}@${v.endVoltage}V ${p.time}min 功率无效`);
    }
    for (let i = 1; i < v.powers.length; i += 1) {
      assert.ok(
        v.powers[i].power < v.powers[i - 1].power,
        `${b.model}@${v.endVoltage}V 恒功率应随时间严格递减`
      );
    }
  }
}

// 抽样核对数据表原值（HR12V430W @1.75V/30min = 250W）
const sampleBattery = jycBatteries.find((b) => b.model === "HR12V430W");
const samplePower = sampleBattery.voltages
  .find((v) => Math.abs(v.endVoltage - 1.75) < 0.01)
  .powers.find((p) => p.time === 30).power;
assert.equal(samplePower, 250, "HR12V430W@1.75V/30min 应为 250W");

// 推荐链路必须包含 jyc 分类并能按单体功率选出满足型号
const jycRec = getBatteryRecommendationsByPower(200, 1.75, 30);
assert.ok(jycRec.jyc, "推荐结果应包含 jyc 分类桶");
assert.ok(jycRec.jyc.suitable.length > 0, "200W/单体应能在 JYC 中找到满足型号");
assert.ok(jycRec.jyc.suitable[0].power >= 200, "JYC 首选型号恒功率应满足所需功率");

console.log("✅ JYC HR12V 高功率电池数据校验通过（13型号 / 结构 / 单调性 / 推荐链路）");

// ===== JYC 2V 常规与高倍率电池数据校验 =====
const jyc2vBatteries = BATTERY_POWER_DATA.filter((b) => b.category === "jyc2v");
const jyc2vHrBatteries = BATTERY_POWER_DATA.filter((b) => b.category === "jyc2vhr");
assert.equal(BATTERY_POWER_DATA.length, 91, "电池恒功率型号总数应为 91");
assert.equal(jyc2vBatteries.length, 10, "JYC-GFM-2V 型号数量应为 10");
assert.equal(jyc2vHrBatteries.length, 6, "JYC-HR-2V 高倍率型号数量应为 6");
assert.equal(JSON.stringify(jyc2vBatteries.map((b) => b.model)), JSON.stringify([
  "GFM-100", "GFM-200", "GFM-300", "GFM-400", "GFM-500",
  "GFM-600", "GFM-800", "GFM-1000", "GFM-1500", "GFM-2000",
]));
assert.equal(JSON.stringify(jyc2vHrBatteries.map((b) => b.model)), JSON.stringify([
  "HR-2V500W", "HR-2V750W", "HR-2V1000W", "HR-2V1200W", "HR-2V1500W", "HR-2V2000W",
]));

for (const battery of [...jyc2vBatteries, ...jyc2vHrBatteries]) {
  for (const voltage of battery.voltages) {
    for (const point of voltage.powers) {
      assert.ok(Number.isFinite(point.power) && point.power > 0, `${battery.model} 恒功率必须为正数`);
    }
    for (let index = 1; index < voltage.powers.length; index += 1) {
      assert.ok(
        voltage.powers[index].power < voltage.powers[index - 1].power,
        `${battery.model}@${voltage.endVoltage}V 恒功率应随时间严格递减`
      );
    }
  }
}

const hr500 = jyc2vHrBatteries.find((b) => b.model === "HR-2V500W");
assert.equal(hr500.voltages.find((v) => v.endVoltage === 1.75).powers.find((p) => p.time === 30).power, 321);
const gfm1000 = jyc2vBatteries.find((b) => b.model === "GFM-1000");
assert.equal(gfm1000.voltages.find((v) => v.endVoltage === 1.8).powers.find((p) => p.time === 120).power, 636);
const gfm200 = jyc2vBatteries.find((b) => b.model === "GFM-200");
assert.match(gfm200.sourceNote, /GFM-100.*完全相同.*厂家复核/);

assert.equal(JSON.stringify(getBatteryVoltagesForTime("jyc2v", 120)), JSON.stringify([1.8]));
assert.equal(JSON.stringify(getBatteryVoltagesForTime("jyc2vhr", 30)), JSON.stringify([1.65, 1.7, 1.75, 1.8]));
const jyc2vRec = getBatteryRecommendationsByPower(900, 1.75, 60);
assert.equal(jyc2vRec.jyc2v.suitable[0].model, "GFM-1000");
const jyc2vHrRec = getBatteryRecommendationsByPower(700, 1.75, 30);
assert.equal(jyc2vHrRec.jyc2vhr.suitable[0].model, "HR-2V1200W");

console.log("✅ JYC 2V 电池数据校验通过（10款GFM + 6款HR / 稀疏曲线 / 推荐链路 / 数据源风险）");
