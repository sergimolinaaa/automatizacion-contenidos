import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

const faces: [string, string, string][] = [
  ["Unbounded", "unbounded-latin-500-normal.woff2", "500"],
  ["Unbounded", "unbounded-latin-700-normal.woff2", "700"],
  ["Unbounded", "unbounded-latin-800-normal.woff2", "800"],
  ["Unbounded", "unbounded-latin-900-normal.woff2", "900"],
  ["JetBrains Mono", "jetbrains-mono-latin-500-normal.woff2", "500"],
  ["JetBrains Mono", "jetbrains-mono-latin-700-normal.woff2", "700"],
  ["JetBrains Mono", "jetbrains-mono-latin-800-normal.woff2", "800"],
];

export const fontsReady = Promise.all(
  faces.map(([family, file, weight]) =>
    loadFont({ family, url: staticFile(`fonts/${file}`), weight, format: "woff2" }),
  ),
);
