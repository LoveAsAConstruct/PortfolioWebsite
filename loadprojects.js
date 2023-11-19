 // JavaScript code to create a parallax effect
 const titleImageText = document.querySelector('.title-image-text');
 const titleImageContainer = document.querySelector('.title-image-container');

 window.addEventListener('scroll', () => {
 const scrollY = window.scrollY;
 const speed = 0.5; // Adjust the speed of the parallax effect

 // Calculate the translateY value for the text
 const translateY = scrollY * speed;

 // Apply the transform to the text element
 titleImageText.style.transform = `translateY(${translateY}px)`;
 });
function getJsonFileName() {
    // This function determines the correct JSON file to load based on the current HTML file name.
    var currentPage = window.location.pathname.split('/').pop();

    // Remove the '.html' extension and append '_projects.json' to match the naming convention
    var jsonFileName = 'Project Data/' + currentPage.replace('.html', '.json');

    return jsonFileName;
}
function loadProjects() {
    var jsonFileName = getJsonFileName();

    fetch(jsonFileName)
        .then(response => response.json())
        .then(projects => {
            // Check for a query parameter 'sortByDate'
            const urlParams = new URLSearchParams(window.location.search);
            const sortByDate = urlParams.get('sortByDate') === 'true';

            if (sortByDate) {
                // Sort the projects by date
                projects.sort((a, b) => {
                    // Assuming each project has a 'date' field in YYYY format
                    return parseInt(a.date) - parseInt(b.date);
                });
            }

            displayProjectsOnPage(projects);
        })
        .catch(error => console.error('Error loading projects:', error));
}

function displayProjectsOnPage(projects) {
    const projectsContainer = document.getElementById('projectsContainer'); // Assuming there's a container element with this ID

    projects.forEach(project => {
        const projectLink = document.createElement('a');
        projectLink.href = project.url || 'index.html'; // Use the URL from the project data if available, otherwise, go to index.html
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
loadProjects();
