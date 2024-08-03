<template>
    <div>
      <h1>気に入ったレビューを選んでね</h1>
      <div v-if="reviews.length">
        <div v-for="(review, reviewIndex) in reviews" :key="reviewIndex">
          <h2></h2>
          <div v-for="(sentence, index) in review.review_texts" :key="index">
            <input type="checkbox" :id="'checkbox-' + index" v-model="selectedSentences" :value="sentence">
            <label :for="'checkbox-' + index">{{ sentence }}</label>
          </div>
        </div>
        <button @click="submitEvaluation">確定</button>
      </div>
      <div v-else>
        <p>ちょっと待ってね</p>
        <button @click="submitEvaluation">次に進む</button>
      </div>
    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    name: 'ReviewEvaluationPage',
    data() {
      return {
        reviews: [],
        selectedSentences: [],
        num_fetch: 1
      };
    },
    async created() {
      await this.fetchReviews();
    },
    methods: {
        async fetchReviews() {
            const { book_id, request_id } = this.$route.params;
            try {
                const response = await axios.post('http://localhost:5001/submit_evaluation', {
                    book_id,
                    request_id,
                });
                this.reviews = response.data.reviews;
            } catch (error) {
                console.error('Error fetching reviews:', error.response ? error.response.data : error.message);
            }
        },
      async submitEvaluation() {
        const { book_id, request_id } = this.$route.params;
        const selected_texts = this.selectedSentences;
        const non_selected_texts = this.reviews.flatMap(review => review.review_texts).filter(sentence => !selected_texts.includes(sentence));

        try {
          const response = await axios.post('http://localhost:5001/submit_evaluation', {
            book_id,
            request_id,
            selected_texts,
            non_selected_texts,
            num_fetch: this.num_fetch
          });
          if (response.data.status === 'success') {
            this.$router.push({ name: 'ResultPage', params: { request_id } });
          } else if (this.reviews.length){
            this.reviews = response.data.reviews;
            this.selectedSentences = []
            this.num_fetch++
          } else if (response.data.message === 'reviews not found') {
            this.$router.push({ name: 'BookListPage', query: { title: this.title } });
          }
          else{
            this.$router.push({ name: 'ResultPage', params: { request_id } });
          }
        } catch (error) {
          console.error('Error submitting evaluation:', error);
        }
      }
    }
  };
  </script>

  <style>
  /* Add any basic styling here */
  </style>
