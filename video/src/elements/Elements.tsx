import { Easing, interpolate, useCurrentFrame } from "remotion";
import { FPS, brand } from "../brand";
import { exitOut, formatNumber, pop, sec, seeded } from "../anim";
import { Icon } from "../icons";
import type { Element } from "../types";

const { colors, fonts, border, shadow, radius } = brand;

type Ctx = { end: number; isLast: boolean };

const Label: React.FC<{ children: React.ReactNode; dark?: boolean }> = ({ children, dark }) => (
  <div
    style={{
      fontFamily: fonts.mono,
      fontWeight: 800,
      fontSize: 22,
      letterSpacing: 1,
      textTransform: "uppercase",
      color: dark ? colors.accent : colors.ink,
      opacity: dark ? 1 : 0.75,
      marginBottom: 8,
    }}
  >
    {children}
  </div>
);

/** Tarjeta neo-brutalista: entra con un barrido limpio (una barra lima abre la tarjeta) y sale al final de la escena. */
const Card: React.FC<{
  el: Element; ctx: Ctx; children: React.ReactNode; tone?: "paper" | "accent" | "ink"; pad?: number; style?: React.CSSProperties;
}> = ({ el, ctx, children, tone = "paper", pad = 26, style }) => {
  const frame = useCurrentFrame();
  const f = frame - sec(el.at);
  const p = interpolate(f, [0, 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const settle = pop(f, 4, 12);
  const out = ctx.isLast ? 1 : exitOut(frame, sec(ctx.end), 6);
  const tilt = (seeded(JSON.stringify(el)) - 0.5) * 2;
  const bg = tone === "accent" ? colors.accent : tone === "ink" ? colors.ink : colors.paper;
  return (
    <div
      style={{
        position: "relative",
        background: bg,
        border: `${border}px solid ${colors.ink}`,
        borderRadius: radius,
        boxShadow: `${shadow}px ${shadow}px 0 ${colors.ink}`,
        padding: pad,
        opacity: f < 0 ? 0 : out,
        clipPath: p < 1 ? `inset(-40px ${((1 - p) * 100).toFixed(2)}% -40px -40px)` : undefined,
        transform: `translateY(${interpolate(p, [0, 1], [24, 0]) + (1 - out) * 30}px) rotate(${interpolate(settle, [0, 1], [0, tilt])}deg) scale(${0.96 + 0.04 * out})`,
        ...style,
      }}
    >
      {children}
      {p > 0 && p < 1 && (
        <div style={{ position: "absolute", top: -border, bottom: -border, left: `calc(${(p * 100).toFixed(2)}% - 14px)`, width: 14, background: colors.accent, borderLeft: `4px solid ${colors.ink}`, borderRight: `4px solid ${colors.ink}` }} />
      )}
    </div>
  );
};

/** Pregunta final para comentarios: corta, del tema del vídeo, con un toque de humor. */
const Ask: React.FC<{ el: Extract<Element, { type: "ask" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  const f = frame - sec(el.at);
  const words = el.text.split(/\s+/).filter(Boolean);
  const bob = Math.sin(frame / 9) * 4;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 26 }}>
      <Card el={el} ctx={ctx} pad={44} style={{ borderRadius: 40 }}>
        <div style={{ display: "flex", flexWrap: "wrap", columnGap: 18, rowGap: 6 }}>
          {words.map((w, i) => {
            const s = pop(f, 6 + i * 1.6, 13);
            const hi = /^\*.*\*[¿?¡!.,]*$/.test(w);
            return (
              <span key={i} style={{ display: "inline-block", overflow: "hidden", padding: "0 4px 6px", margin: "0 -4px -6px" }}>
                <span
                  style={{
                    display: "inline-block",
                    fontFamily: fonts.display, fontWeight: 900, fontSize: 66, lineHeight: 1.1, color: colors.ink,
                    background: hi ? colors.accent : "transparent", padding: hi ? "0 10px" : 0,
                    transform: `translateY(${interpolate(s, [0, 1], [90, 0])}%)`,
                  }}
                >
                  {w.replace(/\*/g, "")}
                </span>
              </span>
            );
          })}
        </div>
        <svg width={90} height={60} viewBox="0 0 90 60" style={{ position: "absolute", left: 70, bottom: -58 }}>
          <path d="M 0 0 L 70 0 L 10 54 Z" fill={colors.paper} stroke={colors.ink} strokeWidth={border} strokeLinejoin="round" />
          <rect x={-2} y={-12} width={80} height={14} fill={colors.paper} />
        </svg>
      </Card>
      <div
        style={{
          alignSelf: "flex-end", display: "flex", alignItems: "center", gap: 14, marginTop: 30,
          fontFamily: fonts.mono, fontWeight: 800, fontSize: 30, background: colors.ink, color: colors.accent,
          padding: "12px 22px", borderRadius: 14, opacity: f < 14 ? 0 : 1,
          transform: `translateY(${(1 - pop(f, 14, 12)) * 30 + bob}px)`,
        }}
      >
        <svg width={40} height={36} viewBox="0 0 44 40"><path d="M 4 4 H 40 V 28 H 18 L 8 36 V 28 H 4 Z" fill={colors.accent} stroke={colors.accent} strokeWidth={4} strokeLinejoin="round" /></svg>
        {el.footer ?? "TE LEO EN COMENTARIOS"}
      </div>
    </div>
  );
};

const Stat: React.FC<{ el: Extract<Element, { type: "stat" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - sec(el.at), [4, 4 + FPS * 1.1], [0, 1], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic),
  });
  const from = el.from ?? (Math.abs(el.value) >= 10 ? 0 : el.value);
  const value = from + (el.value - from) * p;
  const txt = `${el.prefix ?? ""}${formatNumber(value, el.decimals ?? 0)}`;
  const size = txt.length > 9 ? 92 : txt.length > 6 ? 112 : 136;
  return (
    <Card el={el} ctx={ctx}>
      {el.label && <Label>{el.label}</Label>}
      <div style={{ display: "flex", alignItems: "baseline", gap: 14, flexWrap: "wrap" }}>
        <span style={{ fontFamily: fonts.display, fontWeight: 900, fontSize: size, lineHeight: 1, color: colors.ink, fontVariantNumeric: "tabular-nums", letterSpacing: -3 }}>
          {txt}
        </span>
        {el.unit && (
          <span style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: size * 0.42, color: colors.ink, background: colors.accent, padding: "2px 12px", border: `4px solid ${colors.ink}` }}>
            {el.unit}
          </span>
        )}
      </div>
      {el.note && <div style={{ marginTop: 12, fontFamily: fonts.mono, fontWeight: 700, fontSize: 24, color: colors.ink }}>{el.note}</div>}
    </Card>
  );
};

const Fact: React.FC<{ el: Extract<Element, { type: "fact" }>; ctx: Ctx }> = ({ el, ctx }) => (
  <Card el={el} ctx={ctx} tone={el.tone ?? "paper"}>
    {el.label && <Label dark={el.tone === "ink"}>{el.label}</Label>}
    <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 46, lineHeight: 1.12, color: el.tone === "ink" ? colors.paper : colors.ink }}>
      {el.text}
    </div>
  </Card>
);

const IconCard: React.FC<{ el: Extract<Element, { type: "icon" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  return (
    <Card el={el} ctx={ctx} pad={22} style={{ alignSelf: "flex-start", display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
      <div style={{ transform: `rotate(${Math.sin(t * 2) * 4}deg)` }}>
        <Icon name={el.icon} size={250} t={t} />
      </div>
      {el.label && (
        <div style={{ fontFamily: fonts.display, fontWeight: 900, fontSize: 32, color: colors.ink, textTransform: "uppercase" }}>{el.label}</div>
      )}
    </Card>
  );
};

const Compare: React.FC<{ el: Extract<Element, { type: "compare" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  const scale = (v: number) => (el.log ? Math.log10(Math.max(1, v)) : v);
  const max = Math.max(...el.rows.map((r) => scale(r.value)));
  return (
    <Card el={el} ctx={ctx}>
      {el.label && <Label>{el.label}</Label>}
      <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
        {el.rows.map((r, i) => {
          const at = r.at ?? el.at + 0.25 + i * 0.45;
          const g = pop(frame - sec(at), 0, 16);
          const w = Math.max(0.04, scale(r.value) / max);
          return (
            <div key={i} style={{ opacity: frame < sec(at) ? 0.15 : 1 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontFamily: fonts.display, fontWeight: 800, fontSize: 36, color: colors.ink, marginBottom: 8 }}>
                <span>{r.label}</span>
                <span>{r.display ?? formatNumber(r.value)}</span>
              </div>
              <div style={{ height: 44, border: `5px solid ${colors.ink}`, borderRadius: 8, overflow: "hidden", background: "#EEF0FF" }}>
                <div style={{ height: "100%", width: `${w * g * 100}%`, background: i === el.rows.length - 1 ? colors.accent : colors.bg, borderRight: `4px solid ${colors.ink}` }} />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};

const Dots: React.FC<{ el: Extract<Element, { type: "dots" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  const total = el.total ?? 100;
  const cols = 10;
  const shown = interpolate(frame - sec(el.at), [6, 6 + FPS * 1.2], [0, el.filled], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Card el={el} ctx={ctx}>
      {el.label && <Label>{el.label}</Label>}
      <div style={{ display: "flex", gap: 22, alignItems: "center" }}>
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, 26px)`, gap: 8 }}>
          {Array.from({ length: total }, (_, i) => (
            <div key={i} style={{ width: 26, height: 26, borderRadius: 13, border: `3px solid ${colors.ink}`, background: i < shown ? colors.ink : "transparent", transform: `scale(${i < shown && i > shown - 3 ? 1.25 : 1})` }} />
          ))}
        </div>
        <div style={{ fontFamily: fonts.display, fontWeight: 900, fontSize: 80, color: colors.ink, lineHeight: 1 }}>
          {Math.round(shown)}
          <div style={{ fontFamily: fonts.mono, fontWeight: 700, fontSize: 22, marginTop: 8 }}>{el.caption ?? `de cada ${total}`}</div>
        </div>
      </div>
    </Card>
  );
};

const List: React.FC<{ el: Extract<Element, { type: "list" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  return (
    <Card el={el} ctx={ctx}>
      {el.label && <Label>{el.label}</Label>}
      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {el.items.map((it, i) => {
          const at = it.at ?? el.at + 0.3 + i * 0.5;
          const s = pop(frame - sec(at), 0, 12);
          return (
            <div key={i} style={{ display: "flex", gap: 16, alignItems: "center", opacity: frame < sec(at) ? 0 : s, transform: `translateX(${(1 - s) * -40}px)` }}>
              <div style={{ width: 52, height: 52, flexShrink: 0, borderRadius: 26, background: colors.accent, border: `4px solid ${colors.ink}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: fonts.display, fontWeight: 900, fontSize: 26 }}>
                {el.numbered === false ? "✓" : i + 1}
              </div>
              <div style={{ fontFamily: fonts.display, fontWeight: 800, fontSize: 42, color: colors.ink, lineHeight: 1.1 }}>{it.text}</div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};

const Scale: React.FC<{ el: Extract<Element, { type: "scale" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame - sec(el.at), [8, 8 + FPS * 1.4], [0, el.progress], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic),
  });
  return (
    <Card el={el} ctx={ctx}>
      {el.label && <Label>{el.label}</Label>}
      <div style={{ position: "relative", height: 150, marginTop: 10 }}>
        <div style={{ position: "absolute", left: 0, right: 0, top: 86, height: 10, background: colors.ink, borderRadius: 5 }} />
        <div style={{ position: "absolute", left: 0, width: `${Math.min(1, p) * 100}%`, top: 82, height: 18, background: colors.accent, border: `4px solid ${colors.ink}`, borderRadius: 9 }} />
        {Array.from({ length: 11 }, (_, i) => (
          <div key={i} style={{ position: "absolute", left: `${i * 10}%`, top: 72, width: 4, height: i % 5 ? 14 : 30, background: colors.ink, marginLeft: -2 }} />
        ))}
        <div style={{ position: "absolute", left: `${Math.min(1, p) * 100}%`, top: 0, transform: "translateX(-50%)", display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={{ fontFamily: fonts.mono, fontWeight: 800, fontSize: 24, background: colors.ink, color: colors.accent, padding: "4px 12px", borderRadius: 6, whiteSpace: "nowrap" }}>
            {el.marker ?? "▼"}
          </div>
          <div style={{ width: 0, height: 0, borderLeft: "12px solid transparent", borderRight: "12px solid transparent", borderTop: `16px solid ${colors.ink}` }} />
        </div>
        <div style={{ position: "absolute", left: 0, top: 112, fontFamily: fonts.display, fontWeight: 800, fontSize: 26 }}>{el.from}</div>
        <div style={{ position: "absolute", right: 0, top: 112, fontFamily: fonts.display, fontWeight: 800, fontSize: 26 }}>{el.to}</div>
      </div>
    </Card>
  );
};

const Tag: React.FC<{ el: Extract<Element, { type: "tag" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const tone = el.tone ?? "ink";
  const bg = tone === "accent" ? colors.accent : tone === "hot" ? colors.hot : colors.ink;
  const fg = tone === "ink" ? colors.accent : colors.ink;
  const frame = useCurrentFrame();
  const s = pop(frame - sec(el.at), 0, 9);
  const out = ctx.isLast ? 1 : exitOut(frame, sec(ctx.end), 6);
  return (
    <div style={{ alignSelf: "flex-start", opacity: frame < sec(el.at) ? 0 : out, transform: `scale(${s}) rotate(${-4 + (1 - s) * -20}deg)` }}>
      <div style={{ background: bg, color: fg, border: `5px solid ${colors.ink}`, boxShadow: `8px 8px 0 ${colors.ink}`, padding: "8px 20px", fontFamily: fonts.display, fontWeight: 900, fontSize: 40, textTransform: "uppercase" }}>
        {el.text}
      </div>
    </div>
  );
};

const Quiz: React.FC<{ el: Extract<Element, { type: "quiz" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      {el.question && <Label dark>{el.question}</Label>}
      {el.options.map((o, i) => {
        const at = o.at ?? el.at + i * 0.5;
        const s = pop(frame - sec(at), 0, 11);
        const pulse = frame >= sec(at) && frame < sec(at) + 18;
        return (
          <div
            key={i}
            style={{
              display: "flex", alignItems: "center", gap: 18, padding: "14px 20px",
              background: pulse ? colors.accent : colors.paper, border: `${border}px solid ${colors.ink}`, borderRadius: radius,
              boxShadow: `${shadow}px ${shadow}px 0 ${colors.ink}`,
              opacity: frame < sec(at) ? 0.25 : 1, transform: `translateX(${(1 - s) * -30}px)`,
            }}
          >
            <div style={{ width: 64, height: 64, borderRadius: 32, background: colors.ink, color: colors.accent, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: fonts.display, fontWeight: 900, fontSize: 28 }}>{i + 1}</div>
            <div style={{ flex: 1, fontFamily: fonts.display, fontWeight: 800, fontSize: 42, color: colors.ink }}>{o.text}</div>
            <svg width={44} height={40} viewBox="0 0 44 40"><path d="M 4 4 H 40 V 28 H 18 L 8 36 V 28 H 4 Z" fill="none" stroke={colors.ink} strokeWidth={5} strokeLinejoin="round" /></svg>
          </div>
        );
      })}
      {el.footer && (
        <div style={{ marginTop: 6, alignSelf: "flex-start", fontFamily: fonts.mono, fontWeight: 800, fontSize: 24, background: colors.ink, color: colors.accent, padding: "8px 16px", borderRadius: 8, opacity: ctx.isLast ? 1 : exitOut(frame, sec(ctx.end)) }}>
          {el.footer}
        </div>
      )}
    </div>
  );
};

export const ElementView: React.FC<{ el: Element; ctx: Ctx }> = ({ el, ctx }) => {
  switch (el.type) {
    case "stat": return <Stat el={el} ctx={ctx} />;
    case "fact": return <Fact el={el} ctx={ctx} />;
    case "icon": return <IconCard el={el} ctx={ctx} />;
    case "compare": return <Compare el={el} ctx={ctx} />;
    case "dots": return <Dots el={el} ctx={ctx} />;
    case "list": return <List el={el} ctx={ctx} />;
    case "scale": return <Scale el={el} ctx={ctx} />;
    case "tag": return <Tag el={el} ctx={ctx} />;
    case "quiz": return <Quiz el={el} ctx={ctx} />;
    case "ask": return <Ask el={el} ctx={ctx} />;
    case "stamp": return <Stamp el={el} ctx={ctx} />;
    default: return null;
  }
};

/** Sello que "golpea" en su propio hueco (no se superpone a otras tarjetas). */
const Stamp: React.FC<{ el: Extract<Element, { type: "stamp" }>; ctx: Ctx }> = ({ el, ctx }) => {
  const frame = useCurrentFrame();
  const f = frame - sec(el.at);
  const s = f < 0 ? 0 : pop(f, 0, 9, 0.5);
  const out = ctx.isLast ? 1 : exitOut(frame, sec(ctx.end), 5);
  const color = el.tone === "accent" ? colors.accent : colors.hot;
  const shake = f >= 3 && f < 10 ? Math.sin(f * 3) * 6 : 0;
  return (
    <div style={{ alignSelf: "center", padding: "14px 0", opacity: f < 0 ? 0 : out }}>
      <div
        style={{
          transform: `translateX(${shake}px) scale(${interpolate(s, [0, 1], [1.35, 1])}) rotate(-7deg)`,
          opacity: Math.min(1, s * 3),
          border: `10px solid ${colors.ink}`,
          background: color,
          boxShadow: `12px 12px 0 ${colors.ink}`,
          borderRadius: 16,
          padding: "6px 34px 12px",
          fontFamily: fonts.display,
          fontWeight: 900,
          fontSize: 96,
          letterSpacing: 2,
          color: colors.ink,
        }}
      >
        {el.text.toUpperCase()}
      </div>
    </div>
  );
};
