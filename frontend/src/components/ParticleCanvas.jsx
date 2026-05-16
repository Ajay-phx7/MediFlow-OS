import { useEffect, useRef } from 'react';

const ParticleCanvas = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height, particles = [];
    const particleCount = 2000;
    const crossPoints = [];
    let phase = 0; // 0: floating, 1: assembling, 2: dispersion
    let timer = 0;
    let animationFrameId;

    const resize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    const createCrossPoints = () => {
      crossPoints.length = 0;
      const size = Math.min(width, height) * 0.25;
      const thickness = size * 0.3;
      const step = 4;

      // Calculate gap between header and hero title for vertical centering
      const header = document.getElementById('main-header');
      const heroTitle = document.querySelector('#hero-section h1');

      let centerY;
      if (header && heroTitle) {
        const headerBottom = header.getBoundingClientRect().bottom;
        const heroTop = heroTitle.getBoundingClientRect().top;
        centerY = headerBottom + (heroTop - headerBottom) / 2;
      } else {
        centerY = height * 0.25; // Fallback
      }

      // Vertical bar
      for (let x = -thickness / 2; x < thickness / 2; x += step) {
        for (let y = -size / 2; y < size / 2; y += step) {
          crossPoints.push({ x: width / 2 + x, y: centerY + y });
        }
      }
      // Horizontal bar
      for (let x = -size / 2; x < size / 2; x += step) {
        for (let y = -thickness / 2; y < thickness / 2; y += step) {
          if (x < -thickness / 2 || x > thickness / 2) {
            crossPoints.push({ x: width / 2 + x, y: centerY + y });
          }
        }
      }
    };

    const init = () => {
      resize();
      createCrossPoints();
      particles = [];
      for (let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          originX: Math.random() * width,
          originY: Math.random() * height,
          size: Math.random() * 1.5 + 0.5,
          color: 'rgba(93, 248, 216, ' + (Math.random() * 0.5 + 0.3) + ')',
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          targetX: null,
          targetY: null,
        });
      }
      animate();
    };

    const animate = () => {
      ctx.clearRect(0, 0, width, height);
      timer++;

      if (timer > 300 && phase === 0) phase = 1;
      if (timer > 750 && phase === 1) phase = 2;
      if (timer > 1100) {
        timer = 0;
        phase = 0;
      }

      particles.forEach((p, i) => {
        if (phase === 1) {
          const target = crossPoints[i % crossPoints.length];
          p.x += (target.x - p.x) * 0.025;
          p.y += (target.y - p.y) * 0.025;
          p.color = 'rgba(93, 248, 216, 0.8)';
        } else if (phase === 2) {
          p.x += p.vx * 2.5;
          p.y += p.vy * 2.5;
          p.color = 'rgba(111, 209, 215, 0.4)';
        } else {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > width) p.vx *= -1;
          if (p.y < 0 || p.y > height) p.vy *= -1;
          p.color = 'rgba(59, 117, 151, 0.3)';
        }

        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();

        if (phase === 1 && i % 50 === 0) {
          ctx.shadowBlur = 15;
          ctx.shadowColor = '#5DF8D8';
        } else {
          ctx.shadowBlur = 0;
        }
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    const handleResize = () => {
      resize();
      createCrossPoints();
    };

    window.addEventListener('resize', handleResize);
    
    // Initialize after a short delay to ensure DOM is ready
    const timeoutId = setTimeout(init, 100);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      clearTimeout(timeoutId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      id="particle-canvas"
      className="fixed top-0 left-0 w-full h-full -z-10"
      style={{
        background: 'radial-gradient(circle at center, #093C5D 0%, #001525 100%)',
      }}
    />
  );
};

export default ParticleCanvas;

// Made with Bob
