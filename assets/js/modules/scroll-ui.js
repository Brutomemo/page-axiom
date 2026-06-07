// ─── SCROLL PROGRESS ──────────────────────────────── */
    const scrollProgress = document.getElementById('scroll-progress');

    window.addEventListener('scroll', () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = scrollTop / docHeight;
      scrollProgress.style.transform = `scaleX(${scrollPercent})`;
    });

    // ─── INTERSECTION OBSERVER ────────────────────────── */
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translate3d(0, 0, 0)';
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // ─── SMOOTH SCROLL ───────────────────────────────── */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const href = this.getAttribute('href');
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });

    // ─── BUTTON INTERACTIONS ─────────────────────────── */
    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-2px)';
      });

      btn.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0)';
      });
    });

    // ─── CARD HOVER EFFECTS ─────────────────────────── */
    document.querySelectorAll('.card, .skill-tag').forEach(el => {
      el.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-4px)';
      });

      el.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0)';
      });
    });

    document.querySelectorAll('.hero-bar-fill').forEach(el => {
      setTimeout(() => { el.style.width = '12%'; }, 400);
    });
    document.querySelectorAll('.perf-bars .bar').forEach((bar, i) => {
      bar.style.opacity = '0';
      bar.style.transform = 'scaleY(0)';
      bar.style.transformOrigin = 'bottom';
      setTimeout(() => {
        bar.style.transition = 'opacity 0.5s ease, transform 0.6s cubic-bezier(0.22,1,0.36,1)';
        bar.style.opacity = '1';
        bar.style.transform = 'scaleY(1)';
      }, 600 + i * 80);
    });
