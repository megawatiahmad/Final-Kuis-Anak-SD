import streamlit as st
from PIL import Image
import os
import streamlit.components.v1 as components

# Setel halaman
st.set_page_config(page_title="Petualangan Belajar - Kuis Seru!", layout="centered")

# Tambahkan efek suara
sound_html = """
<audio id='clickSound' src='https://www.soundjay.com/buttons/sounds/button-29.mp3' preload='auto'></audio>
<script>
function playClick() {
  var audio = document.getElementById('clickSound');
  if (audio) audio.play();
}
document.querySelectorAll("button").forEach(btn => btn.addEventListener("click", playClick));
</script>
"""
components.html(sound_html, height=0)

# Inisialisasi state
if "name" not in st.session_state:
    st.session_state.name = ""
    st.session_state.level = 1
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.answered = False

# Soal per level
quiz_data = {
    1: [
        {"q": "Apa warna bendera Indonesia?", "options": ["Merah Putih", "Hijau Kuning", "Biru Merah", "Putih Hitam"], "ans": 0},
        {"q": "1 + 1 = ?", "options": ["1", "2", "3", "4"], "ans": 1},
        {"q": "Binatang yang bisa terbang?", "options": ["Ikan", "Gajah", "Burung", "Kucing"], "ans": 2},
        {"q": "Huruf pertama alfabet?", "options": ["Z", "A", "K", "O"], "ans": 1},
        {"q": "Minuman sehat dari sapi?", "options": ["Susu", "Jus", "Teh", "Soda"], "ans": 0},
    ],
    2: [
        {"q": "Ibukota Indonesia?", "options": ["Bandung", "Surabaya", "Jakarta", "Medan"], "ans": 2},
        {"q": "Hari Kemerdekaan Indonesia?", "options": ["17 Agustus", "1 Januari", "20 Mei", "10 November"], "ans": 0},
        {"q": "Hewan yang hidup di air?", "options": ["Ikan", "Burung", "Ayam", "Sapi"], "ans": 0},
        {"q": "Bahasa resmi Indonesia?", "options": ["Sunda", "Minang", "Indonesia", "Jawa"], "ans": 2},
        {"q": "Lambang negara kita?", "options": ["Garuda", "Singa", "Harimau", "Elang"], "ans": 0},
    ],
    3: [
        {"q": "2 x 3 = ?", "options": ["5", "6", "7", "8"], "ans": 1},
        {"q": "Hewan berkaki 8?", "options": ["Kucing", "Laba-laba", "Ayam", "Ikan"], "ans": 1},
        {"q": "Planet tempat kita tinggal?", "options": ["Mars", "Venus", "Bumi", "Saturnus"], "ans": 2},
        {"q": "Sayur berwarna oranye?", "options": ["Bayam", "Wortel", "Tomat", "Jagung"], "ans": 1},
        {"q": "Berapa huruf dalam kata 'sekolah'?", "options": ["5", "6", "7", "8"], "ans": 2},
    ],
    4: [
        {"q": "Hari setelah Senin?", "options": ["Minggu", "Selasa", "Rabu", "Kamis"], "ans": 1},
        {"q": "Alat untuk menulis?", "options": ["Penggaris", "Pensil", "Spidol", "Kapur"], "ans": 1},
        {"q": "Hewan penghasil telur?", "options": ["Ayam", "Sapi", "Kucing", "Ular"], "ans": 0},
        {"q": "Buah berwarna kuning?", "options": ["Apel", "Jeruk", "Pisang", "Mangga"], "ans": 2},
        {"q": "Bilangan genap di bawah 5?", "options": ["1", "2", "3", "5"], "ans": 1},
    ],
    5: [
        {"q": "Alat untuk makan?", "options": ["Pisau", "Sendok", "Talenan", "Wajan"], "ans": 1},
        {"q": "Bentuk matahari?", "options": ["Segitiga", "Persegi", "Lingkaran", "Trapesium"], "ans": 2},
        {"q": "Benda yang bisa mengapung?", "options": ["Kayu", "Batu", "Besi", "Kaca"], "ans": 0},
        {"q": "Warna campuran merah dan biru?", "options": ["Ungu", "Hijau", "Coklat", "Pink"], "ans": 0},
        {"q": "Tempat tidur disebut?", "options": ["Kursi", "Kasur", "Meja", "Lemari"], "ans": 1},
    ],
}

def reset_quiz():
    st.session_state.level = 1
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.answered = False

# Tampilan awal
if not st.session_state.name:
    st.image("static/assets/character_start.jpg", width=150)
    st.title("Petualangan Belajar - Kuis Seru!")
    name = st.text_input("Halo! Siapa namamu?")
    if st.button("Mulai Petualangan!") and name.strip():
        st.session_state.name = name
        st.experimental_rerun()

elif st.session_state.finished:
    st.image("static/assets/character_end.jpg", width=150)
    st.header(f"Selamat, {st.session_state.name}!")
    st.subheader(f"Skormu: {st.session_state.score} dari 25")

    if st.session_state.score >= 22:
        st.success("Luar biasa! Kamu sangat pintar!")
    elif st.session_state.score >= 18:
        st.info("Bagus sekali! Terus semangat belajar!")
    elif st.session_state.score >= 12:
        st.warning("Cukup baik, tapi bisa lebih baik lagi!")
    else:
        st.error("Jangan menyerah, coba lagi ya!")

    st.markdown("---")
    st.markdown("### 💪 Kamu pasti bisa!")

    if st.button("Mulai Ulang"):
        st.session_state.name = ""
        reset_quiz()
        st.experimental_rerun()

else:
    level = st.session_state.level
    idx = st.session_state.question_index
    st.markdown(f"### Level {level} - Soal {idx+1} dari {len(quiz_data[level])}")

    qdata = quiz_data[level][idx]
    st.write(qdata["q"])

    if not st.session_state.answered:
        for i, opt in enumerate(qdata["options"]):
            if st.button(opt, key=f"{level}-{idx}-{i}"):
                st.session_state.answered = True
                if i == qdata["ans"]:
                    st.success("Jawaban benar! 🎉")
                    st.session_state.score += 1
                else:
                    st.error(f"Salah! Jawaban benar adalah: {qdata['options'][qdata['ans']]}")

    if st.session_state.answered:
        if st.button("Next ➡️"):
            st.session_state.answered = False
            if idx + 1 >= len(quiz_data[level]):
                if level >= 5:
                    st.session_state.finished = True
                else:
                    st.session_state.level += 1
                    st.session_state.question_index = 0
            else:
                st.session_state.question_index += 1
            st.experimental_rerun()

    st.markdown("\n---\n")
    st.markdown("### 💪 Kamu pasti bisa! Tetap semangat menjawab ya!")
