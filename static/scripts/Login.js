// Animate login container
gsap.to('.login-container', {
    opacity: 1,
    y: 0,
    duration: 1.2,
    ease: 'power2.out',
});

// Animate inputs
gsap.to('input', {
    x: 0,
    opacity: 1,
    duration: 1,
    delay: 0.4,
    stagger: 0.15,
    ease: 'power2.out',
});

// Animate button
gsap.to('button', {
    scale: 1,
    opacity: 1,
    duration: 1,
    delay: 0.2,
    ease: 'back.out(1.7)',
});

// Animate toggle password button
gsap.to('.toggle-password', {
    opacity: 1,
    duration: 1,
    delay: 0.7,
    ease: 'power2.out',
});

// Input focus effect
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('focus', () => {
        gsap.to(input, {
            scale: 1.05,
            duration: 0.2,
        });
    });

    input.addEventListener('blur', () => {
        gsap.to(input, {
            scale: 1,
            duration: 0.2,
        });
    });
});

// Toggle password visibility
document.querySelector('.toggle-password').addEventListener('click', function () {
    const passwordInput = document.querySelector('input[name="password"]');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        this.textContent = 'Hide';
    } else {
        passwordInput.type = 'password';
        this.textContent = 'Show';
    }
});