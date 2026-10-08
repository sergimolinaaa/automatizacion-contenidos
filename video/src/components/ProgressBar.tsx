import { interpolate, useCurrentFrame } from "remotion";
import { FPS, PAD, brand } from "../brand";
import type { Scene } from "../types";

const { colors, fonts } = brand;

// Barra de capítulos superior: los pasados en tinta, el actual se va llenando de lima.
export const ProgressBar: React.FC<{ chapters: string[]; scenes: Scene[]; source?: string }> = ({ chapters, scenes, source }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;

  const spans = chapters.map((_, i) => {
    const own = scenes.filter((s) => s.chapter === i);
    return own.length ? { start: Math.min(...own.map((s) => s.start)), end: Math.max(...own.map((s) => s.end)) } : null;
  });
  const current = scenes.reduce((acc, s) => (t >= s.start ? s.chapter : acc), 0);

  return (
    <div style={{ position: "absolute", top: 118, left: PAD, right: PAD }}>
      <div style={{ display: "flex", gap: 10, height: 40 }}>
        {chapters.map((label, i) => {
          const span = spans[i];
          const fill = span ? interpolate(t, [span.start, span.end], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
          const past = i < current;
          const active = i === current;
          return (
            <div
              key={i}
              style={{
                flex: i === 0 ? 0.55 : 1,
                position: "relative",
                borderRadius: 8,
                border: `3px solid ${past || active ? colors.ink : "rgba(255,255,255,0.55)"}`,
                background: past ? colors.ink : "rgba(255,255,255,0.08)",
                overflow: "hidden",
                transform: active ? `translateY(${-2 * Math.sin(frame / 6)}px)` : undefined,
              }}
            >
              {active && <div style={{ position: "absolute", inset: 0, width: `${fill * 100}%`, background: colors.accent }} />}
              <div
                style={{
                  position: "relative",
                  textAlign: "center",
                  lineHeight: "34px",
                  fontFamily: fonts.mono,
                  fontWeight: 800,
                  fontSize: 20,
                  color: past ? colors.accent : active ? colors.ink : "rgba(255,255,255,0.75)",
                }}
              >
                {label}
              </div>
            </div>
          );
        })}
      </div>
      {source && (
        <div style={{ marginTop: 14, display: "flex", alignItems: "center", gap: 10, fontFamily: fonts.mono, fontWeight: 500, fontSize: 21, color: "rgba(255,255,255,0.85)" }}>
          <div style={{ width: 14, height: 14, flexShrink: 0, background: colors.accent, border: `2px solid ${colors.ink}` }} />
          <span style={{ whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{source}</span>
        </div>
      )}
    </div>
  );
};
