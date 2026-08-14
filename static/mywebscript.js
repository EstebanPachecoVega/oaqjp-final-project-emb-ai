let RunSentimentAnalysis = ()=>{
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            // Handle both success (200) and error (400) responses
            if (this.status == 200) {
                document.getElementById("system_response").innerHTML = this.responseText;
            } else {
                // For status codes other than 200 (e.g., 400 Bad Request)
                document.getElementById("system_response").innerHTML = this.responseText;
                // Optional: Add styling to highlight errors
                // document.getElementById("system_response").style.color = "red";
            }
        }
    };
    xhttp.open("GET", "/emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
}