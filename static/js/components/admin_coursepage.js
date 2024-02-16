import admin_navbar from "./admin_navbar.js";

const admin_coursepage = {
  template: `
    <div>
        <admin_navbar />
        <div class="admincourse-container">
        <!-- Machine Learning Container -->
        <div class="admincourse-card admincourse-left">
          <div class="admincourse-card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <h1>{{ title }}</h1>
            <router-link :to="'/admin_editcoursepage/'+title"><button class="admincourse-edit">Edit</button></router-link>
          </div>
          <div class="admincourse-card-body">
            <p>{{ paragraph }}</p>
          </div>
        </div>
      
        <!-- Right Column -->
        <div class="admincourse-right-column">
          <!-- Similar Courses Container -->
          <div class="admincourse-card">
            <div class="admincourse-card-header">
              <h2>Feedbacks</h2>
            </div>
            <div class="admincourse-card-body">
            <button v-for="(course, index) in feedbacks.slice(0, 4)" :key="index" class="admincourse-course-btn">{{ course.feedback }}</button>
            <a href="#"><input type="submit" value="See More" class="admincourse-input" @click="sendfeedback"></a>
          </div>
          </div>
      
          <!-- Subject Statistics Container -->
          <div class="admincourse-card">
            <div class="admincourse-card-header">
              <h2>Subject Statistics</h2>
            </div>
            <div class="admincourse-card-body">
            <ul>
              <li>Fees: {{ subjectStatistics.fees }}</li>
              <li>Enrollments: {{ subjectStatistics.enrollments }}</li>
              <li>Toughness: {{ subjectStatistics.toughness }}</li>
              <li>Teacher: {{ subjectStatistics.teacher }}</li>
            </ul>
            </div>
          </div>
        </div>
      </div>      
      </div>
    `,
  components: { admin_navbar: admin_navbar },
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
      feedbacks: [],
    };
  },
  mounted() {
    this.title = this.$route.params.course;
    this.paragraph = this.Content[this.title];
    this.getSubjectStatistics();
    this.getfeedback();
  },
  methods: {
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
    sendfeedback() {
      fetch(`/sendfeedback/${this.title}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else if (response.status == 500 || response.status == 404) {
            throw new Error("Feedback not available");
          }
        })
        .then((data) => {
          alert("Feedback sent successfully! Please check your email.");
        })
        .catch((error) => {
          alert(error.message);
        });
    },
    getfeedback() {
      fetch(`/api/feedback/${this.title}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else if (response.status == 500 || response.status == 400) {
            throw new Error("Feedback not available");
          }
        })
        .then((data) => {
          this.feedbacks = data;
          console.log(data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};

export default admin_coursepage;
