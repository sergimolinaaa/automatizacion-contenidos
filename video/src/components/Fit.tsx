import { useLayoutEffect, useRef } from "react";

/**
 * Encaja su contenido en el alto disponible: si no cabe, lo reduce entero y lo centra (sin recortar ni
 * solapar con lo de abajo). No cambia el ancho del contenido, así los paneles mantienen su proporción.
 */
export const Fit: React.FC<{ height: number; width: number; children: React.ReactNode; align?: "top" | "center" }> = ({
  height, width, children, align = "top",
}) => {
  const ref = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.width = `${width}px`;
    const natural = el.offsetHeight;
    const scale = Math.min(1, height / Math.max(1, natural));
    const dx = (width - width * scale) / 2;
    const offset = align === "center" ? Math.max(0, (height - natural * scale) / 2) : 0;
    el.style.transform = `translate(${dx}px, ${offset}px) scale(${scale})`;
  });
  return (
    <div style={{ position: "relative", height, width }}>
      <div ref={ref} style={{ position: "absolute", top: 0, left: 0, transformOrigin: "0 0" }}>
        {children}
      </div>
    </div>
  );
};
