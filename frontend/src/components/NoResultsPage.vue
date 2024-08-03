<template>
    <div>
      <h1>失敗！</h1>
        <p>{{ message }}</p>
        <button @click="goToMainPage">最初から</button>
    </div>
  </template>

  <script>

  export default {
    name: 'NoResultsPage',
    data() {
      return {
        message: this.$route.query.message || '予期しないエラーが発生しました。'
      };
    },
    methods: {
      goToMainPage() {
        this.$router.push({ path: '/' });
      }
    }
  };
  </script>

  <style>
  /* Add any basic styling here */
  </style>
