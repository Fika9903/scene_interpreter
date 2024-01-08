
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

//speech to text
let recognition;
let Transcription = "";
let isReading = false;


if ('webkitSpeechRecognition' in window) {
    // For Chrome
    recognition = new webkitSpeechRecognition();
} else if ('SpeechRecognition' in window) {
    // For Firefox
    recognition = new SpeechRecognition();
} else {
    console.error('Speech recognition not supported in this browser.');
}

if (recognition) {
    let transcription = "";

    // properties för speech rec
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    // Event listener för när speec recon är klart 
    recognition.onresult = function(event) {
        transcription = event.results[0][0].transcript;
        document.getElementById("UserInput").value = "" + transcription;


    };
    

    // Error speech
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };

    // Button click event listener to start speech recognition
    document.getElementById("startSpeechRecognition").addEventListener("click", function() {
        recognition.start();
    });

    // Knapp för speec recon
    document.getElementById("readTranscription").addEventListener("click", function() {
        Text_To_Speech(transcription);
    });
}

document.addEventListener("keydown",function (c){
    if (c.key == "Ö" || c.key == "ö"){
        recognition.start();
    }
})


document.getElementById("UserInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessageHelper(e.target.value);
    }
});

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
        })
        .finally(() =>{
            clearInputField()
        })
        ;

        const readBotMessagesCheckbox = document.getElementById('readBotMessagesCheckbox');
        if (readBotMessagesCheckbox.checked) {
            Text_To_Speech(data.answer);
        }}
    }

function clearInputField() {
    document.getElementById("UserInput").value = "";
}


// Function to handle key press events




document.querySelector("#asker button").addEventListener("click", sendMessage);







