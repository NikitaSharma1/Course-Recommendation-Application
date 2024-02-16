import navbar from "./navbar.js";

const faq = {
  template: `
      <div class = "faq-con">
        <navbar />
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
  components: { navbar: navbar },
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

export default faq;
