function loadProjects(type) {
    var jsonFileName = "/static/project-data/default_projects.json"

    fetch(jsonFileName)
        .then(response => response.json())
        .then(projects => {
            const urlParams = new URLSearchParams(window.location.search);
            const sortByDate = urlParams.get('sortByDate') === 'true';

            
            // Filter projects based on 'type' and 'tags'
            if (type && type != "all") {
                projects = projects.filter(project => {
                    // Check if 'tags' exists and includes the specified 'type'
                    return project.tags ? project.tags.includes(type) : false;
                });
            }
            if (true) {
                projects.sort((a, b) => parseInt(a.date) + parseInt(b.date));
            }

            displayProjectsOnPage(projects);
        })
        .catch(error => console.error('Error loading projects:', error));
}

function displayProjectsOnPage(projects) {
    const projectsContainer = document.getElementById('projectsContainer'); // Assuming there's a container element with this ID

    projects.forEach(project => {
        const projectLink = document.createElement('a');
        projectLink.href = project.url || '/'; // Use the URL from the project data if available, otherwise, go to index.html
        projectLink.className = 'project-link';

        const projectElement = document.createElement('div');
        projectElement.className = 'project-container';

        const img = document.createElement('img');
        img.className = 'project-picture';
        img.src = project.imgSrc;

        const title = document.createElement('h4');
        title.innerHTML = `<strong>${project.title}</strong> <em class="project-date">${project.date}</em>`;

        projectElement.appendChild(img);
        projectElement.appendChild(title);
        projectLink.appendChild(projectElement); // Append the project container to the link
        projectsContainer.appendChild(projectLink); // Append the link to the projects container
    });
}
// Call loadProjects when the page loads
var scriptTag = document.currentScript || document.querySelector('script[src*="loadprojects.js"]');
var tags = scriptTag.getAttribute('tags');
loadProjects(tags);
