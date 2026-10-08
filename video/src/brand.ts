// Identidad visual de la cuenta. Cambiar aquí cambia todos los vídeos.
export const brand = {
  name: "¿Y ESO CÓMO?",
  handle: "@yesocomo",
  // Logotipo: palabras en orden; las "boxed" van en bloque lima.
  logo: [
    { text: "¿Y ESO", boxed: false },
    { text: "CÓMO?", boxed: true },
  ],
  tagline: "Lo increíble, explicado",
  colors: {
    bg: "#2347FF", // azul eléctrico de laboratorio
    bgDeep: "#1631C9",
    grid: "rgba(255,255,255,0.10)",
    gridStrong: "rgba(255,255,255,0.18)",
    ink: "#0B0B14",
    paper: "#FFFFFF",
    accent: "#C8FF2E", // lima: resaltados, líquido del matraz
    hot: "#FF5A36", // coral: FALSO, alertas
    muted: "rgba(255,255,255,0.38)",
  },
  fonts: {
    display: "Unbounded",
    mono: "JetBrains Mono",
  },
  border: 6,
  shadow: 12,
  radius: 14,
} as const;

export const W = 1080;
export const H = 1920;
export const FPS = 30;
export const PAD = 64;
