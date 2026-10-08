import { interpolate, useCurrentFrame } from "remotion";
import { brand } from "../brand";
import { pop, seeded } from "../anim";
import type { Pose } from "../types";

const { colors } = brand;
const INK = colors.ink;

type Arm = { shoulder: number; elbow: number }; // grados desde "colgando hacia abajo", positivo = hacia fuera

const UPPER = 58;
const LOWER = 50;

function armPoints(sx: number, sy: number, side: -1 | 1, a: Arm) {
  const r1 = ((a.shoulder) * Math.PI) / 180;
  const ex = sx + side * Math.sin(r1) * UPPER;
  const ey = sy + Math.cos(r1) * UPPER;
  const r2 = ((a.shoulder + a.elbow) * Math.PI) / 180;
  const hx = ex + side * Math.sin(r2) * LOWER;
  const hy = ey + Math.cos(r2) * LOWER;
  return { ex, ey, hx, hy };
}

function poseArms(pose: Pose, t: number, toward: -1 | 1): { L: Arm; R: Arm } {
  const swing = Math.sin(t * 2.2) * 6;
  const pointArm: Arm = { shoulder: 92 + Math.sin(t * 3) * 3, elbow: -4 };
  const restArm: Arm = { shoulder: 36 + swing, elbow: -30 };
  switch (pose) {
    case "point":
      return toward === -1 ? { L: pointArm, R: restArm } : { L: restArm, R: pointArm };
    case "wave": {
      const wave: Arm = { shoulder: 150, elbow: 20 + Math.sin(t * 12) * 28 };
      return toward === -1 ? { L: restArm, R: wave } : { L: wave, R: restArm };
    }
    case "think":
      return { L: { shoulder: 35, elbow: 125 }, R: { shoulder: 30, elbow: -95 } };
    case "surprise":
      return { L: { shoulder: 140, elbow: 25 }, R: { shoulder: 140, elbow: 25 } };
    case "explain": {
      const k = Math.sin(t * 4);
      return { L: { shoulder: 70 + k * 12, elbow: -40 }, R: { shoulder: 70 - k * 12, elbow: -40 } };
    }
    case "cheer": {
      const k = Math.abs(Math.sin(t * 6));
      return { L: { shoulder: 150 + k * 15, elbow: 5 }, R: { shoulder: 150 + k * 15, elbow: 5 } };
    }
    default:
      return { L: { shoulder: 14 + swing, elbow: -10 }, R: { shoulder: 14 - swing, elbow: -10 } };
  }
}

// "Matra": un matraz Erlenmeyer con ojos, brazos y piernas. Habla cuando suena la voz.
export const Mascot: React.FC<{
  pose: Pose;
  toward: -1 | 1;
  look: "left" | "right" | "up" | "down" | "center";
  talking: number; // 0-1, apertura de boca
  poseFrame: number; // frames desde el último cambio de pose
  scale?: number;
}> = ({ pose, toward, look, talking, poseFrame, scale = 1 }) => {
  const frame = useCurrentFrame();
  const t = frame / 30;

  // parpadeo cada ~3,2 s con algo de variación
  const cycle = frame % 97;
  const blink = cycle < 5 ? Math.abs(Math.sin((cycle / 5) * Math.PI)) : 0;
  const eyeOpen = 1 - blink * 0.92;

  const react = pop(poseFrame, 0, 8, 0.5); // pequeño "salto" al cambiar de pose
  const jump = pose === "surprise" || pose === "cheer" ? Math.sin(Math.min(1, poseFrame / 10) * Math.PI) * 26 : 0;
  const bob = Math.sin(t * 2.4) * 6;
  const squash = interpolate(react, [0, 0.6, 1], [0.88, 1.06, 1], { extrapolateRight: "clamp" });

  const arms = poseArms(pose, t, toward);
  const L = armPoints(78, 252, -1, arms.L);
  const R = armPoints(222, 252, 1, arms.R);

  const lookOff = { left: [-7, 0], right: [7, 0], up: [0, -7], down: [0, 6], center: [0, 0] }[look];
  const pupil = (pose === "point" ? [toward * 7, 0] : lookOff) as number[];
  const eyeR = pose === "surprise" ? 25 : 21;
  const brow = pose === "think" ? -8 : pose === "surprise" ? -14 : pose === "cheer" ? -10 : 0;

  // superficie del líquido ondulante
  const waveY = (x: number) => 268 + Math.sin(x / 22 + t * 4) * 5;
  let liquid = `M 40 ${waveY(40)}`;
  for (let x = 40; x <= 260; x += 10) liquid += ` L ${x} ${waveY(x)}`;
  liquid += " L 260 400 L 40 400 Z";

  const bubbles = Array.from({ length: 6 }, (_, i) => {
    const speed = 0.35 + seeded(`b${i}`) * 0.4;
    const p = ((t * speed + seeded(`o${i}`)) % 1);
    return { x: 95 + seeded(`x${i}`) * 110 + Math.sin(t * 3 + i) * 4, y: 340 - p * 90, r: 4 + seeded(`r${i}`) * 6, o: p < 0.85 ? 1 : (1 - p) / 0.15 };
  });
  const vapor = Array.from({ length: 3 }, (_, i) => {
    const p = ((t * 0.5 + i / 3) % 1);
    return { x: 150 + Math.sin(t * 2 + i * 2) * 14, y: 22 - p * 70, r: 6 + p * 10, o: 1 - p };
  });

  const mouthOpen = Math.max(0.15, talking);

  return (
    <svg
      width={300 * scale}
      height={440 * scale}
      viewBox="0 -60 300 500"
      style={{
        overflow: "visible",
        transform: `translateY(${bob - jump}px) scale(${2 - squash}, ${squash})`,
        transformOrigin: "50% 100%",
      }}
    >
      <defs>
        <clipPath id="flask">
          <path d="M 122 120 L 122 160 L 52 318 Q 40 350 72 352 L 228 352 Q 260 350 248 318 L 178 160 L 178 120 Z" />
        </clipPath>
      </defs>
      {/* vapor */}
      {vapor.map((v, i) => (
        <circle key={i} cx={v.x} cy={v.y + 60} r={v.r} fill="none" stroke={colors.paper} strokeWidth={4} opacity={v.o * 0.7} />
      ))}
      {/* piernas */}
      <g stroke={INK} strokeWidth={13} strokeLinecap="round" fill="none">
        <path d={`M 118 350 L ${112 - Math.sin(t * 2.4) * 2} 410`} />
        <path d={`M 182 350 L ${188 + Math.sin(t * 2.4) * 2} 410`} />
      </g>
      <ellipse cx={104} cy={414} rx={22} ry={11} fill={INK} />
      <ellipse cx={196} cy={414} rx={22} ry={11} fill={INK} />
      {/* brazos (detrás del cuerpo) */}
      <g stroke={INK} strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" fill="none">
        <path d={`M 78 252 L ${L.ex} ${L.ey} L ${L.hx} ${L.hy}`} />
        <path d={`M 222 252 L ${R.ex} ${R.ey} L ${R.hx} ${R.hy}`} />
      </g>
      <circle cx={L.hx} cy={L.hy} r={12} fill={INK} />
      <circle cx={R.hx} cy={R.hy} r={12} fill={INK} />
      {/* cuerpo */}
      <path
        d="M 122 120 L 122 160 L 52 318 Q 40 350 72 352 L 228 352 Q 260 350 248 318 L 178 160 L 178 120 Z"
        fill={INK}
      />
      <g clipPath="url(#flask)">
        <path d={liquid} fill={colors.accent} />
        {bubbles.map((b, i) => (
          <circle key={i} cx={b.x} cy={b.y} r={b.r} fill={INK} opacity={0.35 * b.o} />
        ))}
      </g>
      {/* borde y reflejo del vidrio */}
      <path
        d="M 122 120 L 122 160 L 52 318 Q 40 350 72 352 L 228 352 Q 260 350 248 318 L 178 160 L 178 120 Z"
        fill="none"
        stroke={INK}
        strokeWidth={8}
        strokeLinejoin="round"
      />
      <path d="M 84 318 L 104 274" stroke={colors.paper} strokeWidth={7} strokeLinecap="round" opacity={0.5} />
      {/* boca del matraz + tapón */}
      <rect x={112} y={108} width={76} height={18} rx={6} fill={INK} />
      <rect x={128} y={84} width={44} height={30} rx={6} fill={colors.accent} stroke={INK} strokeWidth={6} />
      {/* ojos */}
      {[128, 172].map((cx, i) => (
        <g key={i}>
          <ellipse cx={cx} cy={196} rx={eyeR * 0.82} ry={eyeR * eyeOpen} fill={colors.paper} />
          <circle cx={cx + pupil[0] * 0.9} cy={196 + pupil[1] * eyeOpen} r={9 * Math.max(0.2, eyeOpen)} fill={INK} />
          <path
            d={`M ${cx - 14} ${168 + brow + (i === 0 ? (pose === "think" ? 4 : 0) : 0)} L ${cx + 14} ${168 + brow + (i === 1 && pose === "think" ? 4 : 0)}`}
            stroke={colors.paper}
            strokeWidth={5}
            strokeLinecap="round"
          />
        </g>
      ))}
      {/* boca */}
      <ellipse cx={150} cy={236} rx={10 + mouthOpen * 4} ry={3 + mouthOpen * 10} fill={colors.paper} />
    </svg>
  );
};
