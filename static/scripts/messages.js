// Animate container
document.addEventListener('DOMContentLoaded', () => {

    gsap.to('.container', {
        opacity: 1,
        y: 0,
        duration: 1.2,
        ease: 'power2.out',
    });

    // Animate label
    gsap.to('label', {
        x: 1,
        opacity: 1,
        duration: 1,
        delay: 0.4,
        ease: 'power2.out',
    });

    // Animate input
    gsap.to('input[type="text"]', {
        y: 0,
        opacity: 1,
        duration: 1,
        delay: 0.6,
        ease: 'power2.out',
    });

    // Animate submit button
    gsap.to('input[type="submit"]', {
        y: 0,
        scale: 1,
        opacity: 1,
        duration: 0.5,
        delay: 0.8,
        ease: 'back.out(1.7)',
    });

    gsap.to('.messages-container,.faculty-container', {
        opacity: 1,
        y: 0,
        duration: 1.2,
        ease: 'power2.out',
    });

    gsap.to('table', {
        opacity: 1,
        duration: 1,
        delay: 0.4,
        ease: 'power2.out',
    });

    gsap.from('.generate-btn', {
        scale: 0.9,
        duration: 0.5,
        delay: 1,
        stagger: 0.1,
        ease: 'back.out(1.7)'
    });
});

// Input focus effect
document.querySelector('input[type="text"]').addEventListener('focus', () => {
    gsap.to('input[type="text"]', {
        scale: 1.05,
        duration: 0.2,
    });
});

document.querySelector('input[type="text"]').addEventListener('blur', () => {
    gsap.to('input[type="text"]', {
        scale: 1,
        duration: 0.2,
    });
});
