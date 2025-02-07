
// Animate container
gsap.to('.container', {
    opacity: 1,
    y: 0,
    duration: 1.2,
    ease: 'power2.out',
});

// Animate label
gsap.to('label', {
    x: 0,
    opacity: 1,
    duration: 1,
    delay: 0.4,
    ease: 'power2.out',
});

// Animate input
gsap.to('input[type="text"]', {
    x: 0,
    opacity: 1,
    duration: 1,
    delay: 0.6,
    ease: 'power2.out',
});

// Animate submit button
gsap.to('input[type="submit"]', {
    scale: 1,
    opacity: 1,
    duration: 1,
    delay: 0.8,
    ease: 'back.out(1.7)',
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
