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