import { AbsoluteFill, useCurrentFrame } from "remotion";
import { brand } from "../brand";
import { PAPEL, PAPER_EDGE, isPapel } from "../theme";

const { colors } = brand;

// Papel milimetrado azul que se desplaza muy despacio.
export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  if (isPapel()) return <PaperBackground frame={frame} />;
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

// Cartulina cálida con fibras, luz suave y dos recortes de papel en los bordes (estilo papel).
const PaperBackground: React.FC<{ frame: number }> = ({ frame }) => {
  const drift = Math.sin(frame / 90) * 6;
  return (
    <AbsoluteFill style={{ backgroundColor: PAPEL.hueso }}>
      <AbsoluteFill>
        <svg width="100%" height="100%">
          <rect width="100%" height="100%" filter="url(#ui-papel-fibras)" opacity={0.55} />
        </svg>
      </AbsoluteFill>
      <div style={{ position: "absolute", left: -120, top: 1540 + drift, width: 1400, height: 520, background: PAPEL.carton, opacity: 0.55, transform: "rotate(-4deg)", filter: `url(#${PAPER_EDGE})` }} />
      <div style={{ position: "absolute", right: -160, top: -260 - drift, width: 620, height: 420, background: PAPEL.crema, opacity: 0.7, transform: "rotate(9deg)", filter: `url(#${PAPER_EDGE})` }} />
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 80% 55% at 50% 40%, rgba(255,250,240,0.45), transparent 70%), radial-gradient(ellipse 130% 90% at 50% 50%, transparent 55%, rgba(185,132,87,0.22))`,
        }}
      />
    </AbsoluteFill>
  );
};
