/**
 * SamAashwas - Pure Web Audio Synthesizer Engine
 * 100% self-contained synthesized sound effects using standard HTML5 AudioContext.
 * Zero external audio files or downloads needed. Works offline and low-bandwidth.
 */

class CivicAudioEngine {
  constructor() {
    this.ctx = null;
    this.enabled = localStorage.getItem('civic_audio_enabled') !== 'false'; // Default enabled
  }

  _initContext() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  toggleSound() {
    this.enabled = !this.enabled;
    localStorage.setItem('civic_audio_enabled', this.enabled ? 'true' : 'false');
    this.updateSoundButtonUI();
    if (this.enabled) {
      this.playClick();
      if (typeof showStickerToast === 'function') {
        showStickerToast('🔊 Sound Effects Enabled! Enjoy tactile civic feedback.', 'info', 2000);
      }
    } else {
      if (typeof showStickerToast === 'function') {
        showStickerToast('🔇 Sound Effects Muted.', 'info', 2000);
      }
    }
    return this.enabled;
  }

  updateSoundButtonUI() {
    const btn = document.getElementById('btn-sound-toggle');
    if (btn) {
      btn.innerHTML = this.enabled ? '🔊 Sound: ON' : '🔇 Sound: OFF';
      btn.classList.toggle('active', this.enabled);
    }
  }

  // 1. Tactile Neo-Brutalist Mechanical Click
  playClick() {
    if (!this.enabled) return;
    try {
      this._initContext();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const now = this.ctx.currentTime;

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.exponentialRampToValueAtTime(70, now + 0.04);

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.05);
    } catch (e) {
      // AudioContext policy fallback
    }
  }

  // 2. Smooth Tab / Skin Switch Pop
  playTabSwitch() {
    if (!this.enabled) return;
    try {
      this._initContext();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const now = this.ctx.currentTime;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(340, now);
      osc.frequency.exponentialRampToValueAtTime(520, now + 0.07);

      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.07);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.08);
    } catch (e) {}
  }

  // 3. Celebratory Grievance Resolved / Karma Earned Fanfare (Ascending Major Chime)
  playSuccessFanfare() {
    if (!this.enabled) return;
    try {
      this._initContext();
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      // C5, E5, G5, C6 arpeggio notes
      const notes = [523.25, 659.25, 783.99, 1046.50];
      notes.forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        const noteStart = now + i * 0.09;

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, noteStart);

        gain.gain.setValueAtTime(0.001, noteStart);
        gain.gain.linearRampToValueAtTime(0.25, noteStart + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.001, noteStart + 0.28);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(noteStart);
        osc.stop(noteStart + 0.3);
      });
    } catch (e) {}
  }

  // 4. Jan Sunwai / Critical Hazard Two-Tone Bell Chime
  playAlertBell() {
    if (!this.enabled) return;
    try {
      this._initContext();
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      const tones = [880, 1320];
      tones.forEach((freq) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now);

        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.46);
      });
    } catch (e) {}
  }

  // 5. Municipal Inspector Whistle Sound
  playInspectorWhistle() {
    if (!this.enabled) return;
    try {
      this._initContext();
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(1400, now);
      osc.frequency.linearRampToValueAtTime(1800, now + 0.08);
      osc.frequency.linearRampToValueAtTime(1600, now + 0.16);

      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.22);
    } catch (e) {}
  }

  // 6. Confetti Pop / Bubble sound
  playConfettiPop() {
    if (!this.enabled) return;
    try {
      this._initContext();
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(400, now);
      osc.frequency.exponentialRampToValueAtTime(950, now + 0.08);

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.1);
    } catch (e) {}
  }
}

// Global singleton instance
window.civicAudio = new CivicAudioEngine();
