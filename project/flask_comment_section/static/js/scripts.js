
async function fetchComments() {
    const response = await fetch('/comments');
    const data = await response.json();
    document.getElementById('comments').innerHTML = data.map(c => 
        `<div class="comment"><strong>${c.name}</strong>: ${c.text} <br><small>${c.timestamp}</small></div>`
    ).join('');
}

async function addComment() {
    const name = document.getElementById('name').value;
    const text = document.getElementById('text').value;
    if (!name || !text) return alert('Please fill all fields!');
    
    await fetch('/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, text })
    });
    document.getElementById('name').value = '';
    document.getElementById('text').value = '';
    fetchComments();
}

function downloadExcel() {
    window.location.href = '/download_excel';
}

fetchComments();

