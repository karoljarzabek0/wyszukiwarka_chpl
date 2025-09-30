const urlParams = new URLSearchParams(window.location.search);
const query = urlParams.get("q");       // "test"
var results = document.getElementById("results");

function slugify(productName) {
  return productName
    .toLowerCase()
    .replace(/[-,\\%+ ]+/g, '_')       // dash first
    .replace(/_+/g, '_')               // collapse multiple underscores
    .replace(/^_+|_+$/g, '');          // trim leading/trailing underscores
}

function getAtcIcon(kod_atc) {
  // mapping ATC letters to SVG file names
  const icons = {
    A: "stomach.svg",
    B: "blood.svg",
    C: "heart.svg",
    D: "skin.svg",
    G: "gender.svg",
    H: "hormones.svg",
    J: "virus.svg",
    L: "cancer.svg",
    M: "bones.svg",
    N: "brain.svg",
    P: "bug.svg",
    R: "lungs.svg",
    S: "eye.svg",
    V: "other.svg"
  };

  if (!kod_atc || typeof kod_atc !== "string") {
    return "other.svg";
  }

  const atcLetter = kod_atc.charAt(0).toUpperCase();
  return icons[atcLetter] || "other.svg";
}

//let currentDomain = `${window.location.protocol}//${window.location.hostname}`;
let currentDomain = `https://leki.karoljarzabek.pl`;

// Function to fetch search results from API
async function performSearch(query) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = "<div class='container'><div class='loader'></div></div>";

    try {
        const response = await fetch(`${currentDomain}/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        resultsContainer.innerHTML = '';
        if (data && data.length > 0) {
            data.forEach(item => {
                const li = document.createElement('div');
                const iconFile = getAtcIcon(item.kod_atc);
                li.innerHTML = `
                <div class="ind-med">
                    <div class="ind-med-left">
                    <a href="/leki/${slugify(item.nazwa_produktu)}" target="_blank">
                        <h2>${item.nazwa_produktu}</h2>
                        <p>${item.nazwa_powszechna} (${item.moc})</p>
                    </a>
                    </div>
                    <div class="ind-med-right">
                    <img src="/static/svg/${iconFile}" alt="${item.kod_atc}" title="${item.kod_atc}" width="48" height="48">
                    </div>
                </div>
                    <p class="atc-group">${item.grupa_atc}</p>
                    <p class="headline">"...${item.ts_headline}..."</p>
                
                `;
                resultsContainer.appendChild(li);
            });
        } else {
            resultsContainer.innerHTML = "<p>No results found.</p>";
        }
    } catch (error) {
        resultsContainer.innerHTML = "<p>Error fetching data.</p>";
        console.error(error);
    }
    }

// Update URL with query parameter and trigger search
function updateURLAndSearch() {
const query = document.getElementById('searchBox').value;
if (!query) return;
const newURL = `${window.location.pathname}?q=${encodeURIComponent(query)}`;
window.history.pushState({path: newURL}, '', newURL);
document.title = `Wyniki dla: "${query}"`
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