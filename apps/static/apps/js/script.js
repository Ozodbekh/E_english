let time = 60; // Taymerning boshlang'ich qiymati
let timerInterval; // Intervalni global o'zgaruvchida saqlaymiz

// Elementlarni olish
const timerElement = document.getElementById('timer');
const resendButton = document.getElementById('resendButton');

// Taymerni yangilash funksiyasi
function updateTimer() {
    const minutes = Math.floor(time / 60); // Daqiqalarni hisoblash
    const seconds = time % 60; // Sekundlarni hisoblash
    timerElement.textContent =
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // Agar vaqt tugagan bo'lsa
    if (time === 0) {
        clearInterval(timerInterval); // Taymerni to'xtatish
        timerElement.textContent = "Vaqt tugadi!";
        resendButton.style.display = "block"; // Havolani ko‘rsatish
    }

    time--;
}

// Taymerni boshlash funksiyasi
function startTimer() {
    clearInterval(timerInterval); // Eski intervalni to‘xtatish
    time = 60; // Vaqtni qayta sozlash
    resendButton.style.display = "none"; // Havolani yashirish
    timerInterval = setInterval(updateTimer, 1000); // Yangi intervalni boshlash
    updateTimer(); // Taymerni bir marta darhol yangilash
}

// Dastlab taymerni ishga tushirish
startTimer();

// "Qayta kod yuborish" havolasi bosilganda hodisa
resendButton.addEventListener('click', (event) => {
    event.preventDefault(); // Havola standart harakatini bloklash
    resendButton.textContent = "Qayta kode yuborildi"; // Matnni o‘zgartirish
    startTimer(); // Taymerni qayta boshlash
});

// ==============================================================


