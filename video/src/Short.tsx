import { AbsoluteFill, Audio, interpolate, spring, staticFile, useCurrentFrame } from "remotion";
import { FPS, PAD, W, brand } from "./brand";
import { sec } from "./anim";
import { Background } from "./components/Background";
import { Captions } from "./components/Captions";
import { Headline } from "./components/Headline";
import { Mascot } from "./components/Mascot";
import { Outro } from "./components/Outro";
import { ProgressBar } from "./components/ProgressBar";
import { ElementView, Stamp } from "./elements/Elements";
import type { Scene, ShortProps } from "./types";

const CONTENT_TOP = 236;
const STAGE_BOTTOM = 1300;
const MASCOT_W = 300;
const SIDE_SCALE = 1.25;
const CENTER_SCALE = 1.55;

const sideOf = (s: Scene) => {
  const hasCards = (s.elements ?? []).some((e) => e.type !== "stamp");
  if (!hasCards) return 0; // centro
  return s.mascot?.side === "left" ? -1 : 1;
};

export const Short: React.FC<ShortProps> = ({ chapters, scenes, words, source, audio, music, musicVolume = 0.1, outro }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const idx = Math.max(0, scenes.findIndex((s, i) => t >= s.start && (t < s.end || i === scenes.length - 1)));
  const scene = scenes[idx];
  const prev = scenes[idx - 1];

  // Posición de la mascota: se desplaza con un muelle entre escenas.
  const mv = spring({ frame: frame - sec(scene.start), fps: FPS, config: { damping: 14, mass: 0.7 } });
  const xFor = (side: number) => (side === 0 ? (W - MASCOT_W * CENTER_SCALE) / 2 : side === -1 ? 0 : W - MASCOT_W * SIDE_SCALE);
  const fromSide = prev ? sideOf(prev) : sideOf(scene);
  const toSide = sideOf(scene);
  const mx = interpolate(mv, [0, 1], [xFor(fromSide), xFor(toSide)]);
  const sc = (side: number) => (side === 0 ? CENTER_SCALE : SIDE_SCALE);
  const mScale = interpolate(mv, [0, 1], [sc(fromSide), sc(toSide)]);
  const toward: -1 | 1 = toSide === 1 ? -1 : 1;

  const speaking = words.some((w) => t >= w.start && t < w.end);
  const talking = speaking ? 0.45 + 0.55 * Math.abs(Math.sin(frame * 0.9)) : 0;

  // barrido de color al cambiar de capítulo
  const chapterChange = prev && prev.chapter !== scene.chapter;
  const sweep = chapterChange ? interpolate(frame - sec(scene.start), [-4, 8], [-0.2, 1.2], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 2;

  const ctx = { end: scene.end, isLast: idx === scenes.length - 1 };
  const cards = (scene.elements ?? []).filter((e) => e.type !== "stamp");
  const stamps = (scene.elements ?? []).filter((e) => e.type === "stamp");

  return (
    <AbsoluteFill style={{ fontFamily: brand.fonts.display }}>
      <Background />
      {audio && <Audio src={audio.startsWith("http") ? audio : staticFile(audio)} />}
      {music && <Audio src={music.startsWith("http") ? music : staticFile(music)} volume={musicVolume} loop />}

      <ProgressBar chapters={chapters} scenes={scenes} source={source} />
      {/* columna de contenido: titular + tarjetas */}
      <div
        style={{
          position: "absolute",
          top: CONTENT_TOP,
          left: PAD,
          right: PAD,
          bottom: 1920 - STAGE_BOTTOM,
          display: "flex",
          flexDirection: "column",
          gap: 44,
        }}
      >
        <Headline key={`h${idx}`} text={scene.headline} number={scene.number} start={scene.start} end={scene.end} isLast={ctx.isLast} />
        <div
          key={`s${idx}`}
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 30,
            marginLeft: toSide === -1 ? MASCOT_W * SIDE_SCALE - 70 : 0,
            marginRight: toSide === 1 ? MASCOT_W * SIDE_SCALE - 90 : 0,
          }}
        >
          {cards.map((el, i) => (
            <ElementView key={i} el={el} ctx={ctx} />
          ))}
        </div>
      </div>

      {/* mascota */}
      <div style={{ position: "absolute", left: mx, top: STAGE_BOTTOM - 440 * mScale + 10, width: MASCOT_W * mScale }}>
        <Mascot
          pose={scene.mascot?.pose ?? (toSide === 0 ? "explain" : "point")}
          toward={toward}
          look={scene.mascot?.look ?? "center"}
          talking={talking}
          poseFrame={frame - sec(scene.start)}
          scale={mScale}
        />
      </div>

      {stamps.map((el, i) => (
        <Stamp key={i} el={el as Extract<typeof el, { type: "stamp" }>} ctx={ctx} />
      ))}

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
    </AbsoluteFill>
  );
};
