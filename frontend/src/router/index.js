import BookListPage from '@/components/BookListPage.vue';
import MainPage from '@/components/MainPage.vue';
import NoResultsPage from '@/components/NoResultsPage.vue';
import PresentationPage from '@/components/PresentationPage.vue';
import ResultPage from '@/components/ResultPage.vue';
import ReviewEvaluationPage from '@/components/ReviewEvaluationPage.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    { path: '/', component: MainPage },
    { path: '/books', name: 'BookListPage', component: BookListPage },
    { path: '/result/:request_id', name: 'ResultPage', component: ResultPage },
    { path: '/evaluate/:book_id/:request_id', name: 'ReviewEvaluationPage', component: ReviewEvaluationPage },
    { path: '/presentation/:book_id', name: 'PresentationPage', component: PresentationPage },
    { path: '/noData', name: 'NoResultsPage', component: NoResultsPage },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;




