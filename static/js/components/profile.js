import navbar from "./navbar.js";

const profile = {
  template: `
        <div>
        <navbar />
        <div class="profile-container">
        <div class="profile-left-panel">
          <div class="profile-picture">
          <img src="static/js/pfp.jpg" alt="profile picture">
          </div>
          <div class="profile-info">
            <p>Name: {{ profileData.user_name }}</p>
            <p>Roll No.: {{ profileData.roll_no }}</p>
            <p>Email: {{ profileData.email }}</p>
            <p>DOB: {{ profileData.dob }}</p>
            <p>Course: {{ profileData.select_your_course }}</p>
            <p>Working Professional: {{ profileData.current_status=="Working Professional" ? 'Yes' : 'No' }}</p>
            <p>Standalone: {{ profileData.current_status=="Standalone" ? 'Yes' : 'No' }}</p>
          </div>
          <div class="profile-edit-button">
            <button @click="editProfile">Edit</button>
          </div>
        </div>
        <div class="profile-right-panel">
          <div class="profile-top-row">
            <div class="profile-box">
              <h1>{{ profileData.CGPA }}</h1>CGPA
            </div>
            <div class="profile-box">
              <label for="profile-showCompletedCourses" class="profile-button">Completed Courses</label>
              <input type="checkbox" id="profile-showCompletedCourses" class="profile-hidden-checkbox" @change="toggleCompletedCourses">
              <div class="profile-modal" v-if="showCompletedCourses">
                <label for="profile-showCompletedCourses" class="profile-close-btn">&times;</label>
                <h2>Completed Courses</h2>
                <ul>
                  <li v-for="course in completedCourses">{{ course }}</li>
                </ul>
              </div>
            </div>
            <div class="profile-box">
              <label for="profile-showSavedRecommendations" class="profile-button">Saved Recommendations</label>
              <input type="checkbox" id="profile-showSavedRecommendations" class="profile-hidden-checkbox" @change="togglerecomCourses">
              <div class="profile-modal" v-if="showSavedRecommendations">
                <label for="profile-showSavedRecommendations" class="profile-close-btn">&times;</label>
                <h2>Saved Recommendations</h2>
                <ul>
                  <div v-for="(recommendation, index) in savedRecommendations" :key="index" class="recommendation-card">
                    <div class="recommendation-header">
                      <h3>Recommendation {{ index + 1 }}</h3>
                    </div>
                    <div class="recommendation-body">
                      <ul class="recommendation-list">
                        <li v-if="recommendation.course_one" class="recommendation-item">Course One: {{ recommendation.course_one }}</li>
                        <li v-if="recommendation.course_two" class="recommendation-item">Course Two: {{ recommendation.course_two }}</li>
                        <li v-if="recommendation.course_three && recommendation.course_three !== 'Nil'" class="recommendation-item">Course Three: {{ recommendation.course_three }}</li>
                        <li v-if="recommendation.course_four && recommendation.course_four !== 'Nil'" class="recommendation-item">Course Four: {{ recommendation.course_four }}</li>
                      </ul>
                    </div>
                    <div class="recommendation-footer">
                      <button class="remove-btn" @click="removeRecommendation(recommendation)">Unsave</button>
                    </div>
                  </div>
                </ul>
              </div>
            </div>



          </div>
          <div class="profile-lorem-textbox">
            <h5>Description:</h5>
            <p>{{ profileData.about }}</p>
          </div>
          <div class="profile-bottom-row">
            <div class="profile-info-row">
              <span class="profile-info-title">Amount paid so far</span>
              <span class="profile-info-value">{{ amountPaid }}</span>
            </div>
            <div class="profile-info-row">
              <span class="profile-info-title">Credits acquired so far</span>
              <span class="profile-info-value">{{creditsAcquired }}</span>
            </div>
            <div class="profile-info-row">
              <span class="profile-info-title">Current year</span>
              <span class="profile-info-value">{{ currentYear }}</span>
            </div>
            <div class="profile-info-row">
              <span class="profile-info-title">Your Interests</span>
              <span class="profile-info-value">{{ profileData.interest }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    `,
  components: { navbar: navbar },
  data() {
    return {
      profileData: {},
      completedCourses: ["MLF", "MLT", "BDM", "MAD I"],
      savedRecommendations: [],
      showCompletedCourses: false,
      showSavedRecommendations: false,
      currentYear: 3,
      creditsAcquired: 88,
      amountPaid: 100000,
    };
  },
  mounted() {
    this.fetchprofile();
    this.fetchCompletedCourses();
    this.fetchAmountPaid();
    this.fetchCreditsAcquired();
    this.fetchSavedRecommendations();
  },
  methods: {
    togglerecomCourses() {
      this.showSavedRecommendations = !this.showSavedRecommendations;
    },
    toggleCompletedCourses() {
      this.showCompletedCourses = !this.showCompletedCourses;
    },

    fetchCompletedCourses() {
      // fetch to "api/completedcourses" and get the course_name out of it and store it in completedCourses
      fetch("/api/completedcourses", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.completedCourses = data.map((course) => course.course_name);
        });
    },

    fetchAmountPaid() {
      // fetch and store it in amountPaid
      fetch("/api/totalcost", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.amountPaid = data.total_cost;
        });
    },

    fetchCreditsAcquired() {
      // fetch and store it in creditsAcquired
      fetch("/api/totalcredits", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.creditsAcquired = data.total_credits;
        });
    },
    removeRecommendation(recommendation) {
      const confirmDelete = confirm(
        "Are you sure you want to unsave this recommendation?"
      );
      if (!confirmDelete) {
        return;
      }

      fetch(`/api/recommendation/${recommendation.r_id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
        body: JSON.stringify(recommendation),
      })
        .then((response) => response.json())
        .then((data) => {
          alert("Recommendation removed successfully!");
          this.fetchSavedRecommendations();
        })
        .catch((error) => {
          alert("Error removing recommendation!");
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

    formatDate(inputDate) {
      const date = new Date(inputDate);
      const day = date.getDate().toString().padStart(2, "0");
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const year = date.getFullYear();

      return `${year}-${month}-${day}`;
    },
    fetchprofile() {
      fetch("/api/studentdetails", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.profileData = {
            ...data,
            dob: this.formatDate(data.dob),
          };
        });
    },
    editProfile() {
      this.$router.push("/editprofile");
    },
    closeModal() {
      this.showCompletedCourses = false;
      this.showSavedRecommendations = false;
    },
  },
};

export default profile;
