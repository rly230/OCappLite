<template>
  <div class="container">
    <div class="results-container">
      <div class="search-results">
        <OverlayLogo @click="reloadPage"/>
        <ul>
          <li v-for="book in books" :key="book.book_id" class="book-item">
            <router-link :to="{ name: 'PresentationPage', params: { book_id: book.book_id } }">{{ book.title }}</router-link>
          </li>
        </ul>
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">前のページ</button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">次のページ</button>
        </div>
      </div>
      <div class="god-section">
        <img class="god-image" src="@/assets/god.png" alt="神様">
        <div class="dialogue-box">
          <div class="name-box">神様</div>
          <p class="dialogue-text">この中にある？</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import OverlayLogo from '@/components/OverlayLogo.vue';
import axios from 'axios';

export default {
  name: 'BookListPage',
  components: {
    OverlayLogo
  },
  data() {
    return {
      books: [],
      currentPage: 1,
      totalPages: 1,
      request_id: null
    };
  },
  watch: {
    '$route.query.title': 'fetchBooks'
  },
  async created() {
    await this.fetchBooks();
  },
  methods: {
    reloadPage() {
      window.location.reload();
    },
    async fetchBooks() {
      const title = this.$route.query.title;
      if (!title) {
        this.$router.push({ name: 'NoResultsPage', query: { message: 'タイトルが必要です。' } });
        return;
      }

      try {
        const response = await axios.post('http://localhost:5001/search_books', {
          title: title,
          page: this.currentPage
        });
        if (!response.data.books.length) {
          this.$router.push({ name: 'NoResultsPage', query: { message: '検索結果なし' } });
          return;
        }
        this.books = response.data.books;
        this.totalPages = response.data.totalPages || 1;
        this.request_id = response.data.request_id;
      } catch (error) {
        console.error('Error fetching books:', error);
        this.$router.push({ name: 'NoResultsPage', query: { message: 'エラーが発生しました。' } });
      }
    },
    async nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        await this.fetchBooks();
      }
    },
    async prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        await this.fetchBooks();
      }
    }
  }
};
</script>

<style scoped>
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 15px;
}

.results-container {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.search-results {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.god-section {
  position: relative;
  width: 30%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}

.god-image {
  position: absolute;
  width: 100%;
  bottom: 0;
  height: auto;
}

.dialogue-box {
  position: relative;
  width: 100%;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px;
  bottom: 25vh;
}

.name-box {
  font-weight: bold;
  margin-bottom: 10px;
}

.book-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
  list-style-type: none;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  padding: 10px;
  margin: 0 10px;
}
</style>
