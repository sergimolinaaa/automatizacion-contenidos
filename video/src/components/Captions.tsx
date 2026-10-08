import { interpolate, useCurrentFrame } from "remotion";
import { FPS, PAD, brand } from "../brand";
import { pop, sec } from "../anim";
import type { Word } from "../types";

const { colors, fonts } = brand;
const MAX_WORDS = 4;

/** Agrupa palabras en frases cortas, cortando tras puntuación o pausas. */
export const groupLines = (words: Word[]) => {
  const lines: Word[][] = [];
  let cur: Word[] = [];
  words.forEach((w, i) => {
    cur.push(w);
    const next = words[i + 1];
    const pause = next ? next.start - w.end > 0.35 : true;
    if (cur.length >= MAX_WORDS || /[.,!?;:…]$/.test(w.text) || pause) {
      lines.push(cur);
      cur = [];
    }
  });
  if (cur.length) lines.push(cur);
  return lines;
};

// Subtítulos karaoke: la palabra que suena va en bloque lima; las siguientes, tenues.
export const Captions: React.FC<{ words: Word[] }> = ({ words }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const lines = groupLines(words);
  const li = lines.findIndex((l, i) => {
    const nextStart = lines[i + 1]?.[0].start ?? Infinity;
    return t >= l[0].start - 0.05 && t < nextStart - 0.05;
  });
  if (li < 0) return null;
  const line = lines[li];
  const lineIn = pop(frame - sec(line[0].start - 0.05), 0, 14);
  const lastEnd = line[line.length - 1].end;
  const fade = interpolate(t, [lastEnd + 0.6, lastEnd + 0.8], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div
      style={{
        position: "absolute",
        top: 1350,
        left: PAD,
        right: PAD,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "center",
        columnGap: 14,
        rowGap: 10,
        opacity: fade,
        transform: `translateY(${interpolate(lineIn, [0, 1], [24, 0])}px)`,
      }}
    >
      {line.map((w, i) => {
        const next = line[i + 1];
        const active = t >= w.start && (next ? t < next.start : t < lastEnd + 0.6);
        const past = t >= w.end && !active;
        const hit = pop(frame - sec(w.start), 0, 10);
        return (
          <span
            key={i}
            style={{
              fontFamily: fonts.display,
              fontWeight: 800,
              fontSize: 54,
              padding: "4px 12px 8px",
              borderRadius: 8,
              color: active ? colors.ink : past ? colors.paper : colors.muted,
              background: active ? colors.accent : "transparent",
              border: `4px solid ${active ? colors.ink : "transparent"}`,
              boxShadow: active ? `6px 6px 0 ${colors.ink}` : undefined,
              textShadow: active ? undefined : past ? `4px 4px 0 ${colors.ink}` : undefined,
              transform: active ? `scale(${interpolate(hit, [0, 1], [0.86, 1])}) rotate(-1.5deg)` : undefined,
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
