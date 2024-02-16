import admin_navbar from "./admin_navbar.js";

const editcoursepage = {
  template: `
    <div>
    <admin_navbar />
    <div>
    
    <form @submit.prevent="submitForm" class="editcourse-form">
          <h2>Edit Course: {{courseName}}</h2>
          <div class="alert alert-success" v-if="showmessage">
            <p>{{ showmessage }}</p>
          </div>
          <div class="alert alert-danger" v-if="errormessage">
            <p>{{ errormessage }}</p>
          </div>

          <div class="form-group">
            <div class="row">
              <div class="col-md-6">
                <label for="editcourseName" class="editcourse-label">Course Name</label>
                <input v-model="course.course_name" type="text" id="editcourseName" name="editcourseName" class="editcourse-input" readonly>
              </div>
              <div class="col-md-6">
                <label for="editcourselevel" class="editcourse-label">Course Level</label>
                <input v-model="course.level" type="text" id="editcourselevel" name="editcourselevel" class="editcourse-input" required>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <label for="editcourseCredit" class="editcourse-label">Course Credit</label>
                <input v-model="course.course_credit" type="text" id="editcourseCredit" name="editcourseCredit" class="editcourse-input" required>
              </div>
              <div class="col-md-6">
                <label for="editcourseTeacher" class="editcourse-label">Course Teacher</label>
                <input v-model="course.teacher" type="text" id="editcourseTeacher" name="editcourseTeacher" class="editcourse-input" required>
              </div>
            </div>

            <div class="row">
              <!-- Add more pairs of input fields as needed -->
              <div class="col-md-6">
                <label for="editcourseContent" class="editcourse-label">Course Description</label>
                <input v-model="course.course_description" id="editcourseContent" name="editcourseContent" rows="8" class="editcourse-textarea" required></input>
              </div>
              <div class="col-md-6">
                <label for="editcoursePrerequisites" class="editcourse-label">Prerequisite 1</label>
                <input v-model="course.pre_req1" type="text" id="editcoursePrerequisites" name="editcoursePrerequisites" class="editcourse-input" required>
              </div>
            </div>

            <div class="row">
            <div class="col-md-6">
                <label for="editcourseToughness" class="editcourse-label">Toughness</label>
                <input v-model="course.toughness" type="text" id="editcourseToughness" name="editcourseToughness" class="editcourse-input" required>
              </div>
              <div class="col-md-6">
                <label for="editcoursePrerequisites" class="editcourse-label">Prerequisite 2</label>
                <input v-model="course.pre_req2" type="text" id="editcoursePrerequisites" name="editcoursePrerequisites" class="editcourse-input" required>
              </div>
              
            </div>

            <div class="row">
              <div class="col-md-6">
                <label for="editfees" class="editcourse-label">Fees</label>
                <input v-model="course.fees" type="text" id="editfees" name="editfees" class="editcourse-input" required>
              </div>
              <!-- Add more pairs of input fields as needed -->
            </div>

          </div>

          <div class="form-group">
            <button type="button" class="fb-cancel-btn" @click="cancelFeedback">Cancel</button>
            <button type="submit" class="fb-submit-btn">Submit</button>
          </div>
        </form>
    <div>
  </div>
    `,
  components: { admin_navbar: admin_navbar },
  data() {
    return {
      courseName: "",
      course: {},
      showmessage: "",
      errormessage: "",
    };
  },
  created() {
    this.courseName = this.$route.params.course;
    this.getcourse();
  },
  methods: {
    getcourse() {
      // Handle form submission logic here
      fetch("/getcourse/" + this.courseName, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("auth_token"),
        },
      })
        .then((res) => res.json())
        .then((data) => {
          this.course = data;
        })
        .catch((err) => console.log(err));
    },
    submitForm() {
      // Handle form submission logic here
      fetch("/api/courses/" + this.course.course_id, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("auth_token"),
        },
        body: JSON.stringify(this.course),
      })
        .then((res) => {
          if (res.status === 200) {
            return res.json();
          } else {
            throw new Error("Something went wrong");
          }
        })
        .then((data) => {
          this.showmessage = data.message;
          setTimeout(() => {
            this.showmessage = "";
            this.$router.push({
              name: "admin_coursepage",
              params: { course: this.courseName },
            });
          }, 5000);
        })
        .catch((err) => {
          this.errormessage = err.message;
          setTimeout(() => {
            this.errormessage = "";
          }, 5000);
        });
    },
    cancelFeedback() {
      // Implement your cancel logic here
      console.log("Feedback canceled");
      this.$router.push({
        name: "admin_coursepage",
        params: { course: this.courseName },
      });
    },
  },
};

export default editcoursepage;
