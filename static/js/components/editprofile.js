import navbar from "./navbar.js";
const editProfile = {
  template: `
          <div>
          <navbar />
        <div class="signup-container">
        <div class="signup-form-container">
          <div class="signup-form-header text-center">
          <h2>Edit Profile</h2>
          </div>
                  <form class = "signup-form">
                  <div class="alert alert-success" v-if="showmessage">
                      <p>{{ showmessage }}</p>
                  </div>
                  <div class="alert alert-danger" v-if="errormessage">
                      <p>{{ errormessage }}</p>
                  </div>
                      <div class="signup-form-row">
                      <!-- Row 1 -->
                      <div class="col-md-4">
                          <label class="signup-form-label">Full Name</label>
                          <input type="text" class="signup-form-control" v-model="profileData.user_name" placeholder="Full Name" readonly>
                      </div>
                      <div class="col-md-4">
                          <label class="signup-form-label">How much time can you commit per week?</label>
                          <select class="signup-form-control" v-model="profileData.commit_per_week">
                              <option disabled selected>Select hours</option>
                              <option>20</option>
                              <option>30</option>
                              <option>40</option>
                          </select>

                      </div>
                      <div class="col-md-4">
                          <label class="signup-form-label">Date of birth</label>
                          <input type="text" class="signup-form-control" v-model="profileData.dob" placeholder="yyyy-mm-dd">
                      </div>
                  </div>
                  <div class="signup-form-row">
                      <!-- Row 2 -->
                      <div class="col-md-4">
                          <label class="signup-form-label">What's your budget per term?</label>
                          <select class="signup-form-control" v-model="profileData.budget_per_term">
                              <option disabled selected>Select your Budget</option>
                              <option>20000</option>
                              <option>30000</option>
                              <option>40000</option>
                          </select>
                      </div>
                      <div class="col-md-4">
                          <label class="signup-form-label">Email</label>
                          <input type="email" class="signup-form-control" v-model="profileData.email" placeholder="Email" readonly>
                      </div>
                      <div class="col-md-4">
                          <label class="signup-form-label">What's your CGPA so far?</label>
                          <input type="text" class="signup-form-control" v-model="profileData.CGPA" placeholder="CGPA">
                      </div>
                  </div>
                  <div class="signup-form-row">
                      <!-- Row 3 -->
                      <div class="col-md-4">
                          <label class="signup-form-label">What are your interests?</label>
                          <select class="signup-form-control" v-model="profileData.interest">
                              <option disabled selected>Select your interests</option>
                              <option>data Science</option>
                              <option>programming</option>
                          </select>
                      </div>
                      <div class="col-md-4">
                          <label class="signup-form-label">Select your course</label>
                          <select class="signup-form-control" v-model="profileData.select_your_course" required>
                              <option disabled selected>Select your course</option>
                              <option>BSc in DS and Programming</option>
                              <option>BS in DS and Application</option>
                              <option>Diploma in DS/Programming</option>
                          </select>
                      </div>
                      <div class="col-md-4">
                          <label class="signup-form-label">Current status</label>
                          <select class="signup-form-control" v-model="profileData.current_status">
                              <option disabled selected>Select your current status</option>
                              <option>Working Professional</option>
                              <option>College Student</option>
                              <option>Standalone</option>
                          </select>
                      </div>
                  </div>
                  <div class="signup-form-row">
                      <!-- Row 4 -->
                      <div class="col-md-4">
                          <label class="signup-form-label">About yourself</label>
                          <textarea type="text" class="signup-form-control form-control"  rows="3" v-model="profileData.about" placeholder="I am a student."></textarea>
                      </div>
                      <div class="col-md-4">
                          <!-- Leave this column empty for spacing -->
                      </div>
                  </div>
                          <div class="signup-form-row">
                              <div class="col">
                                  <button type="submit" class="btn signup-btn-next" @click="editProfile">Submit</button>
                                  <button type="button" class="btn signup-btn-cancel" @click="cancelupdatepassword">Cancel</button>
                              </div>
                          </div>
                      </form>

                      <form class="signup-form" @submit.prevent="submitCompletedCourses">
                      <br>
                      <div class="signup-form-header text-center">
                          <h2>Select Completed Course & Enter Your Grade</h2>
                      </div>
                      <div class="alert alert-success" v-if="showcmessage">
                          <p>{{ showcmessage }}</p>
                      </div>
                      <div class="alert alert-danger" v-if="errorcmessage">
                          <p>{{ errorcmessage }}</p>
                      </div>
                  
                      <div class="signup-form-header text-center">
                          <h3>Foundation Level</h3>
                      </div>
                  
                      <div class="signup-form-row">
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="maths1Checkbox">
                                  Mathematics I
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="maths1Field" name="maths1Field"
                                  v-model="completedCourses['Mathematics I']">
                          </div>
                  
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="maths2Checkbox">
                                  Mathematics II
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="maths2Field" name="maths2Field"
                                  v-model="completedCourses['Mathematics II']">
                          </div>
                  
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="compThinkingCheckbox">
                                  Computational Thinking
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="compThinkingField"
                                  name="compThinkingField" v-model="completedCourses['Computational Thinking']">
                          </div>
                      </div>
                      <div class="signup-form-row">
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="English1Checkbox">
                                  English I
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="english1Field" name="english1Field"
                                  v-model="completedCourses['English I']">
                          </div>
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="English2Checkbox">
                                  English II
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="english2Field" name="english2Field"
                                  v-model="completedCourses['English II']">
                          </div>
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="compThinkinggCheckbox">
                                  Python
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="pythonField" name="pythonField"
                                  v-model="completedCourses['Python']">
                          </div>
                      </div>
                  
                      <!-- Repeat the pattern for other Foundation Level courses -->
                  
                      <div class="signup-form-header text-center">
                          <h3>Diploma Level</h3>
                      </div>
                  
                      <div class="signup-form-row">
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="pdsaCheckbox">
                                  PDSA
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="pdsaField" name="pdsaField"
                                  v-model="completedCourses['PDSA']">
                          </div>
                  
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="javaCheckbox">
                                  Java
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="javaField" name="javaField"
                                  v-model="completedCourses['Java']">
                          </div>
                  
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="dbmsCheckbox">
                                  DBMS
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="dbmsField" name="dbmsField"
                                  v-model="completedCourses['DBMS']">
                          </div>
                      </div>
                      <div class="signup-form-row">
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="scCheckbox">
                                  System Commands
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="scField" name="scField"
                                  v-model="completedCourses['System Commands']">
                          </div>
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="bdmCheckbox">
                                  BDM
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="bdmField" name="bdmField"
                                  v-model="completedCourses['BDM']">
                          </div>
                          <div class="col-md-4">
                              <label class="signup-form-label">
                                  <input type="checkbox" id="tdsCheckbox">
                                  TDS
                              </label>
                              <input type="text" class="signup-form-control conditional-input" id="tdsField" name="tdsField"
                                  v-model="completedCourses['TDS']">
                          </div>
                      </div>
                  
                      <!-- Repeat the pattern for other Diploma Level courses -->
                  
                      <div class="signup-form-row">
                          <div class="col">
                              <button type="submit" class="btn signup-btn-next">Submit</button>
                              <button type="button" class="btn signup-btn-cancel" @click="cancelupdatepassword">Cancel</button>
                          </div>
                      </div>
                  </form>

                  <div class="signup-form-header text-center" style="margin-top:10px;">
                  <h2>Update Password</h2>
                  </div>
                      <form class="signup-form" @submit.prevent="updatePassword" style="margin-top:30px;">
                      <div class="alert alert-success" v-if="showumessage">
                          <p>{{ showumessage }}</p>
                      </div>
                      <div v-if="passwordsNotMatched" class="alert alert-danger" role="alert">
                            Passwords do not match.
                      </div>
                      <div class="signup-form-row">
                        <div class="col-md-4">
                          <label class="signup-form-label">New Password</label>
                          <input type="password" class="signup-form-control" v-model="newPassword" placeholder="New Password">
                        </div>
                        <div class="col-md-4">
                          <label class="signup-form-label">Confirm Password</label>
                          <input type="password" class="signup-form-control" v-model="confirmPassword" placeholder="Confirm Password">
                        </div>
                        <div class="col-md-4">
                          <!-- Leave this column empty for spacing -->
                        </div>
                      </div>
                      <div class="signup-form-row">
                        <div class="col">
                          <button type="submit" class="btn signup-btn-next">Submit</button>
                          <button type="button" class="btn signup-btn-cancel" @click="cancelupdatepassword">Cancel</button>
                        </div>
                      </div>
                    </form>
          
                  </div>
              </div>
          </div>
      `,
  components: { navbar: navbar },
  data() {
    return {
      profileData: {},
      completedCourses: {},
      name: "",
      email: "",
      showmessage: "",
      showumessage: "",
      errormessage: "",
      errorcmessage: "",
      showcmessage: "",
      newPassword: "",
      confirmPassword: "",
      passwordsNotMatched: false,
    };
  },
  created() {
    this.name = this.$route.params.name;
    this.email = this.$route.params.email;
  },
  mounted() {
    this.fetchProfile();
    this.fetchCompletedCourses();
  },
  methods: {
    cancelupdatepassword() {
      this.$router.push("/profile");
    },
    formatDate(inputDate) {
      const date = new Date(inputDate);
      const day = date.getDate().toString().padStart(2, "0");
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const year = date.getFullYear();

      return `${year}-${month}-${day}`;
    },
    editProfile() {
      fetch(`/api/studentdetails/${this.profileData.sd_id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
        body: JSON.stringify(this.profileData),
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else if (res.status == 500 || res.status == 400) {
            throw new Error("Profile not updated");
          }
        })
        .then((data) => {
          this.showmessage = data.message;
          setTimeout(() => {
            this.showmessage = "";
            this.$router.push("/profile");
          }, 5000);
        })
        .catch((error) => {
          this.errormessage = error.message;
          setTimeout(() => {
            this.errormessage = "";
          }, 5000);
        });
    },
    fetchProfile() {
      fetch("/api/studentdetails", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((res) => res.json())
        .then((data) => {
          this.profileData = {
            ...data,
            dob: this.formatDate(data.dob),
          };
        });
    },
    updatePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.passwordsNotMatched = true;
        return;
      }

      const data = {
        password: this.newPassword,
      };

      fetch("/api/user", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
        body: JSON.stringify(data),
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else if (res.status == 500 || res.status == 400) {
            throw new Error("Password not updated");
          }
        })
        .then((data) => {
          this.showumessage = data.message;
          this.newPassword = "";
          this.confirmPassword = "";
          this.passwordsNotMatched = false;
          setTimeout(() => {
            this.showumessage = "";
          }, 5000);
        })
        .catch((error) => {
          this.errormessage = error.message;
          setTimeout(() => {
            this.errormessage = "";
          }, 5000);
        });
    },
    submitCompletedCourses() {
      console.log("completed courses", this.completedCourses);
      // make a post method to /completedcourses with this.completedCourses and then route to /profile
      if (Object.keys(this.completedCourses).length === 0) {
        this.errorcmessage = "Please select a course";
        setTimeout(() => {
          this.errorcmessage = "";
        }, 5000);
        return;
      }
      fetch("/api/completedcourses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
        body: JSON.stringify(this.completedCourses),
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else if (
            res.status == 500 ||
            res.status == 400 ||
            res.status == 404
          ) {
            throw new Error("Completed courses not updated");
          }
        })
        .then((data) => {
          this.showcmessage = data.message;
          setTimeout(() => {
            this.showcmessage = "";
            this.$router.push("/profile");
          }, 5000);
        })
        .catch((error) => {
          this.errorcmessage = error.message;
          setTimeout(() => {
            this.errorcmessage = "";
          }, 5000);
        });
    },
    fetchCompletedCourses() {
      // Assuming you have a route to fetch completed courses for the user
      fetch("/api/completecoursesgrades", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((res) => res.json())
        .then((data) => {
          // Assuming the response structure as mentioned
          const [courseDetails, grades] = data;

          // Check if both lists are of the same length
          if (courseDetails.length === grades.length) {
            // Transform the data into the required format
            this.completedCourses = courseDetails.reduce(
              (acc, course, index) => {
                // Ensure the course has a valid course_name property
                if (course.course_name) {
                  acc[course.course_name] = grades[index];
                }
                return acc;
              },
              {}
            );
          } else {
            console.error(
              "Mismatch in the length of courseDetails and grades lists"
            );
          }
        })
        .catch((error) => {
          console.error("Error fetching completed courses:", error);
        });
    },
  },
};

export default editProfile;
