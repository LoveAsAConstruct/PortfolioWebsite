function changeFavicon() {
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const favicon = document.getElementById('icon');
  
    if (darkModeMediaQuery.matches) {
      favicon.href = 'images/Site Images/Favicon/favicon-dark.png'; // Path to dark theme favicon
    } else {
      favicon.href = 'images/Site Images/Favicon/favicon-light.png'; // Path to light theme favicon
    }
  }
  
  // Call the function on load
  changeFavicon();
  
  // Add listener for theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addListener(changeFavicon);
  