<template>
  <div class="container">
    <div class="main-page">
      <OverlayLogo @click="reloadPage" />
      <div v-if="showOverlay" class="overlay" @click="nextLine" ></div>
      <div v-if="showDialogue" class="dialogue-box">
        <img class="background-image" src="@/assets/background_god.png" alt="背景" />
        <img class="god-image" v-if="!isDialogueComplete" :class="{ fadeIn: showGodImage }" src="@/assets/god.png" alt="神様" @load="onGodImageLoad" />
        <div v-if="showDialogueBox" class="text-box">
          <div class="name-box">{{ currentSpeaker }}</div>
          <p class="dialogue-text">{{ currentText }}</p>
        </div>
      </div>
      <div v-else class="input-container">
        <img class="god-image-stand-by" src="@/assets/god.png" alt="神様" />
        <div class="text-box">
          <div class="name-box">マスダ教授（本の神）</div>
          <p class="dialogue-text">どうだったかな？読みたくなったかどうかを教えてね</p>
        </div>
        <div class="rating">
          <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= rating }" @click="setRating(star)">&#9733;</span>
        </div>
        <button @click="submitRating" :disabled="!isRateValid">確定</button>
      </div>
    </div>
  </div>
</template>

<script>
import OverlayLogo from '@/components/OverlayLogo.vue';
import axios from 'axios';

export default {
  name: 'PresentationPage',
  components: {
    OverlayLogo,
  },
  data() {
    return {
      dialogue: [{ speaker: '考え中', line: '少々お待ちください...' }],
      rating: 0,
      currentLineIndex: 0,
      showDialogue: true,
      showGodImage: false,
      showDialogueBox: false,
      showOverlay: false,
      currentText: '少々お待ちください...',
      isAnimating: false,
      isAcceptAIAnswer: false,
      isDialogueComplete: false, // 全てのダイアログが表示されたかどうかを判定するフラグ
    };
  },
  async created() {
    const { book_id } = this.$route.params;
    try {
      const response = await axios.post('http://localhost:5001/summarize', {
        book_id,
      });

      if (response.data.message === 'no reviews') {
        this.$router.push({ name: 'NoResultsPage', query: { message: `${response.data.title}は まだ教えられるほどは知らないんだ。ごめんね。` } });
      } else {
        this.dialogue.push({speaker: '本の神', line: `${response.data.title}という${response.data.book_category}はどうかな。`})
        const newDialogues = response.data.ai_answers.map((answer) => ({
        line: answer,
        speaker: '本の神',
      }));
      this.dialogue.push(...newDialogues);
      if (this.dialogue.length > 0) {
        this.currentText = this.dialogue[this.currentLineIndex].line;
        this.showOverlay = true;
      }
      }
    } catch (error) {
      console.error('Error fetching result:', error);
    }
  },
  watch: {
    currentLine(newLine) {
      this.displayLine(newLine);
    },
  },
  methods: {
    setRating(star) {
      this.rating = star;
    },
    reloadPage() {
      window.location.reload();
    },
    async submitRating() {
      if (this.isRateValid) {
        try {
          const response = await axios.post('http://localhost:5001/submit_rating', {
            ai_answer: this.dialogue.map((d) => d.line).join(' '),
            rating: this.rating,
          });
          if (response.data.status === 'success') {
            this.$router.push({ path: '/' });
          }
        } catch (error) {
          console.error('Error submitting rating:', error);
        }
      }
    },
    async displayLine(line) {
      this.isAnimating = true;
      this.currentText = '';
      for (let i = 0; i < line.length; i++) {
        if (!this.isAnimating) {
          this.currentText = line;
          return;
        }
        this.currentText += line[i];
        await this.sleep(80);
      }
      this.isAnimating = false;
    },
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    nextLine() {
      if (this.isAnimating) {
        this.isAnimating = false;
        this.currentText = this.currentLine;
      } else if (this.currentLineIndex < this.dialogue.length - 1) {
        this.currentLineIndex++;
      } else {
        this.isDialogueComplete = true; // 全てのダイアログが表示されたフラグを立てる
        this.showDialogue = false;
      }
    },
    onGodImageLoad() {
      setTimeout(() => {
        this.showGodImage = true;
        setTimeout(() => {
          this.showDialogueBox = true;
          this.displayLine(this.currentLine); // テキストアニメーションを開始
        }, 4500); // ダイアログボックス表示の遅延
      }, 2000); // 神様画像表示の遅延
    },
  },
  computed: {
    currentLine() {
      return this.dialogue[this.currentLineIndex].line;
    },
    currentSpeaker() {
      return this.dialogue[this.currentLineIndex].speaker;
    },
    isLastLine() {
      return this.currentLineIndex === this.dialogue.length - 1;
    },
    isRateValid() {
      return this.rating > 0;
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.main-page {
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  background-color: #ffffff;
  overflow: hidden; /* スクロールを防止 */
}

.dialogue-box {
  position: relative;
  width: 100%;
  text-align: center;
  color: white;
  padding: 20px;
  z-index: 10;
}

.god-image {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: auto;
  height: calc(100vh - 10vh); /* 画面サイズ一割の隙間を開ける */
  z-index: 11;
  opacity: 0;
  transition: opacity 2s ease-in-out;
}

.god-image.fadeIn {
  opacity: 1;
}

.background-image {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: auto;
  height: 100vh;
  z-index: 9;
  opacity: 1;
  animation: rotate 200s linear infinite;
}

@keyframes rotate {
  from {
    transform: translateX(-50%) rotate(0deg);
  }
  to {
    transform: translateX(-50%) rotate(360deg);
  }
}

.god-image-stand-by {
  position: absolute;
  opacity: 0.5;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: auto;
  height: calc(100vh - 10vh); /* 画面サイズ一割の隙間を開ける */
  z-index: 11;
}

.text-box {
  position: relative;
  width: 80%;
  margin: 0 auto;
  padding: 10px;
  border: 2px solid #ffffff;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 12;
  margin-top: 20px;
  text-align: left;
}

.dialogue-text {
  width: 100%;
  font-size: 1.2em;
  color: #ffffff;
}

.name-box {
  position: absolute;
  top: -45px;
  left: 0;
  padding: 5px 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: #ffffff;
  border: 2px solid #ffffff;
  font-size: 1.2em;
  font-weight: bold;
  z-index: 12;
}

.rating {
  display: flex;
  z-index: 1000;
}

.star {
  font-size: 2em;
  cursor: pointer;
  color: #ccc;
  pointer-events: auto;
}

.star.filled {
  color: #f5b301;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0);
  z-index: 13;
}

.input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 100%;
  height: 100%;
}

button {
  position: relative;
  padding: 10px 20px;
  margin-top: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  z-index: 14;
}

button:disabled {
  background-color: #a6a6a6;
  cursor: not-allowed;
}

/* PC用のスタイル */
@media (min-width: 768px) {
  .dialogue-box {
    height: 33.33vh; /* 画面下1/3 */
  }
  .input-container {
    justify-content: center; /* 画面中央 */
  }
}

/* スマートフォン用のスタイル */
@media (max-width: 767px) {
  .dialogue-box {
    height: 40vh; /* 画面下2/5 */
  }
  .input-container {
    justify-content: flex-end; /* 画面下 */
  }
}
</style>
