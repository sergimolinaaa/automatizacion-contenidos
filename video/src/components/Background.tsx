import { AbsoluteFill, useCurrentFrame } from "remotion";
import { brand } from "../brand";

const { colors } = brand;

// Papel milimetrado azul que se desplaza muy despacio.
export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.35) % 180;
  return (
    <AbsoluteFill style={{ backgroundColor: colors.bg }}>
      <AbsoluteFill
        style={{
          backgroundImage: [
            `linear-gradient(${colors.gridStrong} 2px, transparent 2px)`,
            `linear-gradient(90deg, ${colors.gridStrong} 2px, transparent 2px)`,
            `linear-gradient(${colors.grid} 1px, transparent 1px)`,
            `linear-gradient(90deg, ${colors.grid} 1px, transparent 1px)`,
          ].join(","),
          backgroundSize: "180px 180px, 180px 180px, 36px 36px, 36px 36px",
          backgroundPosition: `${-drift}px ${-drift * 0.5}px`,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 80% 55% at 50% 42%, rgba(255,255,255,0.10), transparent 70%), radial-gradient(ellipse 120% 80% at 50% 100%, ${colors.bgDeep}, transparent 60%)`,
        }}
      />
    </AbsoluteFill>
  );
};
