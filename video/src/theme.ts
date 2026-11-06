import type React from "react";
import { brand } from "./brand";

// Estilo del vídeo. "papel" (guion.json → "estilo": "papel") cambia el fondo azul con cuadrícula por cartulina
// y convierte paneles, tarjetas y textos al papel recortado. Sin el campo, todo queda exactamente como siempre.
export type Estilo = "papel" | undefined | null;

/** Paleta PAPEL de libreria/svg/papel.py (la parte que usa la interfaz). */
export const PAPEL = {
  crema: "#FBF6EC", hueso: "#F3E6CF", carton: "#E3C99A", kraft: "#C9A27A", tinta: "#3A2E2A", tintaSuave: "#6B5A50",
  coral: "#E86A4A", mostaza: "#F2C14E", lima: "#C9D86A", azulOsc: "#4B5A7A", azul: "#6FA8C8",
};

const BASE = { ...brand.colors };
const PAPEL_COLORS: Partial<Record<keyof typeof BASE, string>> = {
  bg: PAPEL.azul,
  bgDeep: PAPEL.hueso,
  ink: PAPEL.tinta,
  paper: PAPEL.crema,
  accent: PAPEL.lima,
  hot: PAPEL.coral,
  muted: "rgba(58,46,42,0.38)",
};

let papel = false;
/** Se llama al empezar a pintar el vídeo o la portada (antes que los hijos), así todos leen la paleta buena. */
export const applyEstilo = (estilo: Estilo) => {
  papel = estilo === "papel";
  Object.assign(brand.colors as Record<string, string>, papel ? { ...BASE, ...PAPEL_COLORS } : BASE);
};
export const isPapel = () => papel;

/** Texto «claro con sombra dura» del estilo azul; en papel, tinta oscura con un leve relieve. */
export const boldText = (shadow: number): React.CSSProperties =>
  papel
    ? { color: PAPEL.tinta, textShadow: `0 ${Math.max(2, shadow / 3)}px 0 rgba(255,255,255,0.55)` }
    : { color: brand.colors.paper, textShadow: `${shadow}px ${shadow}px 0 ${brand.colors.ink}` };

/** Bloque resaltado (lima o coral): en azul, borde de tinta y sombra dura; en papel, cinta adhesiva. */
export const tapeBlock = (borderPx: number, shadow: number): React.CSSProperties =>
  papel
    ? { border: "none", boxShadow: "0 3px 7px rgba(58,46,42,0.28), inset 0 0 0 2px rgba(255,255,255,0.18)", opacity: 0.96 }
    : { border: `${borderPx}px solid ${brand.colors.ink}`, boxShadow: `${shadow}px ${shadow}px 0 ${brand.colors.ink}` };

export const PAPER_EDGE = "ui-papel-borde";
export const PAPER_EDGE_FINE = "ui-papel-fino";
