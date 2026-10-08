import { interpolate, useCurrentFrame } from "remotion";
import { brand } from "../brand";
import { exitOut, parseMarkup, pop, sec } from "../anim";

const { colors, fonts, border } = brand;

// Titular de escena: número de capítulo en bloque lima + palabras que entran escalonadas.
export const Headline: React.FC<{ text: string; number?: string | null; start: number; end: number; isLast: boolean }> = ({
  text, number, start, end, isLast,
}) => {
  const frame = useCurrentFrame();
  const f = frame - sec(start);
  const out = isLast ? 1 : exitOut(frame, sec(end), 6);
  const parts = parseMarkup(text.toUpperCase());

  // Las palabras normales entran una a una; un *resaltado* entra como un único bloque.
  let idx = 0;
  const tokens: { word: string; hi: boolean; i: number }[] = [];
  for (const p of parts) {
    if (p.hi) tokens.push({ word: p.text.trim(), hi: true, i: idx++ });
    else for (const w of p.text.split(/\s+/).filter(Boolean)) tokens.push({ word: w, hi: false, i: idx++ });
  }
  const letters = tokens.reduce((n, t) => n + t.word.length, 0);
  const size = letters > 22 ? 70 : 84;
  const numIn = pop(f, 0, 9);

  return (
    <div
      style={{
        display: "flex",
        gap: 22,
        alignItems: "flex-start",
        opacity: out,
        transform: `translateY(${interpolate(out, [0, 1], [-30, 0])}px)`,
      }}
    >
      {number && (
        <div
          style={{
            flexShrink: 0,
            minWidth: size * 1.15,
            height: size * 1.15,
            padding: "0 12px",
            background: colors.accent,
            border: `${border}px solid ${colors.ink}`,
            boxShadow: `8px 8px 0 ${colors.ink}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: fonts.display,
            fontWeight: 900,
            fontSize: size * 0.82,
            color: colors.ink,
            transform: `scale(${numIn}) rotate(${interpolate(numIn, [0, 1], [-25, -3])}deg)`,
          }}
        >
          {number}
        </div>
      )}
      <div style={{ display: "flex", flexWrap: "wrap", columnGap: size * 0.28, rowGap: 8, lineHeight: 1.08 }}>
        {tokens.map(({ word, hi, i }) => {
          const s = pop(f, 2 + i * 2.5, 12);
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                fontFamily: fonts.display,
                fontWeight: 900,
                fontSize: size,
                letterSpacing: -1,
                color: hi ? colors.ink : colors.paper,
                background: hi ? colors.accent : "transparent",
                padding: hi ? "2px 14px 6px" : 0,
                border: hi ? `${border - 1}px solid ${colors.ink}` : undefined,
                boxShadow: hi ? `7px 7px 0 ${colors.ink}` : undefined,
                textShadow: hi ? undefined : `5px 5px 0 ${colors.ink}`,
                opacity: Math.min(1, s * 1.5),
                transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px) rotate(${hi ? -2 : 0}deg)`,
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
