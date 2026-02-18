import { useRef, useEffect, useCallback } from "react";

/**
 * Jet colormap: maps intensity (0-1) to an RGB triplet.
 */
function jetColor(t) {
  const r = Math.min(1, Math.max(0, 1.5 - Math.abs(4 * t - 3)));
  const g = Math.min(1, Math.max(0, 1.5 - Math.abs(4 * t - 2)));
  const b = Math.min(1, Math.max(0, 1.5 - Math.abs(4 * t - 1)));
  return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}

/**
 * GradCAMCanvas
 *
 * Renders the original brain MRI image with a GradCAM-style heatmap overlay
 * drawn entirely on the client side using the regions returned by Claude.
 *
 * Props:
 *   imageSrc   – data URI or URL of the original scan image
 *   regions    – array of { x, y, w, h, intensity } (normalised 0-1)
 */
export default function GradCAMCanvas({ imageSrc, regions = [] }) {
  const canvasRef = useRef(null);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas || !imageSrc) return;

    const ctx = canvas.getContext("2d");
    const img = new Image();

    img.onload = () => {
      // Match canvas to image dimensions (capped for UI)
      const maxW = 480;
      const scale = Math.min(1, maxW / img.width);
      const w = Math.round(img.width * scale);
      const h = Math.round(img.height * scale);

      canvas.width = w;
      canvas.height = h;

      // Draw original image
      ctx.drawImage(img, 0, 0, w, h);

      if (!regions.length) return;

      // Create off-screen heatmap
      const heatmap = document.createElement("canvas");
      heatmap.width = w;
      heatmap.height = h;
      const hCtx = heatmap.getContext("2d");

      // For each region, paint a radial gradient blob
      regions.forEach((r) => {
        const cx = r.x * w + (r.w * w) / 2;
        const cy = r.y * h + (r.h * h) / 2;
        const rx = (r.w * w) / 2;
        const ry = (r.h * h) / 2;
        const radius = Math.max(rx, ry) * 1.2;

        const [red, green, blue] = jetColor(r.intensity);

        const grad = hCtx.createRadialGradient(cx, cy, 0, cx, cy, radius);
        grad.addColorStop(0, `rgba(${red}, ${green}, ${blue}, ${r.intensity * 0.7})`);
        grad.addColorStop(0.5, `rgba(${red}, ${green}, ${blue}, ${r.intensity * 0.35})`);
        grad.addColorStop(1, `rgba(${red}, ${green}, ${blue}, 0)`);

        hCtx.fillStyle = grad;
        hCtx.fillRect(cx - radius, cy - radius, radius * 2, radius * 2);
      });

      // Composite heatmap onto original
      ctx.globalAlpha = 0.55;
      ctx.drawImage(heatmap, 0, 0);
      ctx.globalAlpha = 1.0;

      // Draw bounding box for the strongest region
      const strongest = regions.reduce(
        (a, b) => (a.intensity > b.intensity ? a : b),
        regions[0]
      );
      ctx.strokeStyle = "#00FF88";
      ctx.lineWidth = 2;
      ctx.setLineDash([6, 4]);
      ctx.strokeRect(
        strongest.x * w,
        strongest.y * h,
        strongest.w * w,
        strongest.h * h
      );
      ctx.setLineDash([]);

      // Label
      ctx.font = "bold 12px monospace";
      ctx.fillStyle = "#00FF88";
      ctx.fillText(
        `Activation ${(strongest.intensity * 100).toFixed(0)}%`,
        strongest.x * w + 4,
        strongest.y * h - 6
      );
    };

    img.src = imageSrc;
  }, [imageSrc, regions]);

  useEffect(() => {
    draw();
  }, [draw]);

  return (
    <div className="gradcam-container">
      <div className="gradcam-header">
        <span className="gradcam-dot"></span>
        GradCAM Activation Map
      </div>
      <canvas ref={canvasRef} className="gradcam-canvas" />
      <div className="gradcam-legend">
        <span className="legend-low">Low</span>
        <div className="legend-bar" />
        <span className="legend-high">High</span>
      </div>
    </div>
  );
}
