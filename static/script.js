async function sendMessage() {

    const inputField = document.getElementById("user-input");
    const message = inputField.value;

    if (!message) {
        return;
    }

    // Show user message
    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    inputField.value = "";

    try {

        // API Request
        const response = await fetch("/chatbot", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Show bot reply
        chatBox.innerHTML += `
            <div class="bot-message">
                ${data.reply}
            </div>
        `;

    } catch (error) {

        console.error("Error:", error);

        chatBox.innerHTML += `
            <div class="bot-message">
                Server Error
            </div>
        `;
    }
}