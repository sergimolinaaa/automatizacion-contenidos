import { brand } from "./brand";
import type { IconName } from "./types";

const { colors } = brand;
const S = { stroke: colors.ink, strokeWidth: 7, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, fill: "none" };
const A = colors.accent;
const I = colors.ink;

// Iconos de trazo grueso (viewBox 100x100), coherentes con la mascota.
const paths: Record<IconName, (t: number) => React.ReactNode> = {
  atom: (t) => (
    <g {...S}>
      {[0, 60, 120].map((r) => (
        <ellipse key={r} cx={50} cy={50} rx={40} ry={15} transform={`rotate(${r + t * 40} 50 50)`} />
      ))}
      <circle cx={50} cy={50} r={9} fill={A} />
    </g>
  ),
  earth: () => (
    <g {...S}>
      <circle cx={50} cy={50} r={38} fill="#5BC0FF" />
      <path d="M 26 34 Q 40 30 44 42 Q 40 56 52 60 Q 50 74 40 80 M 62 22 Q 70 36 82 40 M 60 70 Q 72 64 84 62" />
    </g>
  ),
  moon: () => (
    <g {...S}>
      <circle cx={50} cy={50} r={36} fill="#E9E9F2" />
      <circle cx={38} cy={40} r={7} /> <circle cx={62} cy={60} r={9} /> <circle cx={58} cy={32} r={4} />
    </g>
  ),
  sun: (t) => (
    <g {...S}>
      <circle cx={50} cy={50} r={20} fill={A} />
      {Array.from({ length: 8 }, (_, i) => {
        const a = (i * Math.PI) / 4 + t;
        return <line key={i} x1={50 + Math.cos(a) * 30} y1={50 + Math.sin(a) * 30} x2={50 + Math.cos(a) * 42} y2={50 + Math.sin(a) * 42} />;
      })}
    </g>
  ),
  paper: () => (
    <g {...S}>
      <path d="M 24 12 L 64 12 L 78 26 L 78 88 L 24 88 Z" fill={colors.paper} />
      <path d="M 64 12 L 64 26 L 78 26 M 34 40 L 68 40 M 34 54 L 68 54 M 34 68 L 56 68" />
    </g>
  ),
  dna: (t) => (
    <g {...S}>
      {Array.from({ length: 7 }, (_, i) => {
        const y = 14 + i * 12;
        const k = Math.sin(i * 0.9 + t * 2) * 26;
        return <line key={i} x1={50 - k} y1={y} x2={50 + k} y2={y} stroke={i % 2 ? A : I} />;
      })}
      <path d={Array.from({ length: 7 }, (_, i) => `${i ? "L" : "M"} ${50 - Math.sin(i * 0.9 + t * 2) * 26} ${14 + i * 12}`).join(" ")} />
      <path d={Array.from({ length: 7 }, (_, i) => `${i ? "L" : "M"} ${50 + Math.sin(i * 0.9 + t * 2) * 26} ${14 + i * 12}`).join(" ")} />
    </g>
  ),
  brain: () => (
    <g {...S}>
      <path d="M 50 18 Q 30 10 22 28 Q 8 36 16 54 Q 10 72 30 78 Q 40 92 50 82 Q 60 92 70 78 Q 90 72 84 54 Q 92 36 78 28 Q 70 10 50 18 Z" fill="#FFB3C7" />
      <path d="M 50 18 L 50 82 M 30 40 Q 40 44 38 56 M 70 40 Q 60 44 62 56" />
    </g>
  ),
  drop: () => <path {...S} d="M 50 10 Q 78 48 78 62 A 28 28 0 0 1 22 62 Q 22 48 50 10 Z" fill="#5BC0FF" />,
  bolt: () => <path {...S} d="M 58 8 L 24 56 L 48 56 L 40 92 L 78 40 L 54 40 Z" fill={A} />,
  rocket: () => (
    <g {...S}>
      <path d="M 50 8 Q 74 30 68 66 L 32 66 Q 26 30 50 8 Z" fill={colors.paper} />
      <circle cx={50} cy={38} r={9} fill="#5BC0FF" />
      <path d="M 32 52 L 18 72 L 34 68 M 68 52 L 82 72 L 66 68" />
      <path d="M 42 72 Q 50 96 58 72" fill={colors.hot} />
    </g>
  ),
  clock: (t) => (
    <g {...S}>
      <circle cx={50} cy={50} r={38} fill={colors.paper} />
      <line x1={50} y1={50} x2={50 + Math.sin(t) * 24} y2={50 - Math.cos(t) * 24} />
      <line x1={50} y1={50} x2={50 + Math.sin(t / 12) * 16} y2={50 - Math.cos(t / 12) * 16} />
    </g>
  ),
  eye: () => (
    <g {...S}>
      <path d="M 8 50 Q 50 10 92 50 Q 50 90 8 50 Z" fill={colors.paper} />
      <circle cx={50} cy={50} r={15} fill={A} />
      <circle cx={50} cy={50} r={6} fill={I} />
    </g>
  ),
  bacteria: (t) => (
    <g {...S}>
      <rect x={20} y={34} width={60} height={32} rx={16} fill={A} transform={`rotate(${Math.sin(t) * 8} 50 50)`} />
      <path d="M 20 50 Q 10 44 6 52 M 80 50 Q 90 56 94 48 M 40 34 Q 38 24 44 20 M 60 66 Q 62 76 56 80" />
    </g>
  ),
  star: (t) => (
    <path {...S} transform={`rotate(${t * 20} 50 50)`} fill={A}
      d="M 50 8 L 61 38 L 92 38 L 67 57 L 76 88 L 50 70 L 24 88 L 33 57 L 8 38 L 39 38 Z" />
  ),
  ruler: () => (
    <g {...S}>
      <rect x={8} y={36} width={84} height={28} rx={4} fill={A} />
      {[20, 32, 44, 56, 68, 80].map((x, i) => <line key={x} x1={x} y1={36} x2={x} y2={i % 2 ? 46 : 52} />)}
    </g>
  ),
  heart: (t) => (
    <path {...S} fill={colors.hot} transform={`scale(${1 + Math.max(0, Math.sin(t * 6)) * 0.06}) translate(${-Math.max(0, Math.sin(t * 6)) * 3} ${-Math.max(0, Math.sin(t * 6)) * 3})`}
      d="M 50 86 Q 10 58 12 34 Q 14 14 34 14 Q 46 14 50 28 Q 54 14 66 14 Q 86 14 88 34 Q 90 58 50 86 Z" />
  ),
  fire: (t) => (
    <g {...S}>
      <path d={`M 50 8 Q ${70 + Math.sin(t * 6) * 4} 34 74 56 A 24 24 0 0 1 26 56 Q 26 38 40 26 Q 42 40 50 42 Q 46 24 50 8 Z`} fill={colors.hot} />
      <path d="M 50 86 A 12 12 0 0 1 40 66 Q 46 58 50 52 Q 60 64 60 72 A 10 10 0 0 1 50 86 Z" fill={A} />
    </g>
  ),
  snow: () => (
    <g {...S}>
      {[0, 60, 120].map((r) => <line key={r} x1={50} y1={10} x2={50} y2={90} transform={`rotate(${r} 50 50)`} />)}
      <circle cx={50} cy={50} r={8} fill={colors.paper} />
    </g>
  ),
  magnet: () => (
    <g {...S}>
      <path d="M 22 20 L 22 56 A 28 28 0 0 0 78 56 L 78 20 L 60 20 L 60 56 A 10 10 0 0 1 40 56 L 40 20 Z" fill={colors.hot} />
      <path d="M 22 20 L 40 20 L 40 34 L 22 34 Z M 60 20 L 78 20 L 78 34 L 60 34 Z" fill={colors.paper} />
    </g>
  ),
  planet: (t) => (
    <g {...S}>
      <circle cx={50} cy={50} r={26} fill="#FFB86B" />
      <ellipse cx={50} cy={50} rx={46} ry={13} transform={`rotate(${-18 + Math.sin(t) * 4} 50 50)`} />
    </g>
  ),
  microscope: () => (
    <g {...S}>
      <path d="M 40 12 L 56 12 L 56 50 L 40 50 Z" fill={A} transform="rotate(-20 48 30)" />
      <path d="M 20 88 L 80 88 M 50 88 L 50 72 M 30 72 L 70 72 M 66 72 Q 78 50 60 40" />
    </g>
  ),
  leaf: () => (
    <g {...S}>
      <path d="M 18 82 Q 14 22 84 16 Q 86 80 18 82 Z" fill="#7BE07B" />
      <path d="M 18 82 L 64 36" />
    </g>
  ),
  bone: () => (
    <path {...S} fill={colors.paper}
      d="M 30 22 A 10 10 0 1 0 22 36 L 64 78 A 10 10 0 1 0 78 70 A 10 10 0 1 0 70 64 L 36 22 A 10 10 0 1 0 30 22 Z" />
  ),
  wave: (t) => (
    <path {...S} d={Array.from({ length: 21 }, (_, i) => `${i ? "L" : "M"} ${8 + i * 4.2} ${50 + Math.sin(i * 0.7 + t * 4) * 22}`).join(" ")} />
  ),
};

export const Icon: React.FC<{ name: IconName; size: number; t: number }> = ({ name, size, t }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" style={{ overflow: "visible" }}>
    {(paths[name] ?? paths.atom)(t)}
  </svg>
);
