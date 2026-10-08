import { useLayoutEffect, useRef } from "react";

/**
 * Encaja su contenido en el alto disponible: si no cabe, lo reduce (sin recortar ni
 * solapar con lo de abajo). Se mide sin transformaciones, así que el resultado es estable.
 */
export const Fit: React.FC<{ height: number; width: number; children: React.ReactNode; align?: "top" | "center" }> = ({
  height, width, children, align = "top",
}) => {
  const ref = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    let scale = 1;
    for (let i = 0; i < 4; i++) {
      el.style.width = `${width / scale}px`;
      const natural = el.offsetHeight;
      const next = Math.min(1, height / Math.max(1, natural));
      if (Math.abs(next - scale) < 0.005) break;
      scale = next;
    }
    el.style.width = `${width / scale}px`;
    const offset = align === "center" ? Math.max(0, (height - el.offsetHeight * scale) / 2) : 0;
    el.style.transform = `translateY(${offset}px) scale(${scale})`;
  });
  return (
    <div style={{ position: "relative", height, width }}>
      <div ref={ref} style={{ position: "absolute", top: 0, left: 0, transformOrigin: "0 0" }}>
        {children}
      </div>
    </div>
  );
};
