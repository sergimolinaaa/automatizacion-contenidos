import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Cover, type CoverProps } from "./Cover";
import { FPS, PAD, W, brand } from "./brand";
import { sec } from "./anim";
import { Background } from "./components/Background";
import { CAMEO_H, Cameo } from "./components/Cameo";
import { Captions } from "./components/Captions";
import { Fit } from "./components/Fit";
import { Headline } from "./components/Headline";
import { IllustrationPanel } from "./components/Illustration";
import { Outro } from "./components/Outro";
import { ProgressBar } from "./components/ProgressBar";
import { Signature } from "./components/Signature";
import { ElementView } from "./elements/Elements";
import type { ShortProps } from "./types";

// Zonas fijas de la pantalla (nada se dibuja fuera de la suya, así nada se tapa):
// barra de capítulos 118-210 · contenido 236-1300 · subtítulos 1350-1480 · UI de la red social debajo.
/** Fotogramas finales con la portada: al elegir la portada en la app, se selecciona el final del vídeo. */
export const COVER_FRAMES = 18;

const CONTENT_TOP = 236;
const STAGE_BOTTOM = 1300;
const CONTENT_W = W - PAD * 2;
const GAP = 40;

const src = (f: string) => (f.startsWith("http") ? f : staticFile(f));

/** La música baja mientras habla la voz y sube en las pausas (ducking). */
const duckedVolume = (words: ShortProps["words"], base: number) => (f: number) => {
  const t = f / FPS;
  let near = Infinity;
  for (const w of words) {
    if (t >= w.start && t <= w.end) { near = 0; break; }
    near = Math.min(near, Math.abs(t - w.start), Math.abs(t - w.end));
  }
  const k = interpolate(near, [0.15, 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return base * (0.55 + 0.45 * k);
};

export const Short: React.FC<CoverProps> = (props) => {
  const { chapters, scenes, words, source, audio, music, musicVolume = 0.28, sfx, sfxVolume = 0.85, outro } = props;
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = frame / FPS;
  const idx = Math.max(0, scenes.findIndex((s, i) => t >= s.start && (t < s.end || i === scenes.length - 1)));
  const scene = scenes[idx];
  const prev = scenes[idx - 1];
  const ctx = { end: scene.end, isLast: idx === scenes.length - 1 };

  const speaking = words.some((w) => t >= w.start && t < w.end);
  const talking = speaking ? 0.45 + 0.55 * Math.abs(Math.sin(frame * 0.9)) : 0;

  // barrido de color al cambiar de capítulo
  const chapterChange = prev && prev.chapter !== scene.chapter;
  const sweep = chapterChange ? interpolate(frame - sec(scene.start), [-4, 8], [-0.2, 1.2], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 2;

  const cameo = scene.mascot ?? null;
  const contentH = STAGE_BOTTOM - CONTENT_TOP - (cameo ? CAMEO_H + 20 : 0);
  const elements = scene.elements ?? [];
  const ill = scene.illustration;
  const layout = ill?.layout ?? "panel";

  return (
    <AbsoluteFill style={{ fontFamily: brand.fonts.display }}>
      <Background />
      {audio && <Audio src={src(audio)} />}
      {music && <Audio src={src(music)} volume={duckedVolume(words, musicVolume)} />}
      {sfx && <Audio src={src(sfx)} volume={sfxVolume} />}

      {ill && layout === "full" && !scene.signature && (
        <AbsoluteFill>
          <IllustrationPanel ill={ill} id={String(idx)} sceneStart={scene.start} sceneEnd={scene.end} isLast={ctx.isLast} height={1920} variant="full" />
          {/* velos para que el titular y los subtítulos se lean sobre el dibujo */}
          <AbsoluteFill style={{ background: "linear-gradient(rgba(11,11,20,0.55), rgba(11,11,20,0) 26%, rgba(11,11,20,0) 62%, rgba(11,11,20,0.6) 82%, rgba(11,11,20,0.2))" }} />
        </AbsoluteFill>
      )}

      <ProgressBar chapters={chapters} scenes={scenes} source={source} />

      <div style={{ position: "absolute", top: CONTENT_TOP, left: PAD, width: CONTENT_W }}>
        {scene.signature ? (
          <Fit key={`sig${idx}`} height={STAGE_BOTTOM - CONTENT_TOP} width={CONTENT_W}>
            <Signature start={scene.start} end={scene.end} />
          </Fit>
        ) : (
          <Fit key={`c${idx}`} height={contentH} width={CONTENT_W}>
            <div style={{ display: "flex", flexDirection: "column", gap: GAP }}>
              <Headline text={scene.headline} number={scene.number} start={scene.start} end={scene.end} isLast={ctx.isLast} />
              {ill && layout !== "full" && (
                <IllustrationPanel
                  ill={ill} id={String(idx)} sceneStart={scene.start} sceneEnd={scene.end} isLast={ctx.isLast}
                  height={ill.height ?? (layout === "free" ? 820 : 620)} variant={layout}
                />
              )}
              {elements.length > 0 && (
                <div
                  style={{
                    display: "flex",
                    flexDirection: ill && layout !== "full" ? "row" : "column",
                    flexWrap: ill && layout !== "full" ? "wrap" : "nowrap",
                    alignItems: ill && layout !== "full" ? "flex-start" : "stretch",
                    marginTop: layout === "full" ? 560 : 0,
                    gap: 30,
                  }}
                >
                  {elements.map((el, i) => (
                    <ElementView key={i} el={el} ctx={ctx} />
                  ))}
                </div>
              )}
            </div>
          </Fit>
        )}
        {cameo && !scene.signature && (
          <div style={{ marginTop: 20 }}>
            <Cameo cameo={cameo} sceneEnd={scene.end} talking={talking} width={CONTENT_W} />
          </div>
        )}
      </div>

      <Captions words={words} />

      {sweep >= -0.2 && sweep <= 1.2 && (
        <AbsoluteFill style={{ pointerEvents: "none" }}>
          <div
            style={{
              position: "absolute",
              top: -400,
              bottom: -400,
              width: 260,
              left: `${sweep * 140 - 20}%`,
              background: brand.colors.accent,
              transform: "rotate(14deg)",
              borderLeft: `10px solid ${brand.colors.ink}`,
              borderRight: `10px solid ${brand.colors.ink}`,
            }}
          />
        </AbsoluteFill>
      )}

      {outro && <Outro at={outro.at} cta={outro.cta} />}

      {frame >= durationInFrames - COVER_FRAMES && (
        <AbsoluteFill>
          <Cover {...props} />
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
