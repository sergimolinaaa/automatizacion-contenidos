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
    .replace(/(href|xlink:href)\s*=\s*"(?!#)[^"]*"/gi, "")
    .replace(/@import[^;]*;/gi, "");
  s = s.replace(/\bid="([^"]+)"/g, `id="${prefix}-$1"`);
  s = s.replace(/url\(#([^)]+)\)/g, `url(#${prefix}-$1)`);
  s = s.replace(/href="#([^"]+)"/g, `href="#${prefix}-$1"`);
  // pathLength=1 permite los efectos "draw" y "flow" en cualquier trazo
  s = s.replace(/<(path|line|polyline)\b(?![^>]*pathLength)/g, '<$1 pathLength="1"');
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
    if (ENTRANCES.has(a.effect) || a.effect === "hide") continue;
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
      case "blink": { const c = (lt * FPS) % 90; st.sy *= c < 5 ? Math.max(0.1, Math.abs(Math.cos((c / 5) * Math.PI))) : 1; break; }
    }
  }
  return out;
}

// Panel de "figura" con una ilustración vectorial animada del tema del vídeo.
export const IllustrationPanel: React.FC<{ ill: Ill; id: string; sceneStart: number; sceneEnd: number; isLast: boolean; height: number }> = ({
  ill, id, sceneStart, sceneEnd, isLast, height,
}) => {
  const frame = useCurrentFrame();
  const prefix = `ill${id}`;
  const svg = sanitizeSvg(ill.svg, prefix);
  const states = computeStyles(ill.anims ?? [], frame, sceneStart);
  const css = Object.entries(states)
    .map(([target, s]) => {
      const rules = [
        "transform-box: fill-box",
        `transform-origin: ${s.origin ?? "center"}`,
        `translate: ${s.tx.toFixed(2)}px ${s.ty.toFixed(2)}px`,
        `rotate: ${s.rot.toFixed(2)}deg`,
        `scale: ${s.sx.toFixed(4)} ${s.sy.toFixed(4)}`,
        `opacity: ${s.op.toFixed(3)}`,
      ];
      if (s.dash) rules.push(`stroke-dasharray: ${s.dash}`, `stroke-dashoffset: ${s.offset?.toFixed(4)}`);
      return `#${prefix}-${CSS.escape(target)} { ${rules.join("; ")} }`;
    })
    .join("\n");

  const f = frame - sec(sceneStart);
  const s = pop(f, 0, 13);
  const out = isLast ? 1 : exitOut(frame, sec(sceneEnd), 6);

  return (
    <div
      style={{
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
      }}
    >
      <style>{css}</style>
      <div style={{ position: "absolute", inset: 0 }} dangerouslySetInnerHTML={{ __html: svg }} />
      {ill.caption && (
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
