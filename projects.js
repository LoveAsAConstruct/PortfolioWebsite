

function addHoverEffects() {
    document.querySelectorAll('.project-container').forEach(container => {
        container.addEventListener('mouseenter', () => container.classList.add('project-container-hover'));
        container.addEventListener('mouseleave', () => container.classList.remove('project-container-hover'));
    });
}

document.addEventListener('DOMContentLoaded', renderProjects);
window.addEventListener('resize', renderProjects);
