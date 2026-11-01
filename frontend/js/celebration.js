/**
 * SamAashwas - Pure Canvas Civic Celebration Physics Engine
 * Generates fluttering Marigold Petals (गेंदे के फूल) & Indian Tricolor Confetti
 * 100% self-contained HTML5 Canvas animation. Zero external libraries.
 */

class CivicCelebrationEngine {
  constructor() {
    this.canvas = null;
    this.ctx = null;
    this.particles = [];
    this.animationId = null;
    this.active = false;
  }

  _getOrCreateCanvas() {
    if (!this.canvas) {
      let canvas = document.getElementById('civic-celebration-canvas');
      if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'civic-celebration-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '99999';
        document.body.appendChild(canvas);
      }
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this._resizeCanvas();
      window.addEventListener('resize', () => this._resizeCanvas());
    }
  }

  _resizeCanvas() {
    if (this.canvas) {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
    }
  }

  fire(options = {}) {
    this._getOrCreateCanvas();
    if (!this.canvas || !this.ctx) return;

    if (window.civicAudio && typeof window.civicAudio.playConfettiPop === 'function') {
      window.civicAudio.playConfettiPop();
    }

    const count = options.count || 85;
    const originX = options.x !== undefined ? options.x : window.innerWidth * 0.5;
    const originY = options.y !== undefined ? options.y : window.innerHeight * 0.35;

    // Authentic Indian Civic Colors: Marigold Golden, Saffron, Emerald Green, Crisp White, Festive Yellow
    const colors = [
      '#FF6B35', // Saffron
      '#FF9F1C', // Deep Marigold
      '#FFD166', // Bright Marigold
      '#10B981', // Civic Emerald
      '#059669', // Dark Emerald
      '#FFFFFF', // Crisp White
      '#F43F5E', // Rose Crimson
      '#8B5CF6'  // Royal Violet
    ];

    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 9 + 4;
      const isMarigold = Math.random() > 0.45; // 55% marigold petals

      this.particles.push({
        x: originX + (Math.random() - 0.5) * 60,
        y: originY + (Math.random() - 0.5) * 40,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - Math.random() * 4 - 2, // upward initial impulse
        gravity: 0.18 + Math.random() * 0.08,
        drag: 0.965,
        color: colors[Math.floor(Math.random() * colors.length)],
        radiusX: isMarigold ? (Math.random() * 7 + 6) : (Math.random() * 5 + 4),
        radiusY: isMarigold ? (Math.random() * 4 + 3) : (Math.random() * 9 + 5),
        rotation: Math.random() * Math.PI * 2,
        rotationSpeed: (Math.random() - 0.5) * 0.18,
        isMarigold: isMarigold,
        opacity: 1,
        decay: 0.007 + Math.random() * 0.007
      });
    }

    if (!this.active) {
      this.active = true;
      this._animate();
    }
  }

  _animate() {
    if (!this.ctx || !this.canvas) return;

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];

      p.vx *= p.drag;
      p.vy *= p.drag;
      p.vy += p.gravity;
      p.x += p.vx;
      p.y += p.vy;
      p.rotation += p.rotationSpeed;
      p.opacity -= p.decay;

      if (p.opacity <= 0 || p.y > this.canvas.height + 40) {
        this.particles.splice(i, 1);
        continue;
      }

      this.ctx.save();
      this.ctx.translate(p.x, p.y);
      this.ctx.rotate(p.rotation);
      this.ctx.globalAlpha = Math.max(0, p.opacity);

      if (p.isMarigold) {
        // Render Marigold Petal (soft curved ellipse with slight center fold)
        this.ctx.fillStyle = p.color;
        this.ctx.beginPath();
        this.ctx.ellipse(0, 0, p.radiusX, p.radiusY, 0, 0, Math.PI * 2);
        this.ctx.fill();

        // Subtle center petal vein
        this.ctx.strokeStyle = 'rgba(35, 31, 32, 0.25)';
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.moveTo(0, -p.radiusY * 0.7);
        this.ctx.lineTo(0, p.radiusY * 0.7);
        this.ctx.stroke();
      } else {
        // Render Neo-Brutalist Sticker Confetti Ribbon
        this.ctx.fillStyle = p.color;
        this.ctx.strokeStyle = '#231F20';
        this.ctx.lineWidth = 1.2;
        this.ctx.fillRect(-p.radiusX, -p.radiusY, p.radiusX * 2, p.radiusY * 2);
        this.ctx.strokeRect(-p.radiusX, -p.radiusY, p.radiusX * 2, p.radiusY * 2);
      }

      this.ctx.restore();
    }

    if (this.particles.length > 0) {
      this.animationId = requestAnimationFrame(() => this._animate());
    } else {
      this.active = false;
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
  }
}

// Global celebration helper
window.civicCelebration = new CivicCelebrationEngine();
window.fireCivicCelebration = function(x, y) {
  window.civicCelebration.fire({ x, y });
};
