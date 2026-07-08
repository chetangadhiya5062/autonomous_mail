const API_URL = "http://localhost:8000/api/v1/benefits";


export async function askBenefits(question) {

    const response = await fetch(`${API_URL}/ask`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
        },

        body: JSON.stringify({
            question,
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to fetch answer.");
    }

    return await response.json();
}