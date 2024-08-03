<template>
    <div>
      <h1>気になるレビューを選んでね</h1>
      <div v-for="(review, index) in recommended_reviews" :key="index">
        <p>{{ review.review_text }}</p>
        <router-link :to="{ name: 'PresentationPage', params: { book_id: review.book_id } }">これにする</router-link>
      </div>

      <div v-if="recommended_reviews.length === 0">
        <p>Loading...</p>
      </div>
    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    name: 'ResultPage',
    data() {
      return {
        // review: null,
        recommended_reviews: [],
        showDetail: false
      };
    },
    async created() {
      const { request_id } = this.$route.params;
      try {
        const response = await axios.post('http://localhost:5001/calculate_similarity', {
          request_id
        });
        // this.review = response.data.review;
        this.recommended_reviews = response.data.recommended_reviews;
      } catch (error) {
        console.error('Error fetching result:', error);
      }
    },
    methods: {
      showDetails() {
        this.showDetail = true;
      },
    }
  };
  </script>

  <style>
  /* Add any basic styling here */
  </style>
