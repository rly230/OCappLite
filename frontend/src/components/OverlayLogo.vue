<template>
  <div class="container">
    <img class="overlay-logo" src="@/assets/logo.png" @click="goToMainPage" alt="Logo">
  </div>
</template>

  <script>
  export default {
    name: 'OverlayLogo',
    methods: {
      goToMainPage() {
        this.$router.push({ path: '/' });
      }
    }
  }
  </script>

  <style scoped>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
  }
  .overlay-logo {
    position: absolute;
    top: 30px;
    left: 30px;
    height: 60px;
    cursor: pointer;
    z-index: 1000;
  }
  </style>
