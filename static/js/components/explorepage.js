const explorepage = {
  template: `
    <div>
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
    <!-- Courses Section -->
      <section class="container home-course-section">
        <h2>COURSES AVAILABLE</h2>
        <!-- Search Container for Courses -->
        <div class="home-search-container">
          <input type="text" class="home-search-bar" placeholder="Search" v-model="courseSearchQuery">
          <select class="home-filter-select" v-model="filterOption">
            <option value="all" selected>All Levels</option>
            <option value="hard">Hard</option>
            <option value="medium">Medium</option>
            <option value="easy">Easy</option>
          </select>
          
        </div>


        <!-- Course Grid (Repeating Structure) -->
        <div v-if="filteredCourses.length === 0">
          <div class="alert alert-danger" role="alert">
            Not available. Try different course name!!
          </div>
        </div>
        <div class="home-course-grid" v-else>
          <div v-for="course in filteredCourses" :key="course.course_id" class="home-course">
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
      </section>
    </div>
    `,
  data() {
    return {
      courseSearchQuery: "",
      filterOption: "all",
      courses: [],
    };
  },
  computed: {
    filteredCourses() {
      // Initial data
      let filteredCourses = this.courses;

      // Filter based on course name
      if (this.courseSearchQuery.trim() !== "") {
        const lowerCaseQuery = this.courseSearchQuery.toLowerCase();
        filteredCourses = filteredCourses.filter((course) =>
          course.course_name.toLowerCase().includes(lowerCaseQuery)
        );
      }

      // Filter based on difficulty level
      if (this.filterOption !== "all") {
        const difficultyFilter = (course) => {
          const toughness = course.toughness;
          if (toughness > 7 && this.filterOption === "hard") {
            return true;
          } else if (
            5 < toughness &&
            toughness <= 7 &&
            this.filterOption === "medium"
          ) {
            return true;
          } else if (toughness <= 5 && this.filterOption === "easy") {
            return true;
          }
          return false;
        };
        filteredCourses = filteredCourses.filter(difficultyFilter);
      }

      return filteredCourses;
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    gocoursepage(course_name) {
      this.$router.push({
        name: "explorecourses",
        params: { course: course_name },
      });
    },
    fetchData() {
      fetch("/api/courses", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.courses = data;
          console.log(this.courses);
        });
    },
  },
};

export default explorepage;
