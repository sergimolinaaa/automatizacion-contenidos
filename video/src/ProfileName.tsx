import { AbsoluteFill } from "remotion";
import { brand } from "./brand";

const { colors, fonts } = brand;

// Foto de perfil tipográfica: "EL TRUCO / ES…" apilado, legible incluso en miniatura.
export const ProfileName: React.FC<{ variant: "blue" | "lime" }> = ({ variant }) => {
  const blue = variant === "blue";
  return (
    <AbsoluteFill style={{ backgroundColor: blue ? colors.bg : colors.accent, alignItems: "center", justifyContent: "center" }}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", transform: "rotate(-4deg) translateY(-10px)" }}>
        <div
          style={{
            fontFamily: fonts.display,
            fontWeight: 900,
            fontSize: 190,
            lineHeight: 0.95,
            letterSpacing: -8,
            color: blue ? colors.paper : colors.ink,
            textShadow: blue ? `12px 12px 0 ${colors.ink}` : undefined,
          }}
        >
          EL
        </div>
        <div
          style={{
            fontFamily: fonts.display,
            fontWeight: 900,
            fontSize: 190,
            lineHeight: 0.95,
            letterSpacing: -8,
            color: blue ? colors.paper : colors.ink,
            textShadow: blue ? `12px 12px 0 ${colors.ink}` : undefined,
          }}
        >
          TRUCO
        </div>
        <div
          style={{
            marginTop: 26,
            fontFamily: fonts.display,
            fontWeight: 900,
            fontSize: 170,
            lineHeight: 1,
            letterSpacing: -6,
            padding: "6px 40px 22px",
            color: blue ? colors.ink : colors.accent,
            background: blue ? colors.accent : colors.ink,
            border: `14px solid ${colors.ink}`,
            boxShadow: `16px 16px 0 ${blue ? colors.ink : colors.bg}`,
            transform: "rotate(3deg)",
          }}
        >
          ES…
        </div>
      </div>
    </AbsoluteFill>
  );
};
