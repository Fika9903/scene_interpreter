var chatbox = document.getElementById("chatbox");

// Function to handle the scroll event
function handleScroll() {
    if (chatbox.scrollTop === 0) {
        // Här ska meddelanden från en API eller server hamna 
    }
}

// Add event listener for the scroll event
chatbox.addEventListener("scroll", handleScroll);

// Function to send a message
function sendMessage() {
    var userInput = document.getElementById("UserInput").value;
    if (userInput.trim() !== "") {
        createBubble(userInput, "user");

        if (shouldAskQuestion(userInput)) {
            askQuestion();
        } else {
            interpretScene();
        }
    }
}

// Function to create a chat bubble
function createBubble(text, type) {
    var bubble = document.createElement("div");
    bubble.className = type === "user" ? "user_bubble" : "bot_bubble";
    var textNode = document.createElement("p"); 
    textNode.innerText = text;
    textNode.style.padding = "10px";
    bubble.appendChild(textNode); 
    chatbox.appendChild(bubble);
    bubble.scrollIntoView({ behavior: 'smooth' });
}

// Function to determine if the input is a question
function shouldAskQuestion(input) {
    // Add logic to determine if the input is a question
    return input.includes('?');
}

async function interpretScene() {
    const sceneDescription = document.getElementById('UserInput').value;
    try {
        const response = await fetch('http://127.0.0.1:5000/interpret', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ scene_description: sceneDescription })
        });
        const data = await response.json();
        createBubble(JSON.stringify(data), "bot");
    } catch (error) {
        console.error('Error during fetch operation: ', error);
        createBubble("Error: " + error, "bot");
    }
}

async function askQuestion() {
    const question = document.getElementById('UserInput').value;
    try {
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();
        createBubble(data.answer, "bot");
    } catch (error) {
        console.error('Error during fetch operation: ', error);
        createBubble("Error: " + error, "bot");
    }
}

// Function to handle key press events
document.getElementById("UserInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

document.querySelector("#asker button").addEventListener("click", sendMessage);
