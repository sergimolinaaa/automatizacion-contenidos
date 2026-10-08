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
  | { type: "quiz"; at: number; question?: string; options: { text: string; at?: number }[]; footer?: string };

export type Scene = {
  start: number;
  end: number;
  chapter: number; // índice en `chapters`
  number?: string | null; // número grande junto al titular (p. ej. "1")
  headline: string; // usa *asteriscos* para resaltar
  mascot?: { pose?: Pose; side?: "left" | "right"; look?: "left" | "right" | "up" | "down" | "center" };
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
  outro?: { at: number; cta?: string } | null;
  endPadding?: number;
};
