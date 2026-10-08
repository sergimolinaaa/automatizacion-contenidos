import { interpolate, useCurrentFrame } from "remotion";
import { brand } from "../brand";
import { exitOut, pop, sec } from "../anim";
import { Mascot } from "./Mascot";

const { colors, fonts, border } = brand;

/** Logotipo de la cuenta (palabras con o sin caja), con entrada escalonada opcional. */
export const Wordmark: React.FC<{ size: number; f: number; stagger?: number }> = ({ size, f, stagger = 4 }) => (
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

// Escena-firma: la pregunta que da nombre a la cuenta irrumpe en pantalla, como "¿Y a mí qué?".
export const Signature: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame();
  const f = frame - sec(start);
  const out = exitOut(frame, sec(end), 6);
  const shake = f >= 6 && f < 14 ? Math.sin(f * 3) * 8 : 0;
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 50, paddingTop: 110, opacity: out, transform: `translateX(${shake}px)` }}>
      <Wordmark size={128} f={f} />
      <Mascot pose="explain" toward={1} look="center" talking={0} poseFrame={f} scale={1.15} />
    </div>
  );
};
