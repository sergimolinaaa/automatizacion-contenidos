import { AbsoluteFill, Freeze } from "remotion";
import { PAD, W, brand } from "./brand";
import { parseMarkup } from "./anim";
import { Background } from "./components/Background";
import { Fit } from "./components/Fit";
import { IllustrationPanel } from "./components/Illustration";
import type { ShortProps } from "./types";

const { colors, fonts, border } = brand;

export type CoverProps = ShortProps & {
  cover?: { text?: string; scene?: number; at?: number; badge?: string; layout?: "panel" | "full" };
};

/**
 * Portada 1080x1920 (Reels/TikTok). Todo lo importante cae dentro del recorte 3:4 del perfil
 * de Instagram (y 240 a 1680) y la franja central 1:1.
 */
export const Cover: React.FC<CoverProps> = (props) => {
  const c = props.cover ?? {};
  const sceneIdx = c.scene ?? 0;
  const scene = props.scenes[sceneIdx];
  const text = (c.text ?? scene.headline).toUpperCase();
  const ill = scene.illustration ?? props.scenes.find((s) => s.illustration)?.illustration;
  const lastAnim = Math.max(scene.start, ...((ill?.anims ?? []).map((a) => a.at ?? 0)));
  const freezeAt = c.at ?? Math.min(scene.end - 0.05, lastAnim + 0.6);

  const parts = parseMarkup(text);
  const letters = text.replace(/\*/g, "").length;
  const size = letters > 30 ? 92 : letters > 20 ? 108 : 124;

  const hook = (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: size * 0.26, rowGap: 14, lineHeight: 1.04, transform: "rotate(-2deg)" }}>
      {parts.map((p, i) =>
        p.hi ? (
          <span
            key={i}
            style={{
              fontFamily: fonts.display, fontWeight: 900, fontSize: size, letterSpacing: -2, color: colors.ink,
              background: colors.accent, border: `${border + 2}px solid ${colors.ink}`, boxShadow: `10px 10px 0 ${colors.ink}`,
              padding: "4px 20px 12px", transform: "rotate(-1.5deg)", textAlign: "center",
            }}
          >
            {p.text.trim()}
          </span>
        ) : (
          p.text.split(/\s+/).filter(Boolean).map((w, j) => (
            <span key={`${i}-${j}`} style={{ fontFamily: fonts.display, fontWeight: 900, fontSize: size, letterSpacing: -2, color: colors.paper, textShadow: `8px 8px 0 ${colors.ink}` }}>
              {w}
            </span>
          ))
        ),
      )}
    </div>
  );

  return (
    <AbsoluteFill>
      <Background />
      <div style={{ position: "absolute", top: 250, left: PAD }}>
        <Fit height={1420} width={W - PAD * 2} align="center">
          <div style={{ display: "flex", flexDirection: "column", alignItems: "stretch", gap: 50 }}>
            <div style={{ display: "flex", justifyContent: "center" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 12, background: colors.ink, color: colors.paper, padding: "10px 22px", borderRadius: 14, fontFamily: fonts.display, fontWeight: 900, fontSize: 38, transform: "rotate(-2deg)" }}>
                EL TRUCO
                <span style={{ background: colors.accent, color: colors.ink, padding: "0 12px 4px" }}>ES…</span>
              </div>
            </div>
            {hook}
            {ill && (
              <div style={{ transform: "rotate(1.5deg)", padding: "0 10px" }}>
                <Freeze frame={Math.round(freezeAt * 30)}>
                  <IllustrationPanel ill={{ ...ill, caption: undefined }} id="cover" sceneStart={scene.start} sceneEnd={scene.end + 999} isLast height={560} />
                </Freeze>
              </div>
            )}
          </div>
        </Fit>
      </div>
    </AbsoluteFill>
  );
};
