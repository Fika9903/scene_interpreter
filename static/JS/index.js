var chatbox = document.getElementById("chatbox");
// Function to handle the scroll event
function handleScroll() {
    if (chatbox.scrollTop === 0) {
        //här ska medelanden från en api eller server hamna 
    }
}
// Add event listener for the scroll event
chatbox.addEventListener("scroll", handleScroll);
// Function to send a message
function sendMessage() {
    var userInput = document.getElementById("UserInput").value;
    sendMessageHelper(userInput);
}


//text to speach 

function Text_To_Speech(text) {
    let utterance = new SpeechSynthesisUtterance();
    utterance.text = text;
    utterance.voice = window.speechSynthesis.getVoices()[3];
    window.speechSynthesis.speak(utterance);
}

// Function to handle sending a message
function sendMessageHelper(userInput) {
    if (userInput.trim() !== "") {
        var userBubble = document.createElement("div");
        userBubble.className = "user_bubble";
        var userText = document.createElement("p");
        userText.innerText = userInput;
        userText.style.padding = "10px";
        userBubble.appendChild(userText);
        chatbox.appendChild(userBubble);

        var botBubble = document.createElement("div");
        botBubble.className = "Bot_Bubble";
        var botText = document.createElement("p");
        botText.style.padding = "30px";
        botBubble.appendChild(botText);
        chatbox.appendChild(botBubble);

        // Fetch question from the server
        fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Set the botText with the response from the server
            botText.innerText = data.answer;
            botBubble.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error fetching question:', error);
            botText.innerText = "Error: " + error;
        });
        

        document.getElementById("UserInput").value = "";  // Clear the input field
    }

    Text_To_Speach(botText.innerText)
}

// Function to handle key press events
document.getElementById("UserInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessageHelper(e.target.value);
    }
});
document.querySelector("#asker button").addEventListener("click", sendMessage);



sendMessageHelper("Hello, this is a user message.");





