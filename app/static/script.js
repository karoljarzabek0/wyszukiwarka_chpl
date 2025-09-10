//https://karoljarzabek.pl/api/search?q=null

const urlParams = new URLSearchParams(window.location.search);
const query = urlParams.get("q");       // "test"
var results = document.getElementById("results");
results.innerText = query;
console.log(query);

// Function to fetch search results from API
async function performSearch(query) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = "<li>Loading...</li>";

    try {
        const response = await fetch(`https://karoljarzabek.pl/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        resultsContainer.innerHTML = '';
        if (data.results && data.results.length > 0) {
            data.results.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                resultsContainer.appendChild(li);
            });
        } else {
            resultsContainer.innerHTML = "<li>No results found.</li>";
        }
    } catch (error) {
        resultsContainer.innerHTML = "<li>Error fetching data.</li>";
        console.error(error);
    }
    }

// Update URL with query parameter and trigger search
function updateURLAndSearch() {
const query = document.getElementById('searchBox').value;
if (!query) return;
const newURL = `${window.location.pathname}?q=${encodeURIComponent(query)}`;
window.history.pushState({path: newURL}, '', newURL);
performSearch(query);
}

// Auto-run search if 'q' parameter exists in URL
window.addEventListener('DOMContentLoaded', () => {
const params = new URLSearchParams(window.location.search);
const query = params.get('q');
if (query) {
    document.getElementById('searchBox').value = query;
    performSearch(query);
}
});