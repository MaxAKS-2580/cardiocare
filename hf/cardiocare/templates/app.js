import { GoogleGenerativeAI } from "@google/generative-ai";

const API_KEY = 'AIzaSyARB4TSTJT1FRU0vsi2l7RPIUcHg1vyGfc'; 
const genAI = new GoogleGenerativeAI(API_KEY);

const defaultPrompt = "You are assigned as cardiac patient assistance chat bot. You are not allowed to share any info other than cardiac. The patient's name is Fivye Prakash, age 18, heart patient, height 165cm, weight 70kg, gender male. Give friendly yet precise responses. Avoid phrases like 'I understand' and keep responses short. Use emojis like 🔵 or 🔴 for points. Provide first aid advice when needed. Patient is Indian, so 911 should not be referenced.";

let conversationHistory = `${defaultPrompt}\n`;

document.getElementById('promptForm').addEventListener('submit', async function(event) {
  event.preventDefault();

  const prompt = document.getElementById('prompt').value;
  if (prompt.trim() === '') return;

  addMessageToChat(prompt, 'user-message');

  conversationHistory += `User: ${prompt}\n`;
  document.getElementById('prompt').value = '';

  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(conversationHistory);
    const botResponse = result.response.text();

    conversationHistory += `${botResponse}\n`;
    addMessageToChat(botResponse, 'bot-message');

    const botMessageDiv = document.querySelector('.bot-message:last-child');
    botMessageDiv.innerHTML = ''; 
    typeWriterEffect(botResponse, botMessageDiv);

    // Call Text-to-Speech for the bot's response
    // speakText(botResponse);

  } catch (error) {
    addMessageToChat(`Error: ${error.message}`, 'bot-message');
  }
});

document.getElementById('prompt').addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault(); 
    document.getElementById('promptForm').dispatchEvent(new Event('submit')); 
  }
});

function addMessageToChat(text, className) {
  const chatWindow = document.getElementById('chatWindow');

  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', className);
  messageDiv.innerHTML = text;
  chatWindow.appendChild(messageDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function typeWriterEffect(text, element) {
  let index = 0;
  function typeNextChar() {
    if (index < text.length) {
      element.innerHTML += text.charAt(index);
      index++;
      setTimeout(typeNextChar, 30); 
    }
  }
  typeNextChar();
}

// Text-to-Speech Function
// function speakText(text) {
//   const utterance = new SpeechSynthesisUtterance(text);
//   utterance.lang = 'en-IN'; // Set language and accent (Indian English)
//   utterance.rate = 1;       // Set rate of speech, 1 is normal speed
//   utterance.pitch = 1;      // Set pitch, 1 is default

//   window.speechSynthesis.speak(utterance);
// }
