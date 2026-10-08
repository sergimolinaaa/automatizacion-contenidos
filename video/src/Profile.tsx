import { AbsoluteFill } from "remotion";
import { brand } from "./brand";

const { colors } = brand;
const INK = colors.ink;
const LIME = colors.accent;
const PAPER = colors.paper;

const BODY = "M 470 420 L 470 330 L 610 330 L 610 420 L 806 818 Q 836 884 768 888 L 312 888 Q 244 884 274 818 Z";

const star = (cx: number, cy: number, r: number) =>
  `M ${cx} ${cy - r} Q ${cx + r * 0.16} ${cy - r * 0.16} ${cx + r} ${cy} Q ${cx + r * 0.16} ${cy + r * 0.16} ${cx} ${cy + r} Q ${cx - r * 0.16} ${cy + r * 0.16} ${cx - r} ${cy} Q ${cx - r * 0.16} ${cy - r * 0.16} ${cx} ${cy - r} Z`;

const burst = (() => {
  const pts: string[] = [];
  for (let i = 0; i < 28; i++) {
    const a = (i / 28) * Math.PI * 2 - Math.PI / 2;
    const r = i % 2 ? 330 : 420;
    pts.push(`${(540 + Math.cos(a) * r).toFixed(1)},${(570 + Math.sin(a) * r).toFixed(1)}`);
  }
  return pts.join(" ");
})();

// Foto de perfil: el matraz "mago" (el truco es…) con chistera, varita y guiño.
export const Profile: React.FC<{ variant?: "blue" | "lime" }> = ({ variant = "blue" }) => {
  const bg = variant === "lime" ? LIME : colors.bg;
  const burstFill = variant === "lime" ? colors.bg : LIME;
  return (
    <AbsoluteFill style={{ backgroundColor: bg }}>
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        <defs>
          <clipPath id="body"><path d={BODY} /></clipPath>
          <radialGradient id="glow" cx="50%" cy="50%" r="60%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity={0.18} />
            <stop offset="100%" stopColor="#FFFFFF" stopOpacity={0} />
          </radialGradient>
          <pattern id="grid" width="45" height="45" patternUnits="userSpaceOnUse">
            <path d="M 45 0 L 0 0 0 45" fill="none" stroke="#FFFFFF" strokeOpacity={variant === "lime" ? 0 : 0.1} strokeWidth={2} />
          </pattern>
        </defs>
        <rect width={1080} height={1080} fill="url(#grid)" />
        <rect width={1080} height={1080} fill="url(#glow)" />

        {/* estallido */}
        <polygon points={burst} fill={burstFill} stroke={INK} strokeWidth={14} strokeLinejoin="round" />

        <g transform="rotate(-7 540 600)">
          {/* piernas */}
          <g stroke={INK} strokeWidth={30} strokeLinecap="round">
            <path d="M 470 880 L 458 958" />
            <path d="M 610 880 L 626 958" />
          </g>
          <ellipse cx={440} cy={966} rx={48} ry={22} fill={INK} />
          <ellipse cx={646} cy={966} rx={48} ry={22} fill={INK} />

          {/* brazo izquierdo en jarra */}
          <path d="M 330 700 L 250 640 L 300 580" stroke={INK} strokeWidth={28} strokeLinecap="round" strokeLinejoin="round" fill="none" />
          <circle cx={300} cy={580} r={27} fill={INK} />

          {/* cuerpo + líquido */}
          <path d={BODY} fill={INK} />
          <g clipPath="url(#body)">
            <path d="M 200 712 Q 300 682 400 712 T 600 712 T 800 712 T 1000 712 L 1000 950 L 200 950 Z" fill={LIME} />
            <circle cx={470} cy={800} r={20} fill={INK} opacity={0.3} />
            <circle cx={600} cy={770} r={13} fill={INK} opacity={0.3} />
            <circle cx={660} cy={835} r={24} fill={INK} opacity={0.3} />
            <circle cx={540} cy={850} r={9} fill={INK} opacity={0.3} />
          </g>
          <path d={BODY} fill="none" stroke={INK} strokeWidth={16} strokeLinejoin="round" />
          <path d="M 318 830 L 368 730" stroke={PAPER} strokeWidth={16} strokeLinecap="round" opacity={0.65} />

          {/* cara: guiño + ceja levantada + sonrisa pícara */}
          <path d="M 446 548 Q 482 520 518 548" stroke={PAPER} strokeWidth={16} strokeLinecap="round" fill="none" />
          <path d="M 444 500 L 512 512" stroke={PAPER} strokeWidth={13} strokeLinecap="round" />
          <ellipse cx={604} cy={540} rx={40} ry={46} fill={PAPER} />
          <circle cx={614} cy={548} r={21} fill={INK} />
          <circle cx={622} cy={538} r={7} fill={PAPER} />
          <path d="M 566 474 Q 606 450 648 470" stroke={PAPER} strokeWidth={13} strokeLinecap="round" fill="none" />
          <path d="M 486 616 Q 552 664 624 604" stroke={PAPER} strokeWidth={15} strokeLinecap="round" fill="none" />

          {/* tapón + chistera */}
          <rect x={486} y={292} width={108} height={46} rx={10} fill={LIME} stroke={INK} strokeWidth={12} />
          <g transform="rotate(10 540 292)">
            <rect x={452} y={118} width={176} height={168} rx={10} fill={INK} />
            <rect x={452} y={236} width={176} height={30} fill={LIME} stroke={INK} strokeWidth={8} />
            <ellipse cx={540} cy={290} rx={142} ry={26} fill={INK} />
            <path d="M 470 140 L 470 220" stroke={PAPER} strokeWidth={10} strokeLinecap="round" opacity={0.35} />
          </g>

          {/* brazo derecho con varita */}
          <path d="M 742 690 L 836 652 L 852 556" stroke={INK} strokeWidth={28} strokeLinecap="round" strokeLinejoin="round" fill="none" />
          <g transform="rotate(28 852 556)">
            <rect x={840} y={360} width={26} height={230} rx={8} fill={INK} />
            <rect x={840} y={360} width={26} height={52} rx={8} fill={PAPER} stroke={INK} strokeWidth={8} />
          </g>
          <circle cx={852} cy={560} r={30} fill={INK} />
        </g>

        {/* chispas mágicas */}
        <path d={star(924, 332, 46)} fill={PAPER} stroke={INK} strokeWidth={10} strokeLinejoin="round" />
        <path d={star(856, 236, 28)} fill={LIME} stroke={INK} strokeWidth={9} strokeLinejoin="round" />
        <path d={star(978, 452, 22)} fill={LIME} stroke={INK} strokeWidth={8} strokeLinejoin="round" />
        <circle cx={800} cy={300} r={9} fill={PAPER} stroke={INK} strokeWidth={5} />
      </svg>
    </AbsoluteFill>
  );
};
