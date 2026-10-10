import { Easing, interpolate, spring, useCurrentFrame } from "remotion";
import { FPS, brand } from "../brand";
import { exitOut, pop, sec } from "../anim";
import type { Illustration as Ill, IllustrationAnim } from "../types";

const { colors, fonts, border, shadow } = brand;

const ENTRANCES = new Set(["pop", "fade", "draw", "grow", "slide-left", "slide-right", "slide-up", "slide-down"]);
const ORIGINS: Record<string, string> = {
  center: "center", bottom: "50% 100%", top: "50% 0%", left: "0% 50%", right: "100% 50%",
  "bottom-left": "0% 100%", "bottom-right": "100% 100%", "top-left": "0% 0%", "top-right": "100% 0%",
};

/** Limpia el SVG generado (sin scripts ni recursos externos) y aísla sus ids. */
export function sanitizeSvg(svg: string, prefix: string): string {
  let s = svg
    .replace(/<\?xml[^>]*>/g, "")
    .replace(/<!DOCTYPE[^>]*>/gi, "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<foreignObject[\s\S]*?<\/foreignObject>/gi, "")
    .replace(/\son[a-z]+\s*=\s*("[^"]*"|'[^']*')/gi, "")
    .replace(/(href|xlink:href)\s*=\s*"(?!#|data:image\/(?:png|jpeg);base64,)[^"]*"/gi, "") // solo anclas o imágenes incrustadas (nada externo)
    .replace(/@import[^;]*;/gi, "");
  s = s.replace(/\bid="([^"]+)"/g, `id="${prefix}-$1"`);
  s = s.replace(/url\(#([^)]+)\)/g, `url(#${prefix}-$1)`);
  s = s.replace(/href="#([^"]+)"/g, `href="#${prefix}-$1"`);
  // pathLength=1 permite los efectos "draw" y "flow" en cualquier trazo
  // (salvo en trazos con su propio stroke-dasharray, que se verían continuos)
  s = s.replace(/<(path|line|polyline)\b(?![^>]*(pathLength|stroke-dasharray))/g, '<$1 pathLength="1"');
  // el SVG ocupa todo el panel
  s = s.replace(/<svg\b([^>]*)>/, (_m, attrs: string) => {
    const clean = attrs.replace(/\s(width|height|preserveAspectRatio)="[^"]*"/g, "");
    return `<svg${clean} width="100%" height="100%" preserveAspectRatio="xMidYMid slice">`;
  });
  return s;
}

type State = { tx: number; ty: number; rot: number; sx: number; sy: number; op: number; dash?: string; offset?: number; origin?: string };

function computeStyles(anims: IllustrationAnim[], frame: number, sceneStart: number): Record<string, State> {
  const t = frame / FPS;
  const out: Record<string, State> = {};

  // Visibilidad: por cada elemento, el último evento (entrada u ocultación) anterior al instante actual manda.
  // Si su primer evento es una entrada, empieza oculto; si no tiene eventos, se ve siempre.
  const vis: Record<string, { at: number; a: IllustrationAnim }[]> = {};
  for (const a of anims) {
    if (ENTRANCES.has(a.effect) || a.effect === "hide") (vis[a.target] ??= []).push({ at: a.at ?? sceneStart, a });
  }
  for (const [target, evs] of Object.entries(vis)) {
    evs.sort((x, y) => x.at - y.at);
    const st = (out[target] ??= { tx: 0, ty: 0, rot: 0, sx: 1, sy: 1, op: 1 });
    const past = evs.filter((e) => frame >= sec(e.at));
    if (!past.length) {
      if (ENTRANCES.has(evs[0].a.effect)) st.op = 0;
      continue;
    }
    const { a, at } = past[past.length - 1];
    const f = frame - sec(at);
    if (a.origin) st.origin = ORIGINS[a.origin];
    if (a.effect === "hide") {
      const prevVisible = past.length > 1 || !ENTRANCES.has(evs[0].a.effect);
      st.op *= at <= sceneStart + 0.01 || !prevVisible ? 0 : interpolate(f, [0, 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      continue;
    }
    const dur = a.dur ?? 0.7;
    if (a.effect === "draw") {
      st.dash = "1 1";
      st.offset = 1 - interpolate(f, [0, sec(dur)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
      continue;
    }
    const p = pop(f, 0, 11);
    switch (a.effect) {
      case "pop": st.sx *= p; st.sy *= p; st.op *= Math.min(1, p * 2); break;
      case "fade": st.op *= interpolate(f, [0, sec(dur)], [0, 1], { extrapolateRight: "clamp" }); break;
      case "grow": st.sy *= p; st.origin ??= ORIGINS.bottom; break;
      case "slide-left": st.tx += (1 - p) * -260; st.op *= Math.min(1, p * 2); break;
      case "slide-right": st.tx += (1 - p) * 260; st.op *= Math.min(1, p * 2); break;
      case "slide-up": st.ty += (1 - p) * 220; st.op *= Math.min(1, p * 2); break;
      case "slide-down": st.ty += (1 - p) * -220; st.op *= Math.min(1, p * 2); break;
    }
  }

  for (const a of anims) {
    if (ENTRANCES.has(a.effect) || a.effect === "hide" || a.target === "camera") continue;
    const st = (out[a.target] ??= { tx: 0, ty: 0, rot: 0, sx: 1, sy: 1, op: 1 });
    if (a.origin) st.origin = ORIGINS[a.origin];
    const at = a.at ?? sceneStart;
    const f = frame - sec(at);
    const amount = a.amount ?? 1;
    const lt = Math.max(0, t - at);
    if (a.effect === "move") {
      const p = f < 0 ? 0 : spring({ frame: f, fps: FPS, durationInFrames: sec(a.dur ?? 0.6), config: { damping: 18 } });
      st.tx += (a.to?.[0] ?? 0) * p;
      st.ty += (a.to?.[1] ?? 0) * p;
      st.rot += (a.rotate ?? 0) * p;
      continue;
    }
    if (a.effect === "punch") {
      if (f >= 0 && f < 14) {
        const k = 1 + Math.sin((f / 14) * Math.PI) * 0.16 * amount;
        st.sx *= k;
        st.sy *= k;
      }
      continue;
    }
    if (f < 0) continue; // los bucles empiezan en `at`
    switch (a.effect) {
      case "float": st.ty += Math.sin(lt * 2.2) * 10 * amount; break;
      case "bob": st.ty -= Math.abs(Math.sin(lt * 3.2)) * 14 * amount; break;
      case "sway": st.rot += Math.sin(lt * 2) * 6 * amount; break;
      case "spin": st.rot += lt * 120 * amount; break;
      case "pulse": { const k = 1 + Math.sin(lt * 5) * 0.07 * amount; st.sx *= k; st.sy *= k; break; }
      case "shake": st.tx += Math.sin(lt * 45) * 5 * amount; break;
      case "wiggle": st.rot += Math.sin(lt * 9) * 5 * amount; break;
      case "flow": st.dash = "0.08 0.05"; st.offset = -lt * 0.6 * amount; break;
      case "ripple": {
        const c = (lt / 1.6 + (a.phase ?? 0)) % 1;
        const k = 0.45 + c * 1.1 * amount;
        st.sx *= k; st.sy *= k; st.op *= c < 0.15 ? c / 0.15 : 1 - (c - 0.15) / 0.85;
        break;
      }
      case "breathe": { st.sy *= 1 + Math.sin(lt * 2.4 + (a.phase ?? 0) * 6.28) * 0.03 * amount; st.sx *= 1 + Math.sin(lt * 2.4 + (a.phase ?? 0) * 6.28) * 0.012 * amount; break; }
      case "drift": st.tx += Math.sin(lt * 1.1 + (a.phase ?? 0) * 6.28) * 18 * amount; break;
      case "blink": { const c = (lt * FPS) % 90; st.sy *= c < 5 ? Math.max(0.1, Math.abs(Math.cos((c / 5) * Math.PI))) : 1; break; }
    }
  }
  return out;
}

/** Cámara del panel: acercamientos ("zoom" sobre target "camera") encadenados + un leve avance continuo. */
function camera(anims: IllustrationAnim[], frame: number, sceneStart: number, sceneEnd: number, vw = 1000, vh = 700) {
  const shots = anims.filter((a) => a.target === "camera" && a.effect === "zoom").sort((x, y) => (x.at ?? sceneStart) - (y.at ?? sceneStart));
  const at = (zx: number, zy: number, z: number) => ({ ox: -(zx / vw - 0.5) * z * 100, oy: -(zy / vh - 0.5) * z * 100, s: z });
  let cur = { ox: 0, oy: 0, s: 1 };
  for (const a of shots) {
    const f = frame - sec(a.at ?? sceneStart);
    if (f < 0) break;
    const z = Math.max(1, a.amount ?? 1.5);
    const next = z === 1 ? { ox: 0, oy: 0, s: 1 } : at(a.to?.[0] ?? vw / 2, a.to?.[1] ?? vh / 2, z);
    const p = spring({ frame: f, fps: FPS, durationInFrames: sec(a.dur ?? 0.7), config: { damping: 200 } });
    cur = { ox: cur.ox + (next.ox - cur.ox) * p, oy: cur.oy + (next.oy - cur.oy) * p, s: cur.s + (next.s - cur.s) * p };
  }
  // avance lento tipo documental durante toda la escena
  const drift = interpolate(frame, [sec(sceneStart), sec(sceneEnd)], [1, 1.045], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const s = cur.s * drift;
  const lim = ((s - 1) / 2) * 100; // nunca se ve el borde del dibujo
  const clampL = (v: number) => Math.max(-lim, Math.min(lim, v));
  return `translate(${clampL(cur.ox).toFixed(2)}%, ${clampL(cur.oy).toFixed(2)}%) scale(${s.toFixed(4)})`;
}

// Panel de "figura" con una ilustración vectorial animada del tema del vídeo.
export const IllustrationPanel: React.FC<{
  ill: Ill; id: string; sceneStart: number; sceneEnd: number; isLast: boolean; height: number; variant?: "panel" | "free" | "full";
}> = ({ ill, id, sceneStart, sceneEnd, isLast, height, variant = "panel" }) => {
  const frame = useCurrentFrame();
  const prefix = `ill${id}`;
  const svg = sanitizeSvg(ill.svg, prefix);
  const vb = (ill.svg.match(/viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)/) ?? []).slice(1).map(Number);
  const [vw, vh] = vb.length === 2 ? vb : [1000, 700];
  const states = computeStyles(ill.anims ?? [], frame, sceneStart);
  const css = Object.entries(states)
    .map(([target, s]) => {
      const rules = [
        "transform-box: fill-box",
        `transform-origin: ${s.origin ?? "center"}`,
        `translate: ${s.tx.toFixed(2)}px ${s.ty.toFixed(2)}px`,
        `rotate: ${s.rot.toFixed(2)}deg`,
        `scale: ${s.sx.toFixed(4)} ${s.sy.toFixed(4)}`,
      ];
      // con opacidad 1 no se fija, para respetar la opacidad propia del grupo en el SVG
      if (s.op < 0.999) rules.push(`opacity: ${s.op.toFixed(3)}`);
      if (s.dash) rules.push(`stroke-dasharray: ${s.dash}`, `stroke-dashoffset: ${s.offset?.toFixed(4)}`);
      return `#${prefix}-${CSS.escape(target)} { ${rules.join("; ")} }`;
    })
    .join("\n");

  const f = frame - sec(sceneStart);
  const s = pop(f, 0, 13);
  const out = isLast ? 1 : exitOut(frame, sec(sceneEnd), 6);

  const framed = variant === "panel";
  const box: React.CSSProperties =
    variant === "full"
      ? { position: "absolute", inset: 0, overflow: "hidden", opacity: Math.min(1, s * 2) * out, transform: `scale(${interpolate(s, [0, 1], [1.06, 1])})` }
      : variant === "free"
        ? { position: "relative", height, flexShrink: 0, overflow: "hidden", opacity: Math.min(1, s * 2) * out, transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px) scale(${0.96 + 0.04 * out})` }
        : {
            position: "relative",
            height,
            flexShrink: 0,
            border: `${border}px solid ${colors.ink}`,
            borderRadius: 26,
            boxShadow: `${shadow}px ${shadow}px 0 ${colors.ink}`,
            overflow: "hidden",
            background: colors.paper,
            opacity: Math.min(1, s * 2) * out,
            transform: `scale(${interpolate(s, [0, 1], [0.92, 1]) * (0.95 + 0.05 * out)}) rotate(${interpolate(s, [0, 1], [-2, 0])}deg)`,
          };

  return (
    <div style={box}>
      <style>{css}</style>
      <div
        style={{ position: "absolute", inset: 0, transformOrigin: "50% 50%", transform: camera(ill.anims ?? [], frame, sceneStart, sceneEnd, vw, vh) }}
        dangerouslySetInnerHTML={{ __html: svg }}
      />
      {ill.caption && framed && (
        <div
          style={{
            position: "absolute",
            left: 16,
            top: 16,
            fontFamily: fonts.mono,
            fontWeight: 800,
            fontSize: 22,
            letterSpacing: 1,
            textTransform: "uppercase",
            background: colors.ink,
            color: colors.accent,
            padding: "6px 12px",
            borderRadius: 8,
          }}
        >
          {ill.caption}
        </div>
      )}
    </div>
  );
};
