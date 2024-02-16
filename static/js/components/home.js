import navbar from "./navbar.js";

const home = {
  template: `
    <div>
      <div v-if="!token">
      <h1 style="color:red;">Not authorized.</h1>
      </div>
      <div>
      <div v-if="token">
        <navbar />
        <div class="alert alert-danger" v-if="errormessage">
          <p>
              {{ errormessage }}
              <span v-if="countdown > 0">
                  Redirecting in {{ countdown }} {{ countdown === 1 ? 'second' : 'seconds' }}...
              </span>
          </p>
      </div>
        <!-- Recommendations Section -->
        <header class="recommendation-header">
          <h1 style="margin-left: 110px; margin-top:20px;">Top Recommendations</h1>
        </header>
        <main>
          <section id="home-recommendations" class="container home-recommendations-container">
            <!-- Recommendation Cards (Repeating Structure) -->
            <div v-for="(recommendation, index) in displayedRecommendations" :key="index" class="home-card">
              <div class="home-card-header">
                <h2 class="home-h2">Recommendation {{ index + 1 }}</h2>
              </div>
              <div class="home-card-body">
                <!-- Display courses in the sublist -->
                <ul class="home-course-list">
                  <router-link v-for="course in recommendation" :key="course.course_id" :to="'/coursepage/' + course.course_name" class="home-course-box">
                    <li>{{ course.course_name }}<span v-if="course.isPrerequisite" style="color: red;"> *</span></li>
                  </router-link>
                </ul>
                <!-- Calculate and display total fees, average toughness, average marks, and average success rate -->
                <div class="home-summary">
                  <div>Total Fees: {{ calculateTotalFees(recommendation) }}</div>
                  <div>Average Toughness: {{ calculateAverageToughness(recommendation) }}/10</div>
                  <div>Average Grade: {{ calculateAverageMarks(recommendation) }}</div>
                </div>
                <button type="button" class="home-save-btn" @click="saverecommedation(recommendation)">Save</button>
              </div>
            </div>
          </section>
          <!-- Generate New Button -->
          <button type="button" class="home-generate-btn" @click="generateNewRecommendations">Generate New</button>
        </main>
      </div>

      <!-- Courses Section -->
      <section class="container home-course-section" v-if="token">
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
          <div class="alert alert-danger" role="alert" v-if="token">
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
            <div class="home-course-fees">Toughness: {{ course.toughness }}</div>
            <button class="home-view-button" @click="gocoursepage(course.course_name)">
              View
            </button>
          </div>
        </div>
      </section>
      </div>
    </div>
  `,
  components: { navbar: navbar },
  data() {
    return {
      recommendations: [],
      courses: [],
      displayedRecommendations: [],
      recommendationIndex: 0,
      batchSize: 3,
      courseSearchQuery: "",
      filterOption: "all",
      searchPerformed: false,
      errormessage: "",
      countdown: 10,
      token: localStorage.getItem("auth_token"),
      savedRecommendations: [],
    };
  },
  mounted() {
    this.fetchdata();
    this.fetchrecommendationdata();
    this.fetchSavedRecommendations();
  },
  methods: {
    gocoursepage(course_name) {
      this.$router.push({
        name: "coursepage",
        params: { course: course_name },
      });
    },
    fetchSavedRecommendations() {
      // fetch to "api/savedrecommendations" and get the course_name out of it and store it in savedRecommendations
      fetch("/api/savedrecommendation", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())

        .then((data) => {
          this.savedRecommendations = data;
          console.log(data);
        })
        .catch((error) => {
          console.error("Error fetching saved recommendations:", error);
        });
    },
    saverecommedation(courses) {
      let course = {};
      const names = {
        0: "course_one",
        1: "course_two",
        2: "course_three",
        3: "course_four",
      };
      for (let i = 0; i < courses.length; i++) {
        course[names[i]] = courses[i].course_name;
      }
      if (this.savedRecommendations.length === 3) {
        const confirmdelete = window.confirm(
          "You have already saved 3 recommendations. Do you want to delete the oldest recommendation and save this one?"
        );
        if (!confirmdelete) return;
      } else {
        const confirmsave = window.confirm(
          "Are you sure you want to save this recommendation?"
        );
        if (!confirmsave) return;
      }
      fetch("/api/recommendation", {
        method: "POST",
        body: JSON.stringify(course),
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => {
          if (response.ok) {
            alert("Recommendation Saved");
          } else {
            alert("Recommendation not saved");
          }
        })
        .then((data) => {
          this.fetchSavedRecommendations();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchdata() {
      fetch("/usercourses", {
        method: "GET",
        headers: {
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.courses = data;
          if (this.courses.length === 0) {
            this.errormessage =
              "No courses available! Please update your profile! You will be redirected to the profile page shortly.";
            // Start the countdown when an error message is displayed
            const countdownInterval = setInterval(() => {
              if (this.countdown > 0) {
                this.countdown--;
              } else {
                clearInterval(countdownInterval);
                this.errormessage = "";
                this.$router.push({ name: "profile" });
              }
            }, 1000); // Update every second
          }
        });
    },

    fetchrecommendationdata() {
      fetch("/api/recommendation", {
        method: "GET",
        headers: {
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.recommendations = data;
          console.log(this.recommendations);
          // Create a set to keep track of course names in the first sublist
          const firstSublistCourses = new Set();

          // Set isPrerequisite to true for courses in the first sublist
          if (this.recommendations.length > 0) {
            this.recommendations[0].forEach((course) => {
              firstSublistCourses.add(course.course_name);
              course.isPrerequisite = true;
            });
          }

          // Iterate through other sublists and set isPrerequisite based on the set
          for (let i = 1; i < this.recommendations.length; i++) {
            this.recommendations[i].forEach((course) => {
              course.isPrerequisite = firstSublistCourses.has(
                course.course_name
              );
            });
          }
          this.recommendations = this.recommendations.slice(
            1,
            this.recommendations.length
          );

          this.generateNewRecommendations();
        });
    },

    calculateTotalFees(courses) {
      return courses.reduce((total, course) => total + course.fees, 0);
    },
    calculateAverageToughness(courses) {
      const totalToughness = courses.reduce(
        (total, course) => total + course.toughness,
        0
      );
      const averageToughness = totalToughness / courses.length;
      return averageToughness.toFixed(2);
    },
    calculateAverageMarks(courses) {
      const totalMarks = courses.reduce(
        (total, course) => total + course.avg_marks,
        0
      );
      const averageMarks = totalMarks / courses.length;
      let grade;

      if (averageMarks >= 90) {
        grade = "S";
      } else if (averageMarks >= 80) {
        grade = "A";
      } else if (averageMarks >= 70) {
        grade = "B";
      } else if (averageMarks >= 60) {
        grade = "C";
      } else if (averageMarks >= 50) {
        grade = "D";
      } else {
        grade = "E";
      }

      return grade;
    },

    calculateAverageSuccessRate(courses) {
      const totalSuccessRate = courses.reduce(
        (total, course) => total + course.success_rate,
        0
      );
      const averageSuccessRate = totalSuccessRate / courses.length;
      return averageSuccessRate.toFixed(2);
    },
    juggle(array) {
      // Fisher-Yates shuffle algorithm
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
    },

    generateNewRecommendations() {
      // Increment the recommendationIndex to show the next set of recommendations
      this.recommendationIndex += this.batchSize;

      // Check if recommendationIndex exceeds the length of recommendations
      if (this.recommendationIndex >= this.recommendations.length) {
        // Reset recommendationIndex to 0 to start again from the beginning
        this.recommendationIndex = 0;
      }

      // Calculate the endIndex to ensure only 3 recommendations are shown
      const endIndex = Math.min(
        this.recommendationIndex + this.batchSize,
        this.recommendations.length
      );

      // Update displayedRecommendations with the next batch of recommendations
      const restBatch = this.recommendations.slice(
        this.recommendationIndex,
        endIndex
      );

      // Combine the first recommendation with the rest in the desired order
      this.displayedRecommendations = restBatch;

      // Update the index in displayedRecommendations
      this.displayedRecommendations.forEach((recommendation, index) => {
        this.$set(
          recommendation,
          "index",
          this.recommendationIndex + index + 1 // Adjusted index to start from 1
        );
      });
    },
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
};

export default home;
