import { Easing, interpolate, spring } from "remotion";
import { FPS } from "./brand";

export const sec = (s: number) => Math.round(s * FPS);

/** Spring de entrada "pop" algo elástica. */
export const pop = (frame: number, delay = 0, damping = 11, mass = 0.6) =>
  spring({ frame: frame - delay, fps: FPS, config: { damping, mass, stiffness: 170 } });

/** Spring suave sin rebote. */
export const smooth = (frame: number, delay = 0, durationInFrames = 14) =>
  spring({ frame: frame - delay, fps: FPS, durationInFrames, config: { damping: 200 } });

/** 1 → 0 durante los últimos `len` frames antes de `endFrame`. */
export const exitOut = (frame: number, endFrame: number, len = 7) =>
  interpolate(frame, [endFrame - len, endFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.in(Easing.cubic),
  });

export const clamp01 = (v: number) => Math.max(0, Math.min(1, v));

/** Pseudo-aleatorio estable a partir de una cadena (para rotaciones "a mano"). */
export const seeded = (key: string) => {
  let h = 2166136261;
  for (let i = 0; i < key.length; i++) h = Math.imul(h ^ key.charCodeAt(i), 16777619);
  return ((h >>> 0) % 10000) / 10000;
};

/** Divide "texto con *resaltado*" en trozos. */
export const parseMarkup = (s: string) =>
  s.split(/(\*[^*]+\*)/g).filter(Boolean).map((t) =>
    t.startsWith("*") && t.endsWith("*") ? { text: t.slice(1, -1), hi: true } : { text: t, hi: false },
  );

export const formatNumber = (v: number, decimals = 0) =>
  v.toLocaleString("es-ES", { minimumFractionDigits: decimals, maximumFractionDigits: decimals, useGrouping: Math.abs(v) >= 10000 ? true : "min2" } as Intl.NumberFormatOptions);
