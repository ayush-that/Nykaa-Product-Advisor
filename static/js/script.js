let scrapedContent = "";

function formatRecommendation(text) {
  return text
    .split("\n")
    .map((line) => {
      if (line.trim().startsWith("RECOMMENDED PRODUCT:")) {
        return "RECOMMENDED PRODUCT:";
      }
      return line;
    })
    .join("\n");
}

async function analyzeUrl() {
  const url = document.getElementById("url").value;
  const analyzeBtn = document.getElementById("analyzeBtn");

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    scrapedContent = data.content;
    document.getElementById("recommendationSection").classList.remove("hidden");
  } catch (error) {
    document.getElementById("result").innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                ${error.message}
            </div>`;
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze";
  }
}

async function getRecommendation() {
  const question = document.getElementById("question").value;
  const recommendBtn = document.getElementById("recommendBtn");

  recommendBtn.disabled = true;
  recommendBtn.textContent = "Getting Recommendation...";

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: scrapedContent,
        question: question,
      }),
    });

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    document.getElementById("result").innerHTML = `
            <div class="rounded-lg shadow-md p-6 bg-gray-800">
                <h3 class="text-xl font-semibold mb-4 text-gray-100">Your Personalized Recommendation:</h3>
                <div class="recommendation-content prose prose-invert text-gray-200">
                    ${formatRecommendation(data.recommendation)}
                </div>
            </div>`;
  } catch (error) {
    document.getElementById("result").innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                ${error.message}
            </div>`;
  } finally {
    recommendBtn.disabled = false;
    recommendBtn.textContent = "Get Recommendations";
  }
}
