import { AbsoluteFill } from "remotion";
import { PAPEL, PAPER_EDGE, PAPER_EDGE_FINE } from "../theme";

const filtro = (id: string, escala: number, freq: number, seed: number, dx: number, dy: number, blur: number, op: number) => (
  <filter id={id} x="-8%" y="-8%" width="116%" height="122%" colorInterpolationFilters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency={freq} numOctaves={3} seed={seed} result="n" />
    <feDisplacementMap in="SourceGraphic" in2="n" scale={escala} xChannelSelector="R" yChannelSelector="G" result="r" />
    <feDisplacementMap in="SourceAlpha" in2="n" scale={escala} xChannelSelector="R" yChannelSelector="G" result="ra" />
    <feGaussianBlur in="ra" stdDeviation={blur} />
    <feOffset dx={dx} dy={dy} result="sb" />
    <feFlood floodColor={PAPEL.tinta} floodOpacity={op} />
    <feComposite in2="sb" operator="in" result="sh" />
    <feMerge>
      <feMergeNode in="sh" />
      <feMergeNode in="r" />
    </feMerge>
  </filter>
);

/** Filtros de papel para la interfaz (borde roto + sombra de papel levantado). Se pinta una vez por vídeo. */
export const PaperDefs: React.FC = () => (
  <svg width={0} height={0} style={{ position: "absolute" }} aria-hidden>
    <defs>
      {filtro(PAPER_EDGE, 12, 0.03, 2, 4, 9, 5, 0.38)}
      {filtro(PAPER_EDGE_FINE, 6, 0.06, 5, 2, 5, 3, 0.32)}
      <filter id="ui-papel-fibras" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.012 0.15" numOctaves={2} seed={5} />
        <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.6 -0.1" />
      </filter>
      <filter id="ui-papel-grano" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves={3} seed={9} />
        <feColorMatrix values="0 0 0 0 0.23  0 0 0 0 0.18  0 0 0 0 0.16  0 0 0 0.9 0" />
      </filter>
    </defs>
  </svg>
);

/** Hoja de papel recortado detrás de un panel o una tarjeta (el contenedor necesita `isolation: isolate`). */
export const PaperSheet: React.FC<{ color: string; fine?: boolean; radius?: number }> = ({ color, fine, radius = 6 }) => (
  <div
    style={{
      position: "absolute",
      inset: 0,
      zIndex: -1,
      background: color,
      borderRadius: radius,
      filter: `url(#${fine ? PAPER_EDGE_FINE : PAPER_EDGE})`,
    }}
  />
);

/** Grano de papel encima de todo (multiplica, muy suave). */
export const PaperGrain: React.FC<{ opacity?: number }> = ({ opacity = 0.16 }) => (
  <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "multiply", opacity }}>
    <svg width="100%" height="100%">
      <rect width="100%" height="100%" filter="url(#ui-papel-grano)" />
    </svg>
  </AbsoluteFill>
);
