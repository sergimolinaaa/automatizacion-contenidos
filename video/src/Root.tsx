import { Composition, continueRender, delayRender } from "remotion";
import { FPS, H, W } from "./brand";
import { fontsReady } from "./fonts";
import { Cover } from "./Cover";
import { Profile } from "./Profile";
import { ProfileName } from "./ProfileName";
import { COVER_FRAMES, Short } from "./Short";
import sample from "./sample-props.json";
import type { ShortProps } from "./types";

const handle = delayRender("fuentes");
fontsReady.then(() => continueRender(handle));

const durationOf = (p: ShortProps) => {
  let end = Math.max(...p.scenes.map((s) => s.end));
  if (p.outro) end = Math.max(end, p.outro.at + 2.6);
  return Math.ceil(end * FPS) + COVER_FRAMES;
};

export const Root: React.FC = () => (
  <>
  <Composition id="Portada" component={Cover} width={W} height={H} fps={FPS} durationInFrames={9000} defaultProps={sample as ShortProps} />
  <Composition id="PerfilNombre" component={ProfileName} width={1080} height={1080} fps={FPS} durationInFrames={1} defaultProps={{ variant: "blue" as const }} />
  <Composition id="Perfil" component={Profile} width={1080} height={1080} fps={FPS} durationInFrames={60} defaultProps={{ variant: "blue" as const }} />
  <Composition
    id="Short"
    component={Short}
    width={W}
    height={H}
    fps={FPS}
    durationInFrames={durationOf(sample as ShortProps)}
    defaultProps={sample as ShortProps}
    calculateMetadata={({ props }) => ({ durationInFrames: durationOf(props) })}
  />
  </>
);
