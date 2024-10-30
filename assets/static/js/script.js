// Import dependencies
import axios from 'axios';

// DOM Elements
const promptForm = document.getElementById('prompt-form');
const promptInput = document.getElementById('prompt-input');
const responseOutput = document.getElementById('response-output');
const loadingIndicator = document.getElementById('loading-indicator');

// Event Listeners
promptForm.addEventListener('submit', handlePromptSubmit);

// Functions and Methods
function validateInput(prompt) {
  if (!prompt || prompt.trim() === '') {
    displayError('Please provide a valid prompt.');
    return false;
  }

  // Additional validation rules (e.g., character limits) can be added here
  return true;
}

async function sendPromptToAPI(prompt) {
  try {
    showLoadingIndicator();
    const response = await axios.post('/api/generate_response', { prompt });
    displayResponse(response.data.response);
  } catch (error) {
    displayError('An error occurred while processing your request. Please try again later.');
  } finally {
    hideLoadingIndicator();
  }
}

function displayResponse(response) {
  responseOutput.textContent = response;
}

function displayError(errorMessage) {
  responseOutput.textContent = errorMessage;
  responseOutput.classList.add('error-message');
}

function showLoadingIndicator() {
  loadingIndicator.style.display = 'block';
}

function hideLoadingIndicator() {
  loadingIndicator.style.display = 'none';
  responseOutput.textContent = '';
  responseOutput.classList.remove('error-message');
}

// Handle Form Submission
function handlePromptSubmit(event) {
  event.preventDefault();

  const prompt = promptInput.value;

  if (validateInput(prompt)) {
    sendPromptToAPI(prompt);
  }
}