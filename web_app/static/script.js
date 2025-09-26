const urlParams = new URLSearchParams(window.location.search);
const query = urlParams.get("q");       // "test"
var results = document.getElementById("results");
results.innerText = query;
console.log(query);

function slugify(productName) {
  return productName
    .toLowerCase()
    .replace(/[-,\\%+ ]+/g, '_')       // dash first
    .replace(/_+/g, '_')               // collapse multiple underscores
    .replace(/^_+|_+$/g, '');          // trim leading/trailing underscores
}

currentDomain = 'http://127.0.0.1:5001';

// Function to fetch search results from API
async function performSearch(query) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = "<div class='loader'></div>";

    try {
        const response = await fetch(`${currentDomain}/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        resultsContainer.innerHTML = '';
        if (data && data.length > 0) {
            data.forEach(item => {
                const li = document.createElement('div');
                li.innerHTML = `<a href="/leki/${slugify(item.nazwa_produktu)}" target="_blank">
                    <h2>${item.nazwa_produktu}</h2>
                    <p>Kod ATC: ${item.kod_atc}</p>
                    <p>Nazwa powszechna: ${item.nazwa_powszechna} (${item.moc})</p>
                    <p>Grupa ATC: ${item.grupa_atc}</p>
                    <p>Vector rank: ${item.vector_rank}, FTS rank: ${item.fts_rank}</p>
                    <p class="headline">Headline: ${item.ts_headline}</p>
                </a>
                `;
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