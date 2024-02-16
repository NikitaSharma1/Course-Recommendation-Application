import navbar from "./navbar.js";

const coursepage = {
  template: `
    <div>
    <navbar />
    <div class="cp-container">
      <!-- Machine Learning Container -->
      <div class="cp-card cp-card-left">
        <div class="cp-card-header">
          <h3>{{ title }}</h3>
        </div>
        <div class="cp-card-body">
          <p>{{ paragraph }}</p>
        </div>
      </div>

      <!-- Right Column -->
      <div class="cp-right-column">
        <!-- Similar Courses Container -->
        <div class="cp-card">
          <div class="cp-card-header">
            <h3>Similar Courses</h3>
          </div>
          <div class="cp-card-body">
            <button v-for="course in similarCourses" :key="course" class="cp-course-btn" @click="gocoursepage(course)">{{ course }}</button>
          </div>
        </div>

        <!-- Subject Statistics Container -->
        <div class="cp-card">
          <div class="cp-card-header">
            <h3>Subject Statistics</h3>
          </div>
          <div class="cp-card-body">
          <ul>
            <li>Fees: {{ subjectStatistics.fees }}</li>
            <li>Enrollments: {{ subjectStatistics.enrollments }}</li>
            <li>Toughness: {{ subjectStatistics.toughness }}</li>
            <li>Teacher: {{ subjectStatistics.teacher }}</li>
          </ul>
            <button type="submit" class="cp-query-submit" @click="feedbackpage">Give Feedback</button>
            
          </div>
        </div>

        <!-- Queries Form Container -->
        <div class="cp-card">
          <form @submit.prevent="submitQuery">
            <input type="text" name="query" v-model="query" placeholder="Enter your query and press enter to send" class="cp-query-input">
            <input type="submit" value="Send" class="cp-query-submit">
          </form>
        </div>
      </div>
    </div>
  </div>
`,
  components: { navbar: navbar },
  data() {
    return {
      Content: {
        Java: "This course uses Java to provide an understanding of core ideas in object oriented programming, exception handling, event driven programming, concurrent programming and functional programming.",
        "MAD I":
          "Building a modern application involves many different aspects: front end, recording transactions, storage, connecting to a remote server, using APIs etc. The courses Modern Application Development I and II go through all these aspects through a detailed and evolving case study, teaching the relevant programming skills as the course progresses.",
        "MAD II":
          "Building a modern application involves many different aspects: front end, recording transactions, storage, connecting to a remote server, using APIs etc. The courses Modern Application Development I and II go through all these aspects through a detailed and evolving case study, teaching the relevant programming skills as the course progresses.",
        "System Commands":
          "This course introduces students to the fundamentals of mobile application development using the Android platform. Students will learn to design and develop mobile applications using Android and Java. Topics include user interfaces, data storage, networking, and mobile design patterns.",
        DBMS: "A comprehensive introduction to databases, database management, and relevant topics like database security, integrity, concurrency, and data warehousing.",
        PDSA: "A good foundation course to introduce basic concepts in the design and analysis of algorithms as well as standard data structures, using Python as a base language for implementing these.",
        MLF: "This course lays the groundwork for the upcoming ML courses by covering various fundamentals that do not necessarily fall under Machine Learning but are quite necessary for a comprehensive understanding of Machine Learning.",
        MLT: "To introduce the main methods and models used in machine learning problems of regression, classification and clustering. To study the properties of these models and methods and learn about their suitability for different problems.",
        MLP: "This companion course to the ML Theory course introduces the student to scikit-learn, a popular Python machine learning module, to provide hands-on problem solving experience for all the methods and models learnt in the Theory course.",
        BDM: "A significant source of data sets and problems for data scientists will come from the business domain. This course provides a basic understanding of how businesses are organised and run from a data perspective.",
        BA: "The problems faced by decision makers in today's business environments are extremely complex. Hence, the task of making good decisions is not easy. The answer is in building quantitative models, and this course is designed to help you understand the fundamentals of this critical, foundational, business skill. The business application of statistical methods is the core focus of this course. In that sense, the course builds on the core course in the first year of the program. That basic course focused on the preliminaries of the area. This course highlights a business application and then demonstates an application of a statistical techique to solve that scenario and arrive at the best decisions and insights.",
        TDS: "This course will teach students to use popular tools for sourcing data, transforming it, building and optimizing models, communicating these as visual stories, and deploying them in production.",
      },
      title: "",
      paragraph: "",
      subjectStatistics: {},
      similarCourses: [],
      query: "",
      name: "",
      email: "",
    };
  },
  mounted() {
    this.getSubjectStatistics();
  },
  methods: {
    gocoursepage(course_name) {
      this.$router.push({
        name: "coursepage",
        params: { course: course_name },
      });
      location.reload();
    },
    getSubjectStatistics() {
      fetch(`/satistics/${this.title}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.subjectStatistics = data;
        });
    },
    feedbackpage() {
      this.$router.push({
        name: "feedback",
        params: { course_name: this.title },
      });
    },
    submitQuery() {
      // Add your logic for handling query submission here
      fetch("/email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: this.name,
          email: this.email,
          message: this.query,
        }),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else if (response.status == 500) {
            throw new Error("Querry not sent");
          }
        })
        .then((data) => {
          this.name = "";
          this.email = "";
          this.query = "";
          alert(data.message);
        })
        .catch((error) => {
          alert(error.message);
        });
    },
  },
  created() {
    this.title = this.$route.params.course;
    this.paragraph = this.Content[this.title];
    fetch(`/similarcourses/${this.title}`)
      .then((response) => response.json())
      .then((data) => {
        this.similarCourses = data.map((course) => course.course_name);
      })
      .catch((error) => console.error("Error:", error));
  },
};

export default coursepage;
