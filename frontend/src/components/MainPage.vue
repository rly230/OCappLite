<template>
  <div class="container">
    <div class="main-page">
      <OverlayLogo @click="reloadPage"/>
      <button v-if="showDialogue" class="skip-button" @click="skipDialogue">説明をスキップ</button>
      <div v-if="showOverlay" class="overlay" @click="nextLine"></div>
      <div v-if="showDialogue" class="dialogue-box">
        <img class="background-image" src="@/assets/background_god.png" alt="背景">
        <img class="god-image" :class="{ fadeIn: showGodImage }" src="@/assets/god.png" alt="神様" @load="onGodImageLoad">
        <div v-if="showDialogueBox" class="text-box">
          <div class="name-box">{{ currentSpeaker }}</div>
          <p class="dialogue-text">{{ currentText }}</p>
        </div>
      </div>
      <div v-else class="input-container">
        <img class="god-image-stand-by" src="@/assets/god.png" alt="神様">
        <input v-model="title" type="text" placeholder="書籍タイトルを入力" required autofocus>
        <form action="javascript:0" method="GET">
          <button @click="searchBooks" :disabled="!isTitleValid" type="submit">検索</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import OverlayLogo from '@/components/OverlayLogo.vue';

export default {
  name: 'MainPage',
  components: {
    OverlayLogo
  },
  data() {
    return {
      title: '',
      dialogue: [
        { line: "東京電機大学のオープンキャンパスへようこそ。", speaker: "？？？" },
        { line: "私は本の神。", speaker: "？？？" },
        { line: "私はこの世にある数多の娯楽書籍について知っているんだ。", speaker: "本の神" },
        { line: "気になっている本があれば私に尋ねるといい。", speaker: "本の神" },
        { line: "最高のプレゼンになると約束しよう。", speaker: "本の神" },
      ],
      currentLineIndex: 0,
      showDialogue: true,
      showGodImage: false,
      showDialogueBox: false,
      showOverlay: false,
      currentText: '',
      isAnimating: false,
    };
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
    isTitleValid() {
      return this.title.trim() !== '';
    }
  },
  watch: {
    currentLine(newLine) {
      this.displayLine(newLine);
    }
  },
  methods: {
    reloadPage() {
      window.location.reload();
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
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    nextLine() {
      if (this.isAnimating) {
        this.isAnimating = false;
        this.currentText = this.currentLine;
      } else if (this.currentLineIndex < this.dialogue.length - 1) {
        this.currentLineIndex++;
      } else {
        this.showDialogue = false;
      }
    },
    skipDialogue() {
      this.showDialogue = false;
    },
    searchBooks() {
      if (this.isTitleValid) {
        this.$router.push({ name: 'BookListPage', query: { title: this.title } });
      }
    },
    onGodImageLoad() {
      setTimeout(() => {
        this.showGodImage = true;
        setTimeout(() => {
          this.showDialogueBox = true;
          this.showOverlay = true;
          this.displayLine(this.currentLine); // テキストアニメーションを開始
        }, 4500); // ダイアログボックス表示の遅延
      }, 2000); // 神様画像表示の遅延
    }
  },
  mounted() {
    // テキストアニメーションは神様画像表示とダイアログボックス表示の後に開始されるので、ここでの呼び出しは不要
  }
}
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
  transition: opacity 5s ease-in-out;
}

.god-image.fadeIn {
  opacity: 1;
}

.background-image{
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
}

.name-box {
  position: absolute;
  top: -45px;
  left: 0;
  padding: 5px 10px;
  background-color: rgba(0, 0, 0, 0.7);
  border: 2px solid #ffffff;
  font-size: 1.2em;
  font-weight: bold;
  z-index: 12;
}

.skip-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  color: rgb(0, 0, 0, 0.5);
  border: 2px solid rgb(0, 0, 0, 0.5);
  padding: 10px 20px;
  cursor: pointer;
  z-index: 14;
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

input {
  margin-top: 20px;
  padding: 10px;
  width: 60%;
  border: 1px solid #ccc;
  border-radius: 4px;
  z-index: 14;
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
    height: 25vh; /* 画面下1/5 */
  }
  .input-container {
    justify-content: flex-end; /* 画面下1/3 */
    padding-bottom: 33.33vh; /* 画面下1/3 */
  }
}
</style>
