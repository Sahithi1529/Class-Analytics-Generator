// Wait for the document to load before applying animations
document.addEventListener('DOMContentLoaded', () => {
    // Navbar animation
    gsap.to('#nav-bar', {
        opacity: 1,
        duration: 0.8,
        delay: 0.2,
        ease: "power2.out"
    });

    // Nav items animation
    gsap.to('#nav-bar li', {
        opacity: 1,
        y: 0,
        duration: 0.8,
        stagger: 0.1,
        delay: 0.4,
        ease: "power2.out"
    });

});
