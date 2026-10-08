import { AbsoluteFill } from "remotion";
import { brand } from "./brand";
import { Background } from "./components/Background";
import { Mascot } from "./components/Mascot";

const { colors } = brand;

// Foto de perfil 1080x1080: el matraz centrado (las redes recortan en círculo).
export const Profile: React.FC<{ variant: "blue" | "lime" }> = ({ variant }) => (
  <AbsoluteFill style={{ backgroundColor: colors.bg }}>
    <Background />
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {variant === "lime" && (
        <div style={{ position: "absolute", width: 930, height: 930, borderRadius: "50%", border: `34px solid ${colors.accent}`, boxShadow: `0 0 0 12px ${colors.ink}, inset 0 0 0 12px ${colors.ink}` }} />
      )}
      <div style={{ position: "absolute", top: variant === "lime" ? 110 : 70 }}>
        <Mascot pose="wave" toward={1} look="center" talking={0.3} poseFrame={30} scale={variant === "lime" ? 1.95 : 2.2} />
      </div>
    </AbsoluteFill>
  </AbsoluteFill>
);
