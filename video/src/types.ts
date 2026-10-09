// Formato del JSON que genera el pipeline (Python) y consume el vídeo.
// Todos los tiempos están en segundos absolutos desde el inicio del vídeo.

export type Word = { text: string; start: number; end: number };

export type Pose = "idle" | "point" | "wave" | "think" | "surprise" | "explain" | "cheer";

export type IconName =
  | "atom" | "earth" | "moon" | "sun" | "paper" | "dna" | "brain" | "drop" | "bolt"
  | "rocket" | "clock" | "eye" | "bacteria" | "star" | "ruler" | "heart" | "fire" | "snow"
  | "magnet" | "planet" | "microscope" | "leaf" | "bone" | "wave";

export type Element =
  | { type: "stat"; at: number; label?: string; value: number; from?: number; decimals?: number; unit?: string; prefix?: string; note?: string }
  | { type: "fact"; at: number; label?: string; text: string; tone?: "paper" | "accent" | "ink" }
  | { type: "icon"; at: number; icon: IconName; label?: string }
  | { type: "compare"; at: number; label?: string; rows: { label: string; value: number; display?: string; at?: number }[]; log?: boolean }
  | { type: "dots"; at: number; label?: string; filled: number; total?: number; caption?: string }
  | { type: "list"; at: number; label?: string; items: { text: string; at?: number }[]; numbered?: boolean }
  | { type: "scale"; at: number; label?: string; from: string; to: string; progress: number; marker?: string }
  | { type: "tag"; at: number; text: string; tone?: "accent" | "ink" | "hot" }
  | { type: "stamp"; at: number; text: string; tone?: "accent" | "hot" }
  | { type: "follow"; at: number; text?: string }
  | { type: "ask"; at: number; text: string; footer?: string }
  | { type: "quiz"; at: number; question?: string; options: { text: string; at?: number }[]; footer?: string };

/** Animación aplicada a un elemento (id) de la ilustración SVG. */
export type IllustrationAnim = {
  target: string; // id del elemento SVG (sin '#')
  effect:
    | "pop" | "fade" | "draw" | "grow" | "slide-left" | "slide-right" | "slide-up" | "slide-down" // entradas
    | "float" | "bob" | "sway" | "spin" | "pulse" | "shake" | "wiggle" | "flow" | "blink" // bucles
    | "ripple" | "breathe" | "drift" // bucles: onda que se expande, respiración, deriva lateral
    | "move" | "hide" | "punch" // acciones puntuales (punch: golpe de énfasis)
    | "zoom"; // solo con target "camera": acerca la cámara a `to` ([x, y] del viewBox) con `amount` = zoom
  phase?: number; // desfase de los bucles (0-1), p. ej. para ondas sucesivas
  at?: number; // segundos (absolutos). Bucles sin `at` empiezan desde el principio de la escena
  dur?: number; // segundos
  to?: [number, number]; // para "move": desplazamiento en unidades del viewBox
  rotate?: number; // para "move": giro final en grados
  amount?: number; // intensidad de los bucles (1 = normal)
  origin?: "center" | "bottom" | "top" | "left" | "right" | "bottom-left" | "bottom-right" | "top-left" | "top-right";
};

export type Illustration = {
  svg: string; // SVG completo con viewBox "0 0 1000 700"
  anims?: IllustrationAnim[];
  caption?: string; // rótulo pequeño en la esquina
};

export type MascotCameo = {
  at: number; // cuándo aparece
  until?: number; // cuándo se va (por defecto, fin de escena)
  pose?: Pose;
  note?: string; // texto del bocadillo
  side?: "left" | "right";
};

export type Scene = {
  start: number;
  end: number;
  chapter: number; // índice en `chapters`
  number?: string | null; // número grande junto al titular (p. ej. "1")
  headline: string; // usa *asteriscos* para resaltar
  signature?: boolean; // escena-firma: el nombre de la cuenta irrumpe en pantalla
  illustration?: Illustration | null;
  mascot?: MascotCameo | null; // el matraz solo aparece si se indica
  elements?: Element[];
};

export type ShortProps = {
  source?: string;
  chapters: string[];
  scenes: Scene[];
  words: Word[];
  audio?: string | null;
  music?: string | null;
  musicVolume?: number;
  sfx?: string | null;
  sfxVolume?: number;
  outro?: { at: number; cta?: string } | null;
  endPadding?: number;
};
