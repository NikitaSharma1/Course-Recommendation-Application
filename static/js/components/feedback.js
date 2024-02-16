import navbar from "./navbar.js";

const feedback = {
  template: `
      <div>
        <navbar />
        <div class="alert alert-success" v-if="showmessage">
                    <p>{{ showmessage }}</p>
        </div>
        <div class="alert alert-danger" v-if="errormessage">
                    <p>{{ errormessage }}</p>
        </div>
        <form @submit.prevent="submitFeedback" class="fb-feedback-form">
        <h2 class="fb-title">Feedback Form: {{ subject }}</h2>
        <div class="fb-form-columns">
          <div class="fb-form-column">
            <label for="teacher" class="fb-label">Instructor:</label>
            <input type="text" v-model="feedback.teacher" class="fb-input" required>

            <label for="assignments" class="fb-label">Assignments:</label>
            <input type="text" v-model="feedback.assignment" class="fb-input" required>

            <label for="exams" class="fb-label">Exams:</label>
            <input type="text" v-model="feedback.exams" class="fb-input" required>

            <label for="content" class="fb-label">Content:</label>
            <input type="text" v-model="feedback.content" class="fb-input" required>
          </div>

          <div class="fb-form-column">
            <label for="support" class="fb-label">Support:</label>
            <input type="text" v-model="feedback.support" class="fb-input" required>

            <label for="toughness" class="fb-label">Toughness (1-10):</label>
            <input type="number" v-model="feedback.toughness" class="fb-input" min="1" max="10" required>

            <label for="overall" class="fb-label">Overall:</label>
            <input type="text" v-model="feedback.overall" class="fb-input" required>

            <label for="grade" class="fb-label">Your Grade (Optional):</label>
            <input type="text" v-model="feedback.grade" class="fb-input">
          </div>
        </div>

        <label for="comments" class="fb-label">Any other Comments?</label>
        <textarea v-model="feedback.comments" class="fb-textarea"></textarea>
        <div>
          <button type="button" class="fb-cancel-btn" @click="cancelFeedback">Cancel</button>
          <input type="submit" value="Submit" class="fb-submit-btn">
        </div>
      </form>
      </div>
    `,
  components: { navbar: navbar },
  data() {
    return {
      showmessage: "",
      errormessage: "",
      feedback: {
        teacher: "",
        assignment: "",
        exams: "",
        content: "",
        support: "",
        toughness: 1,
        overall: "",
        grade: "",
        comments: "",
        subject: this.$route.params.course_name,
      },
    };
  },
  created() {
    // Implement your created logic here
    this.feedback.subject = this.$route.params.course_name;
    this.subject = this.$route.params.course_name;
  },
  methods: {
    submitFeedback() {
      console.log(this.feedback);
      // Implement your feedback submission logic here
      const token = localStorage.getItem("auth_token");
      fetch("/api/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": token,
        },
        body: JSON.stringify(this.feedback),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else if (response.status == 500 || response.status == 400) {
            throw new Error("Feedback not sent");
          }
        })
        .then((data) => {
          this.showmessage = data.message;
          setTimeout(() => {
            this.showmessage = "";
            this.$router.push({
              name: "coursepage",
              params: { course: this.feedback.subject },
            });
          }, 5000);
        })
        .catch((error) => {
          this.errormessage = error.message;
        });
    },
    cancelFeedback() {
      this.$router.push({
        name: "coursepage",
        params: { course: this.feedback.subject },
      });
    },
  },
};

export default feedback;
