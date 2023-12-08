let recognition;

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

    // Set up properties for speech recognition
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    // Event listener for when speech recognition is complete
    recognition.onresult = function(event) {
        transcription = event.results[0][0].transcript;
        document.getElementById("transcription").innerText = "Transcription: " + transcription;
    };

    // Event listener for errors in speech recognition
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };

    // Button click event listener to start speech recognition
    document.getElementById("startSpeechRecognition").addEventListener("click", function() {
        recognition.start();
    });

    // Button click event listener to read transcription
    document.getElementById("readTranscription").addEventListener("click", function() {
        Text_To_Speech(transcription);
    });
}

// Function to convert text to speech
function Text_To_Speech(text) {
    let utterance = new SpeechSynthesisUtterance();
    utterance.text = text;
    utterance.voice = window.speechSynthesis.getVoices()[3];
    window.speechSynthesis.speak(utterance);
}
