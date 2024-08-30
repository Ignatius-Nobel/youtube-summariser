const addButton = document.getElementById('add-input')
const linkInputContainer = document.getElementById('link-input-container')
const linkInput = document.getElementById('link-input')
const linkErrorMessage = document.getElementById('link-error-message')

// click addButton to add input field

addButton.addEventListener('click',() => {

        // Create a new div for the input group
        const inputGroup = document.createElement('div');
        inputGroup.className = 'flex justify-evenly gap-2 mb-5';
    
        // Create a new input field
        const newInput = document.createElement('input');
        newInput.type = 'url';
        newInput.name = 'links';
        newInput.placeholder = 'Enter another YouTube link...';
        newInput.className = 'border border-2 border-black rounded-md grow pl-2';
        newInput.setAttribute('required','required')

        // Create a remove button
        const removeButton = document.createElement('button');
        removeButton.className = 'p-2 rounded-md bg-red-500 text-white font-bold';
        removeButton.textContent = 'Remove';

        // Add event listener to remove the input field
        removeButton.addEventListener('click', () => {
            linkInputContainer.removeChild(inputGroup);
        });
          
        // Append input and remove button to the input group
        inputGroup.appendChild(newInput);
        inputGroup.appendChild(removeButton);

        // Append the input group to the container
        linkInputContainer.appendChild(inputGroup);
})

linkInput.addEventListener('input', () => {
    linkErrorMessage.style.display = "none"
})

// progress bar

    window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        // If the page was restored from the cache (indicating a back button was used), refresh the page
        window.location.reload();
    }
});

    const progressBar = document.getElementById('progress-bar');
    const progressPercent = document.getElementById('progress-percent');
    const linkForm = document.getElementById('link-form');
    const progressContainer = document.getElementById('progress-container');
    let intervalId
    let isFormSubmitted = false;
    function updateProgress() {
        fetch('/get-progress/')
            .then(response => response.json())
            .then(data => {
                const progress = data.progress;
                console.log(progress)
                progressBar.style.width = `${progress}%`;
                progressPercent.innerText = `${progress}%`;

                if (progress >= 100) {
                    // clearInterval(intervalId);
                    console.log('Processing complete!');
                    progressContainer.classList.add("hidden")
                    clearInterval(intervalId)
                }
            })
            .catch(error => console.error('Error fetching progress:', error));
    }
    
    linkForm.addEventListener('submit', (event) => {
    if (!isFormSubmitted) {
        isFormSubmitted = true; // Set the flag to true when the form is intentionally submitted
        
        event.preventDefault(); // Prevent the default form submission

        // Reset progress bar to 0% and make it visible
        progressBar.style.width = '0%';
        progressPercent.innerText = '0%';
        progressContainer.classList.remove("hidden");

        // Call updateProgress and start polling every second
        updateProgress();
        if (intervalId !== null) {
            clearInterval(intervalId); // Clear any existing interval
        }
        intervalId = setInterval(updateProgress, 1000); // Start a new interval

        linkForm.submit(); // Proceed with form submission after setting up the progress tracking
    }
    isFormSubmitted = false;
});