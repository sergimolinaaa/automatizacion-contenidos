import { Easing, interpolate, useCurrentFrame } from "remotion";
import { brand } from "../brand";
import { pop, sec, seeded } from "../anim";
import type { Element } from "../types";

const { colors, fonts, border } = brand;
const INK = colors.ink;

/** «Tú traes las dudas y nosotros te damos el truco»: las dudas (?) aparecen y, al decir «nosotros»,
 *  se convierten en el truco. Cuatro variantes; si no se fija `variant`, cada vídeo saca una distinta. */
export const Trick: React.FC<{ el: Extract<Element, { type: "trick" }> }> = ({ el }) => {
  const frame = useCurrentFrame();
  const f = frame - sec(el.at);
  const reveal = sec(el.reveal ?? el.at + 1.3) - sec(el.at);
  const r = f - reveal; // frames desde «nosotros»
  const variant = (el.variant ?? Math.floor(seeded(`trick${el.at.toFixed(2)}`) * 4)) % 4;
  const ease = (a: number, b: number) => interpolate(r, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });

  // dudas: posiciones a la izquierda/centro, cada una con su tamaño y giro
  const qs = [
    { x: 230, y: 330, s: 1.15, rot: -12 }, { x: 420, y: 250, s: 0.9, rot: 10 }, { x: 330, y: 520, s: 1.0, rot: 6 },
    { x: 560, y: 420, s: 0.8, rot: -8 }, { x: 160, y: 560, s: 0.75, rot: 14 },
  ];
  const center = { x: 500, y: 470 };

  const chip = (x: number, y: number, text: string, on: number, tone: string) => (
    <g transform={`translate(${x} ${y}) scale(${on})`} opacity={Math.min(1, on * 2)}>
      <rect x={-text.length * 17 - 26} y={-36} width={text.length * 34 + 52} height={72} rx={14} fill={tone} stroke={INK} strokeWidth={border} />
      <text x={0} y={14} textAnchor="middle" fontFamily={fonts.display} fontWeight={900} fontSize={40} fill={INK}>{text}</text>
    </g>
  );

  const question = (q: (typeof qs)[number], i: number) => {
    const appear = f < 0 ? 0 : pop(f, i * 5, 10);
    const wob = Math.sin((frame + i * 13) / 6) * 6;
    let x = q.x, y = q.y, s = q.s * appear, op = 1, flip = 1, bang = false;
    if (variant === 0) { // se funden en el centro
      const m = ease(i * 2, 14 + i * 2);
      x = interpolate(m, [0, 1], [q.x, center.x]); y = interpolate(m, [0, 1], [q.y, center.y]);
      s *= 1 - m; op = 1 - m;
    } else if (variant === 1 || variant === 3) { // la varita / la lupa las convierte en «!» / «✓»
      const t = ease(8 + i * 4, 16 + i * 4);
      flip = Math.abs(Math.cos(t * Math.PI)); bang = t > 0.5;
    } else { // caen en la caja
      const m = ease(i * 3, 12 + i * 3);
      x = interpolate(m, [0, 1], [q.x, center.x]); y = interpolate(m, [0, 1], [q.y, 700]);
      s *= 1 - 0.6 * m; op = m >= 1 ? 0 : 1;
    }
    const sign = bang ? (variant === 1 ? "!" : "✓") : "?";
    const fill = bang ? colors.accent : i % 2 ? colors.paper : colors.hot;
    return (
      <g key={i} transform={`translate(${x} ${y + (r < 0 ? wob : 0)}) rotate(${q.rot + (r < 0 ? wob : 0)}) scale(${s * flip} ${s})`} opacity={op}>
        <circle r={78} fill={fill} stroke={INK} strokeWidth={border} />
        <text y={34} textAnchor="middle" fontFamily={fonts.display} fontWeight={900} fontSize={100} fill={INK}>{sign}</text>
      </g>
    );
  };

  const bulb = (on: number) => (
    <g transform={`translate(${center.x} ${center.y}) scale(${on})`}>
      {Array.from({ length: 12 }).map((_, k) => (
        <rect key={k} x={-9} y={-250} width={18} height={60} rx={9} fill={colors.accent} stroke={INK} strokeWidth={4}
          transform={`rotate(${k * 30 + frame * 1.5})`} />
      ))}
      <circle r={130} fill={colors.accent} stroke={INK} strokeWidth={border} />
      <ellipse cx={-45} cy={-50} rx={30} ry={45} fill="#fff" opacity={0.6} />
      <rect x={-55} y={118} width={110} height={70} rx={12} fill="#9AA0B5" stroke={INK} strokeWidth={border} />
      <path d="M -40 -10 Q 0 -60 40 -10 L 20 60 M -40 -10 L -20 60" fill="none" stroke={INK} strokeWidth={8} strokeLinecap="round" />
    </g>
  );

  const label = (on: number, y = 820) => (
    <g transform={`translate(${center.x} ${y}) rotate(-4) scale(${on})`}>
      <rect x={-250} y={-60} width={500} height={110} rx={16} fill={colors.accent} stroke={INK} strokeWidth={8} />
      <text y={22} textAnchor="middle" fontFamily={fonts.display} fontWeight={900} fontSize={70} fill={INK}>EL TRUCO</text>
    </g>
  );

  const sparkles = (cx: number, cy: number, t: number) =>
    t > 0 && t < 1 ? Array.from({ length: 10 }).map((_, k) => {
      const a = (k / 10) * Math.PI * 2; const d = 40 + t * 220;
      return <path key={k} d="M 0 -22 L 6 -6 L 22 0 L 6 6 L 0 22 L -6 6 L -22 0 L -6 -6 Z" fill={k % 2 ? colors.accent : colors.paper}
        stroke={INK} strokeWidth={3} opacity={1 - t} transform={`translate(${cx + Math.cos(a) * d} ${cy + Math.sin(a) * d}) scale(${1 - t * 0.5})`} />;
    }) : null;

  const youOn = f < 0 ? 0 : pop(f, 0, 12);
  const weOn = r < 0 ? 0 : pop(r, 0, 12);

  return (
    <div style={{ width: "100%", opacity: f < 0 ? 0 : 1 }}>
      <svg viewBox="0 0 1000 900" style={{ width: "100%", overflow: "visible" }}>
        {chip(150, 70, "TÚ", youOn, colors.paper)}
        {chip(790, 70, "NOSOTROS", weOn, colors.accent)}

        {variant === 2 && r > -6 && ( // caja
          <g transform={`translate(${center.x} 720) scale(${pop(r, -6, 12)})`}>
            <rect x={-170} y={-60} width={340} height={170} rx={10} fill="#C98B4E" stroke={INK} strokeWidth={border} />
            <rect x={-20} y={-60} width={40} height={170} fill={colors.hot} stroke={INK} strokeWidth={4} />
            <g transform={`translate(-180 -60) rotate(${-110 * ease(16, 24)})`}>
              <rect x={0} y={-40} width={360} height={40} rx={8} fill="#DDA06A" stroke={INK} strokeWidth={border} />
            </g>
          </g>
        )}

        {qs.map(question)}

        {variant === 0 && r >= 12 && bulb(pop(r, 12, 10))}
        {variant === 0 && label(r < 22 ? 0 : pop(r, 22, 11))}

        {variant === 1 && r >= 0 && ( // varita que barre las dudas
          <g transform={`translate(${interpolate(ease(0, 30), [0, 1], [1150, 560])} ${200 + 120 * Math.sin(ease(0, 30) * Math.PI)}) rotate(${-30 + 50 * ease(4, 30)})`}>
            <rect x={-12} y={0} width={24} height={300} rx={10} fill={INK} />
            <rect x={-12} y={0} width={24} height={50} rx={10} fill={colors.paper} stroke={INK} strokeWidth={4} />
            <path d="M 0 -60 L 16 -18 L 60 -18 L 24 8 L 38 50 L 0 24 L -38 50 L -24 8 L -60 -18 L -16 -18 Z" fill={colors.accent} stroke={INK} strokeWidth={5} />
          </g>
        )}
        {variant === 1 && sparkles(380, 400, interpolate(r, [8, 36], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }))}
        {variant === 1 && label(r < 30 ? 0 : pop(r, 30, 11))}

        {variant === 2 && r >= 18 && (
          <g transform={`translate(${center.x} ${interpolate(pop(r, 18, 9), [0, 1], [700, 420])})`}>
            <rect x={-230} y={-80} width={460} height={140} rx={18} fill={colors.accent} stroke={INK} strokeWidth={8} transform="rotate(-5)" />
            <text y={20} textAnchor="middle" fontFamily={fonts.display} fontWeight={900} fontSize={76} fill={INK} transform="rotate(-5)">EL TRUCO</text>
          </g>
        )}
        {variant === 2 && sparkles(center.x, 560, interpolate(r, [18, 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }))}

        {variant === 3 && r >= 0 && ( // lupa que revisa cada duda
          <g transform={`translate(${interpolate(ease(0, 34), [0, 1], [-120, 640])} ${interpolate(ease(0, 34), [0, 1], [260, 520]) + Math.sin(r / 3) * 10})`}>
            <rect x={70} y={70} width={34} height={150} rx={14} fill={INK} transform="rotate(-45 87 145)" />
            <circle r={110} fill="rgba(255,255,255,0.35)" stroke={INK} strokeWidth={14} />
            <ellipse cx={-40} cy={-40} rx={22} ry={34} fill="#fff" opacity={0.7} />
          </g>
        )}
        {variant === 3 && label(r < 32 ? 0 : pop(r, 32, 11))}
      </svg>
    </div>
  );
};
