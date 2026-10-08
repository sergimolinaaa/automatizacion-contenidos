import { Composition, continueRender, delayRender } from "remotion";
import { FPS, H, W } from "./brand";
import { fontsReady } from "./fonts";
import { Short } from "./Short";
import sample from "./sample-props.json";
import type { ShortProps } from "./types";

const handle = delayRender("fuentes");
fontsReady.then(() => continueRender(handle));

const durationOf = (p: ShortProps) => {
  let end = Math.max(...p.scenes.map((s) => s.end));
  if (p.outro) end = Math.max(end, p.outro.at + 2.6);
  return Math.ceil(end * FPS);
};

export const Root: React.FC = () => (
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
);
