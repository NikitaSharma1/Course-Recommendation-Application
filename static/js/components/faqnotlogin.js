const faqnl = {
  template: `
      <div class = "faq-con">
        <nav class=" navbar navbar-expand-lg navbar-dark">
        <router-link to="/login" class="navbar-brand">Course Recommendation</router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                <router-link to="/faqnl" class="login-nav-link nav-link">FAQs</router-link>
            </li>
            <li class="nav-item">
                <router-link to="/contactnl" class="login-nav-link nav-link">Contact Us</router-link>
            </li>
            </ul>
        </div>
        </nav>
        <main class="faq-main">
          <h2 class="faq-h2">Frequently Asked Questions</h2>
          <details v-for="(faqItem, index) in faqItems" :key="index" :open="faqItem.open">
            <summary @click="toggleDetails(index)" class="faq-summary">{{ faqItem.question }}</summary>
            <div class="faq__content">
              <p>{{ faqItem.answer }}</p>
            </div>
          </details>
        </main>
      </div>
    `,

  data() {
    return {
      faqItems: [
        {
          question: "How I solve this issue?",
          answer:
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dolor suscipit, iure tenetur eveniet, vero tempore delectus? Perferendis, quisquam ullam consequuntur?",
          open: true,
        },
        {
          question: "How to input your data on this board?",
          answer:
            "Fugiat quo voluptas nulla pariatur? Et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque. Accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo.",
          open: false,
        },
        // Add more FAQ items as needed
      ],
    };
  },
  methods: {
    toggleDetails(index) {
      this.faqItems[index].open = !this.faqItems[index].open;
    },
  },
};

export default faqnl;
