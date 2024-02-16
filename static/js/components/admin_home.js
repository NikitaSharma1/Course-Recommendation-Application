import admin_navbar from "./admin_navbar.js";

const admin_home = {
  template: `
      <div>
        <admin_navbar v-if="token" />
  
        <div v-if="!token">
          <h1 style="color:red;">Not authorized.</h1>
        </div>

        <!-- Courses Section -->
        <section v-if="token" class="container home-course-section">
            <br>
            <br>
          <!-- Course Grid (Repeating Structure) -->
          <div class="home-course-grid">
            <div v-for="(course, index) in visibleCourses" :key="course.course_id" class="home-course">
              <div class="home-course-name">{{ course.course_name }}</div>
              <div class="home-course-fees">Fees: {{ course.fees }}</div>
              <div class="home-course-fees">Teacher: {{ course.teacher }}</div>
              <div class="home-course-fees">Level: {{ course.level }}</div>
              <div class="home-course-fees">
                Pre-requisite:
                {{ course.pre_req1 && course.pre_req1 !== "Nil" ? course.pre_req1 : "None" }}
                {{ (course.pre_req1 && course.pre_req1 !== "Nil") && (course.pre_req2 && course.pre_req2 !== "Nil") ? ',' : '' }}
                {{ course.pre_req2 && course.pre_req2 !== "Nil" ? course.pre_req2 : '' }}
              </div>
              <button class="home-view-button" @click="gocoursepage(course.course_name)">
                View
              </button>
            </div>
          </div>
  
          <!-- Show More Button -->
          <button @click="showMore" type="button" class="home-generate-btn">Show More</button>
        </section>
      </div>
    `,
  components: { admin_navbar: admin_navbar },
  data() {
    return {
      courses: [],
      visibleCourses: [], // Updated to hold the visible courses
      coursesPerPage: 6, // Number of courses per page
      currentPage: 1, // Current page number
      token: localStorage.getItem("auth_token"),
    };
  },
  mounted() {
    if (this.token) {
      this.fetchdata();
    }
  },
  methods: {
    gocoursepage(course_name) {
      this.$router.push({
        name: "admin_coursepage",
        params: { course: course_name },
      });
    },
    fetchdata() {
      fetch("/api/courses", {
        method: "GET",
        headers: {
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.courses = data;
          this.updateVisibleCourses();
        });
    },
    updateVisibleCourses() {
      const startIndex = 0;
      const endIndex = this.currentPage * this.coursesPerPage;
      this.visibleCourses = this.courses.slice(startIndex, endIndex);
    },
    showMore() {
      this.currentPage++;
      this.updateVisibleCourses();
    },
  },
};

export default admin_home;
