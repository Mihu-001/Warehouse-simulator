import { useEffect, useRef } from 'react';

export default function useCanvasRenderer(canvasRef, drawFn, deps = []) {
  const drawFnRef = useRef(drawFn);

  // Keep drawFn updated so the loop always calls the latest logic
  useEffect(() => {
    drawFnRef.current = drawFn;
  }, [drawFn]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    let animationFrameId;

    const renderLoop = () => {
      if (drawFnRef.current) {
        drawFnRef.current();
      }
      animationFrameId = requestAnimationFrame(renderLoop);
    };

    // Start loop
    renderLoop();

    // Clean up
    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, deps); // Re-run when dependencies change
}
