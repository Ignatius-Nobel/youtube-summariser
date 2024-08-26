function toggleContent(id) {
    const contentDiv = document.getElementById(`content-${id}`);
    contentDiv.classList.toggle('hidden');
}

document.getElementById('transcript-button').addEventListener('click',() => {
    document.getElementById('transcript-tab').classList.remove("hidden")
    document.getElementById('blog-tab').classList.add("hidden")
    document.getElementById('summary-tab').classList.add("hidden")
})
document.getElementById('summary-button').addEventListener('click',() => {
    document.getElementById('summary-tab').classList.remove("hidden")
    document.getElementById('transcript-tab').classList.add("hidden")
    document.getElementById('blog-tab').classList.add("hidden")
})
document.getElementById('blog-button').addEventListener('click',() => {
    document.getElementById('blog-tab').classList.remove("hidden")
    document.getElementById('transcript-tab').classList.add("hidden")
    document.getElementById('summary-tab').classList.add("hidden")
})
