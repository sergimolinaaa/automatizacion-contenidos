import { interpolate, useCurrentFrame } from "remotion";
import { FPS, brand } from "../brand";
import { pop, sec } from "../anim";
import type { MascotCameo } from "../types";
import { Mascot } from "./Mascot";

const { colors, fonts, border, shadow } = brand;
export const CAMEO_H = 330;

// El matraz entra desde abajo a hacer una anotación con su bocadillo. Tiene su propia franja: no tapa nada.
export const Cameo: React.FC<{ cameo: MascotCameo; sceneEnd: number; talking: number; width: number }> = ({ cameo, sceneEnd, talking, width }) => {
  const frame = useCurrentFrame();
  const until = cameo.until ?? sceneEnd;
  const f = frame - sec(cameo.at);
  if (f < 0 || frame > sec(until) + 8) return null;
  const inP = pop(f, 0, 12);
  const outP = interpolate(frame, [sec(until) - 2, sec(until) + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const y = (1 - inP) * CAMEO_H + outP * CAMEO_H;
  const bubble = pop(f, 7, 11) * (1 - outP);
  const side = cameo.side ?? "right";
  const toward: -1 | 1 = side === "right" ? -1 : 1;
  const mascotW = 240;

  return (
    <div style={{ position: "relative", height: CAMEO_H, width, overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          bottom: 0,
          [side]: 0,
          width: mascotW,
          transform: `translateY(${y}px)`,
        }}
      >
        <Mascot pose={cameo.pose ?? "point"} toward={toward} look={side === "right" ? "left" : "right"} talking={talking} poseFrame={f} scale={0.72} />
      </div>
      {cameo.note && (
        <div
          style={{
            position: "absolute",
            top: 40,
            [side === "right" ? "right" : "left"]: mascotW + 10,
            [side === "right" ? "left" : "right"]: 0,
            display: "flex",
            justifyContent: side === "right" ? "flex-end" : "flex-start",
          }}
        >
          <div
            style={{
              position: "relative",
              maxWidth: width - mascotW - 30,
              background: colors.paper,
              border: `${border}px solid ${colors.ink}`,
              boxShadow: `${shadow}px ${shadow}px 0 ${colors.ink}`,
              borderRadius: 22,
              padding: "20px 26px",
              fontFamily: fonts.display,
              fontWeight: 800,
              fontSize: 38,
              lineHeight: 1.15,
              color: colors.ink,
              opacity: Math.min(1, bubble * 2),
              transform: `scale(${bubble})`,
              transformOrigin: side === "right" ? "100% 70%" : "0% 70%",
            }}
          >
            <div style={{ fontFamily: fonts.mono, fontSize: 20, fontWeight: 800, letterSpacing: 1, color: colors.bg, marginBottom: 6 }}>
              NOTA DEL MATRAZ
            </div>
            {cameo.note}
            <div
              style={{
                position: "absolute",
                bottom: 26,
                [side === "right" ? "right" : "left"]: -26,
                width: 0,
                height: 0,
                borderTop: "16px solid transparent",
                borderBottom: "16px solid transparent",
                [side === "right" ? "borderLeft" : "borderRight"]: `24px solid ${colors.ink}`,
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export const cameoVisible = (cameo: MascotCameo | null | undefined, sceneEnd: number, t: number) =>
  !!cameo && t >= cameo.at - 0.001 && t <= (cameo.until ?? sceneEnd) + 8 / FPS;
