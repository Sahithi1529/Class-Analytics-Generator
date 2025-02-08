gsap.to('.courses-container', {
    opacity: 1,
    y: 0,
    duration: 1,
    ease: 'power2.out'
});

gsap.to('table', {
    opacity: 1,
    duration: 0.8,
    delay: 0.3,
    ease: 'power2.out'
});

gsap.from('.start-session-btn', {
    scale: 0.9,
    duration: 0.5,
    delay: 1,
    stagger: 0.1,
    ease: 'back.out(1.7)'
});