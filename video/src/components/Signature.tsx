import { Easing, interpolate, useCurrentFrame } from "remotion";
import { brand } from "../brand";
import { exitOut, pop, sec } from "../anim";
import { Mascot } from "./Mascot";

const { colors, fonts, border } = brand;

/** Logotipo de la cuenta (palabras con o sin caja), con entrada escalonada opcional. */
export const Wordmark: React.FC<{ size: number; f: number; stagger?: number }> = ({ size, f, stagger = 3 }) => (
  <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", alignItems: "center", gap: size * 0.22, rowGap: size * 0.18 }}>
    {brand.logo.map((w, i) => {
      const s = pop(f, i * stagger, 9, 0.5);
      return (
        <div
          key={i}
          style={{
            fontFamily: fonts.display,
            fontWeight: 900,
            fontSize: size,
            lineHeight: 1,
            letterSpacing: -2,
            color: w.boxed ? colors.ink : colors.paper,
            background: w.boxed ? colors.accent : "transparent",
            padding: w.boxed ? `${size * 0.06}px ${size * 0.18}px ${size * 0.12}px` : 0,
            border: w.boxed ? `${border + 2}px solid ${colors.ink}` : undefined,
            boxShadow: w.boxed ? `10px 10px 0 ${colors.ink}` : undefined,
            textShadow: w.boxed ? undefined : `7px 7px 0 ${colors.ink}`,
            opacity: Math.min(1, s * 2),
            transform: `translateY(${interpolate(s, [0, 1], [-120, 0])}px) scale(${interpolate(s, [0, 1], [1.4, 1])}) rotate(${w.boxed ? -4 : 0}deg)`,
          }}
        >
          {w.text}
        </div>
      );
    })}
  </div>
);

// Escena-firma: rayos de fondo, letras que caen una a una, «ES…» que golpea con sus puntos rebotando,
// chispas que salen disparadas y el matraz que salta. Corta (1-1,5 s) y muy llamativa.
export const Signature: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame();
  const f = frame - sec(start);
  const out = exitOut(frame, sec(end), 5);
  const slam = 9;
  const shake = f >= slam && f < slam + 7 ? Math.sin((f - slam) * 3.2) * (slam + 7 - f) * 2.2 : 0;
  const rays = interpolate(f, [0, 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const letters = "EL TRUCO".split("");
  const box = pop(f, slam, 8, 0.5);
  const jump = pop(f, 6, 9, 0.6);
  return (
    <div style={{ position: "relative", height: 1060, overflow: "hidden", opacity: out, transform: `translate(${shake}px, ${shake * 0.4}px)` }}>
      {/* rayos giratorios */}
      <svg viewBox="-500 -500 1000 1000" style={{ position: "absolute", left: "50%", top: 330, width: 1500, height: 1500, marginLeft: -750, marginTop: -750, opacity: rays * 0.9 }}>
        <g transform={`rotate(${f * 1.5}) scale(${0.4 + 0.6 * rays})`}>
          {Array.from({ length: 16 }).map((_, i) => (
            <path key={i} d="M 0 0 L -38 -520 L 38 -520 Z" fill={i % 2 ? colors.accent : colors.paper} opacity={i % 2 ? 0.22 : 0.08} transform={`rotate(${i * 22.5})`} />
          ))}
        </g>
      </svg>
      {/* chispas */}
      {Array.from({ length: 10 }).map((_, i) => {
        const ang = (i / 10) * Math.PI * 2 + 0.3;
        const p = interpolate(f, [slam, slam + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
        const r = 120 + p * (330 + (i % 3) * 60);
        return (
          <div key={i} style={{
            position: "absolute", left: 500 + Math.cos(ang) * r - 14, top: 330 + Math.sin(ang) * r * 0.75 - 14, width: 28, height: 28,
            background: i % 2 ? colors.accent : colors.paper, border: `5px solid ${colors.ink}`, borderRadius: i % 3 === 0 ? 14 : 4,
            transform: `rotate(${f * 12 + i * 40}deg) scale(${p > 0 ? 1 - p * 0.5 : 0})`, opacity: p < 1 ? 1 : 0,
          }} />
        );
      })}
      {/* EL TRUCO, letra a letra */}
      <div style={{ position: "absolute", top: 120, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
        {letters.map((ch, i) => {
          const k = pop(f, i * 1.1, 9, 0.5);
          return (
            <span key={i} style={{
              display: "inline-block", width: ch === " " ? 40 : undefined, fontFamily: fonts.display, fontWeight: 900, fontSize: 150,
              lineHeight: 1, letterSpacing: -3, color: colors.paper, textShadow: `8px 8px 0 ${colors.ink}`,
              opacity: Math.min(1, k * 3),
              transform: `translateY(${interpolate(k, [0, 1], [-260, 0])}px) rotate(${interpolate(k, [0, 1], [(i % 2 ? 1 : -1) * 25, 0])}deg)`,
            }}>{ch}</span>
          );
        })}
      </div>
      {/* ES… que golpea */}
      <div style={{ position: "absolute", top: 300, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
        <div style={{
          display: "flex", alignItems: "baseline", fontFamily: fonts.display, fontWeight: 900, fontSize: 150, lineHeight: 1,
          color: colors.ink, background: colors.accent, border: `${border + 2}px solid ${colors.ink}`, boxShadow: `12px 12px 0 ${colors.ink}`,
          padding: "8px 34px 18px", opacity: f < slam ? 0 : 1,
          transform: `scale(${interpolate(box, [0, 1], [2.4, 1])}) rotate(${interpolate(box, [0, 1], [8, -4])}deg)`,
        }}>
          ES
          {[0, 1, 2].map((d) => {
            const b = pop(f, slam + 4 + d * 3, 7, 0.4);
            return <span key={d} style={{ display: "inline-block", opacity: b > 0.05 ? 1 : 0, transform: `translateY(${interpolate(b, [0, 1], [-60, 0])}px)` }}>.</span>;
          })}
        </div>
      </div>
      {/* el matraz salta */}
      <div style={{ position: "absolute", top: 560, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: Math.min(1, jump * 2),
        transform: `translateY(${interpolate(jump, [0, 1], [420, 0])}px) rotate(${interpolate(jump, [0, 1], [-30, 0])}deg)` }}>
        <Mascot pose="surprise" toward={1} look="center" talking={0} poseFrame={f} scale={1.1} />
      </div>
    </div>
  );
};
