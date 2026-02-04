<template>
    <div class="container fade-in">
      <h1>⏱️ Ready to test your reading speed?</h1>
      <p>Simply stop the timer when you finish reading the paragraph.</p>
  
      <router-link to="/readingspeed">
        <button class="btn">▶️ Start</button>
      </router-link>
    </div>
  </template>
  
  <script setup></script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Baloo+2&family=Fredoka&display=swap');
  
  .container {
    max-width: 700px;
    margin: 5rem auto;
    padding: 2rem;
    text-align: center;
    font-family: 'Baloo 2', 'Fredoka', sans-serif;
    background: linear-gradient(to bottom, #fff5e6, #ffd9ec);
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .btn {
    margin-top: 2rem;
    padding: 0.8rem 1.5rem;
    font-size: 1.2rem;
    background-color: #ffd972;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s;
  }
  
  .btn:hover {
    background-color: #ffc947;
  }
  
  .fade-in {
    animation: fadeIn 0.6s ease-in-out;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  </style>
  