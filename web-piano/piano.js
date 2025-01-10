class Piano {
    constructor() {
        this.synth = new Tone.Synth().toDestination();
        this.volume = 0.5;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Teclas do piano
        document.querySelectorAll('.key').forEach(key => {
            key.addEventListener('mousedown', () => this.playNote(key.dataset.note));
            key.addEventListener('mouseup', () => this.stopNote(key.dataset.note));
            key.addEventListener('mouseleave', () => this.stopNote(key.dataset.note));
        });

        // Teclas do teclado
        document.addEventListener('keydown', (e) => {
            const key = document.querySelector(`.key[data-key="${e.key}"]`);
            if (key && !e.repeat) {
                this.playNote(key.dataset.note);
                key.classList.add('active');
            }
        });

        document.addEventListener('keyup', (e) => {
            const key = document.querySelector(`.key[data-key="${e.key}"]`);
            if (key) {
                this.stopNote(key.dataset.note);
                key.classList.remove('active');
            }
        });

        // Volume
        document.getElementById('volume').addEventListener('input', (e) => {
            this.volume = parseFloat(e.target.value);
            this.synth.volume.value = Tone.gainToDb(this.volume);
        });
    }

    playNote(note) {
        this.synth.triggerAttack(note);
        const key = document.querySelector(`[data-note="${note}"]`);
        if (key) key.classList.add('active');
    }

    stopNote(note) {
        this.synth.triggerRelease();
        const key = document.querySelector(`[data-note="${note}"]`);
        if (key) key.classList.remove('active');
    }
}

// Inicializar o piano quando a página carregar
window.addEventListener('load', () => {
    new Piano();

    // Smooth scroll para links da navegação
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Animação de fade-in para os cards de features
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });

    // Navegação fixa com mudança de cor no scroll
    const nav = document.querySelector('nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });
});
