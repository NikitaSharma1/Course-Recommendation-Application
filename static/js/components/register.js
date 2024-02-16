const register = {
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

    <div class="container" style="display: flex; align-items: center; justify-content: center; margin-top: 4%;">
      <div class="row">
        <!-- Course Recommendation Section -->
        <div class="col-md-7">
          <div class="login-main-content main-content" style="margin-top: 12%;">
            <h1 class="login-h1">Course Recommendation</h1>
            <p>
            Discover a smarter path to success with our Course Recommendation System. Personalized, practical, and designed for you. Simplify your academic journey and make informed choices effortlessly. Start exploring now!
            </p>
            <router-link to="/explorepage" class="login-explore-btn explore-btn btn btn-primary">Explore</router-link>
          </div>
        </div>
        <div class="col-md-5">
          <div class="login-container">
            <h2 class="login-h2">Register</h2>
          <h4 :class="{ 'register-text-success': ermsg === 'successfully registered!!', 'register-text-danger': ermsg !== 'successfully registered!!' }" v-if="showmessage">{{ ermsg }}</h4>
          <form class="register-form" @submit.prevent="register">
            <div class="form-group">
              <label for="username" class="register-label">Username:</label>
              <input v-model="formData.username" type="text" class="register-input" id="username" name="username" required>
              <p class="register-error" id="usernameError">{{ usernameError }}</p>
            </div>
            <div class="form-group">
              <label for="email" class="register-label">Email:</label>
              <input v-model="formData.email" type="email" class="register-input" id="email" name="email" required>
              <p class="register-error" id="emailError">{{ emailError }}</p>
            </div>
            <div class="form-group">
              <label for="password" class="register-label">Password:</label>
              <input v-model="formData.password" type="password" class="register-input" id="password" name="password" required>
            </div>
            <div>
              <input type="submit" class="login-btn login-btn btn btn-primary" value="Register">
              Already a user?<router-link to="/">Log In</router-link>
            </div>
          </form>
        </div>
    </div>
    `,
  data() {
    return {
      showmessage: false,
      ermsg: "",
      showform: true,
      formData: {
        username: "",
        email: "",
        password: "",
        password_confirm: "",
      },
      emailError: "",
      usernameError: "",
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    register() {
      const data = {
        user_name: this.formData.username,
        email: this.formData.email,
        password: this.formData.password,
      };
      fetch("http://127.0.0.1:8080/api/user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (response.status === 201) return response.json();
          else if (response.status === 400) {
            throw new Error("Bad Request");
          } else if (response.status === 409) {
            throw new Error("Conflict");
          }
        })
        .then((data) => {
          this.showmessage = true;
          this.ermsg = data.message;
          if (data.message === "successfully registered!!") {
            setTimeout(() => {
              this.$router.push("/");
            }, 2000);
          }
        })
        .catch((error) => {
          if (error.message === "Bad Request") {
            this.showmessage = true;
            this.ermsg = "Invalid input";
            setTimeout(() => {
              this.showmessage = false;
              this.ermsg = "";
            }, 3000);
          } else if (error.message === "Conflict") {
            this.showmessage = true;
            this.ermsg = "Username or Email already exists";
            setTimeout(() => {
              this.showmessage = false;
              this.ermsg = "";
            }, 3000);
          } else {
            this.showmessage = true;
            this.ermsg = "Something went wrong";
            setTimeout(() => {
              this.showmessage = false;
              this.ermsg = "";
            }, 3000);
          }
        });
    },
    fetchData() {
      fetch(`http://127.0.0.1:8080/api/user`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.userdata = data;
        });
    },
  },
  watch: {
    "formData.username": function (newVal) {
      this.usernameError = this.userdata.some(
        (user) => user.user_name === newVal
      )
        ? "Username already exists"
        : "";
    },
    "formData.email": function (newVal) {
      this.emailError = this.userdata.some((user) => user.email === newVal)
        ? "Email already exists"
        : "";
    },
  },
};

export default register;
