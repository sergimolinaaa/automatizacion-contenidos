import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { brand } from "../brand";
import { pop, sec } from "../anim";
import { Mascot } from "./Mascot";
import { Wordmark } from "./Signature";

const { colors, fonts } = brand;

// Cierre de marca: logotipo, mascota celebrando y llamada a seguir la cuenta.
export const Outro: React.FC<{ at: number; cta?: string }> = ({ at, cta }) => {
  const frame = useCurrentFrame();
  const f = frame - sec(at);
  if (f < 0) return null;
  const wipe = interpolate(f, [0, 9], [0, 1], { extrapolateRight: "clamp" });
  const logo = pop(f, 6, 9);
  const sub = pop(f, 14, 12);
  return (
    <AbsoluteFill style={{ clipPath: `circle(${wipe * 150}% at 50% 60%)`, backgroundColor: colors.bgDeep }}>
      <AbsoluteFill
        style={{
          backgroundImage: `radial-gradient(${colors.ink} 3px, transparent 3px)`,
          backgroundSize: "44px 44px",
          opacity: 0.35,
        }}
      />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 30, paddingBottom: 260 }}>
        <div style={{ transform: `scale(${logo}) rotate(${interpolate(logo, [0, 1], [-10, -2])}deg)` }}>
          <Wordmark size={116} f={f - 4} stagger={3} />
        </div>
        <Mascot pose="cheer" toward={1} look="center" talking={0} poseFrame={f} scale={1.1} />
        <div style={{ opacity: sub, transform: `translateY(${(1 - sub) * 30}px)`, display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
          <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 46, color: colors.paper, textShadow: `4px 4px 0 ${colors.ink}` }}>{cta ?? brand.tagline}</div>
          <div style={{ fontFamily: fonts.mono, fontWeight: 800, fontSize: 40, color: colors.ink, background: colors.accent, padding: "10px 26px", borderRadius: 12, border: `5px solid ${colors.ink}`, boxShadow: `8px 8px 0 ${colors.ink}` }}>
            {brand.handle}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
