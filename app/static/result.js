function toggleContent(id) {
    const contentDiv = document.getElementById(`content-${id}`);
    contentDiv.classList.toggle('hidden');
}

function showContent(id, content) {
    // List of all tab IDs
    const tabs = ["transcript-tab", "summary-tab", "blog-tab", "details-tab"];

    // Hide all tabs
    tabs.forEach((tab) => {
      document.getElementById(`${tab}-${id}`).classList.add("hidden");
    });

    // Show the selected tab
    document.getElementById(`${content}-${id}`).classList.remove("hidden");
  }
  function copyContent(videoId, tabId) {
  // Select the content inside the specified tab
  const contentToCopy = document.querySelector(`#${tabId}-${videoId} github-md`).innerText;

  // Create a temporary textarea element to hold the text
  const tempTextArea = document.createElement("textarea");
  tempTextArea.value = contentToCopy;
  document.body.appendChild(tempTextArea);

  // Select the text inside the textarea
  tempTextArea.select();
  tempTextArea.setSelectionRange(0, 99999); // For mobile devices

  // Copy the text to the clipboard
  document.execCommand("copy");

  // Remove the temporary textarea element
  document.body.removeChild(tempTextArea);

  // Find the icon and copied message elements
  const copyIcon = document.querySelector(`#copy-${tabId}-${videoId}`);
  const copiedMessage = document.querySelector(`#copied-message-${tabId}-${videoId}`);

  // Hide the icon and show the "Copied!" message
  copyIcon.classList.add("hidden");
  copiedMessage.classList.remove("hidden");

  // Revert back to original state after 3 seconds
  setTimeout(() => {
    copiedMessage.classList.add("hidden");
    copyIcon.classList.remove("hidden");
  }, 3000);
}
