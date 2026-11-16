const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const sourceDirectory = path.resolve(
  __dirname,
  "..",
  "..",
  "Suppla",
  "suppla-api"
);
const sourcePackagePath = path.join(sourceDirectory, "package.json");
const sourceScript = "inpost:update-after-csv";

if (!fs.existsSync(sourcePackagePath)) {
  console.error(`Nie znaleziono projektu Suppla API: ${sourceDirectory}`);
  process.exit(1);
}

const sourcePackage = JSON.parse(fs.readFileSync(sourcePackagePath, "utf8"));
if (!sourcePackage.scripts || !sourcePackage.scripts[sourceScript]) {
  console.error(`Projekt Suppla API nie definiuje skryptu ${sourceScript}.`);
  process.exit(1);
}

const npmCliPath = process.env.npm_execpath;
if (!npmCliPath) {
  console.error("Uruchom tę komendę przez npm run inpost:update-after-csv.");
  process.exit(1);
}

const result = spawnSync(
  process.execPath,
  [npmCliPath, "run", sourceScript],
  { cwd: sourceDirectory, stdio: "inherit" }
);

if (result.error) {
  console.error(`Nie udało się uruchomić workflow Suppla API: ${result.error.message}`);
  process.exitCode = 1;
} else if (result.status === null) {
  console.error(`Workflow Suppla API zakończył się sygnałem ${result.signal}.`);
  process.exitCode = 1;
} else {
  process.exitCode = result.status;
}
