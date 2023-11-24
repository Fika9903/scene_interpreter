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

// Function to handle sending a message
function sendMessageHelper(userInput) {
    if (userInput.trim() !== "") {
        var userBubble = document.createElement("div");
        userBubble.className = "user_bubble";
        var userText = document.createElement("p"); // Creating a p tag
        userText.innerText = userInput;
        userText.style.padding = "10px";
        userBubble.appendChild(userText); // Appending p tag to the div
        chatbox.appendChild(userBubble);

        var botBubble = document.createElement("div");
        botBubble.className = "Bot_Bubble";
        var botText = document.createElement("p"); // Creating a p tag
      
        botText.innerText = "The red cube has now moved to the left and all the other cubesa are in the same place"
        
        botText.style.padding = "30px";
        
        botBubble.appendChild(botText); // Appending p tag to the div
        chatbox.appendChild(botBubble);

        document.getElementById("UserInput").value = "";

        // Smooth scrolling effect
        botBubble.scrollIntoView({ behavior: 'smooth' });
    }
}

// Function to handle key press events
document.getElementById("UserInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessageHelper(e.target.value);
    }
});

document.querySelector("#asker button").addEventListener("click", sendMessage);
