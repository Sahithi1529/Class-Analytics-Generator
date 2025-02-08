// Function to show the upload form
function showUploadForm(type) {
    console.log("Show upload form called for type:", type); // Debug log
    const form = document.getElementById(type + 'Form');
    const overlay = document.getElementById('overlay');

    // Check if the form and overlay elements exist
    if (!form || !overlay) {
        console.error("Form or overlay not found!"); // Log error if elements are not found
        return; // Exit the function if elements are not found
    }

    // Ensure the overlay is displayed
    overlay.style.display = 'block';
    form.style.display = 'block'; // Show form before animating

    // GSAP animation for overlay
    gsap.to(overlay, {
        opacity: 1,
        duration: 0.3,
        ease: "power2.out"
    });

    // GSAP animation for the form
    gsap.fromTo(form,
        {
            opacity: 0,
            y: -50,
            scale: 0.8
        },
        {
            opacity: 1,
            y: 0,
            scale: 1,
            duration: 0.5,
            ease: "back.out(1.7)"
        }
    );
}

// Function to hide the upload form
function hideUploadForm(type) {
    const form = document.getElementById(type + 'Form');
    const overlay = document.getElementById('overlay');

    // Check if the form and overlay elements exist
    if (!form || !overlay) {
        console.error("Form or overlay not found!"); // Log error if elements are not found
        return; // Exit the function if elements are not found
    }

    // GSAP animation for hiding the form and overlay
    gsap.to([form, overlay], {
        opacity: 0,
        duration: 0.3,
        ease: "power2.in",
        onComplete: () => {
            form.style.display = 'none'; // Hide form after animation
            overlay.style.display = 'none'; // Hide overlay after animation
            gsap.set(form, { clearProps: "all" }); // Clear any inline styles
        }
    });
}

// Ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Drag and Drop functionality
    ['csv', 'model'].forEach(type => {
        const dropZone = document.getElementById(type + 'DropZone');
        const input = document.getElementById(type + 'Input');
        const fileNameDisplay = document.getElementById('fileName'); // Element to display the file name

        dropZone.addEventListener('click', () => input.click());

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            input.files = e.dataTransfer.files;
            if (input.files.length > 0) {
                if (fileNameDisplay) { // Check if fileNameDisplay exists
                    fileNameDisplay.textContent = `Uploaded File: ${input.files[0].name}`; // Display the file name
                }
                input.form.submit(); // Submit the form
                hideUploadForm(type); // Automatically close the form after submission
            }
        });

        // Display the file name when a file is selected
        input.addEventListener('change', (e) => {
            if (input.files.length > 0) {
                if (fileNameDisplay) { // Check if fileNameDisplay exists
                    fileNameDisplay.textContent = `Uploaded File: ${input.files[0].name}`; // Display the file name
                }
                input.form.submit(); // Submit the form
                hideUploadForm(type); // Automatically close the form after submission
            } else {
                if (fileNameDisplay) { // Check if fileNameDisplay exists
                    fileNameDisplay.textContent = ''; // Clear the display if no file is selected
                }
            }
        });
    });

    // GSAP Animations for page load
    // Initial body fade in
    gsap.to('body', {
        opacity: 1,
        duration: 0.5,
        ease: "power2.out"
    });

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

    // Title animation
    gsap.to('h1', {
        opacity: 1,
        scale: 1,
        duration: 1,
        delay: 0.6,
        ease: "back.out(1.7)"
    });

    // Upload buttons animation
    gsap.to('.upload-btn', {
        opacity: 1,
        y: 0,
        duration: 0.8,
        stagger: 0.2,
        delay: 0.8,
        ease: "back.out(1.7)"
    });
});