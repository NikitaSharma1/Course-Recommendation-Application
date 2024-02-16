const login = Vue.component("login", {
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

    <div class="container" style="display: flex; align-items: center; justify-content: center; margin-top: 7%;">
      <div class="row">
        <!-- Course Recommendation Section -->
        <div class="col-md-7">
          <div class="login-main-content main-content"  style="margin-top: 7%;">
            <h1 class="login-h1">Course Recommendation</h1>
            <p>
            Discover a smarter path to success with our Course Recommendation System. Personalized, practical, and designed for you. Simplify your academic journey and make informed choices effortlessly. Start exploring now!
            </p>
            <router-link to="/explorepage" class="login-explore-btn explore-btn btn btn-primary">Explore</router-link>
          </div>
        </div>

        <!-- Login Container -->
        <div class="col-md-5">
          <div class="login-container">
            <h2 class="login-h2">Log In</h2>
            <h6 v-if="showmessage" class="login-error-message">{{ msg }}</h6>
            <form @submit.prevent="login">
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" v-model="email" class="form-control" id="email" name="email">
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input type="password" v-model="password" class="form-control" id="password" name="password">
              </div>
              <button type="submit" class="login-btn login-btn btn btn-primary">Log In</button>
              <p class="login-signup-prompt signup-prompt">Don't have an account? <router-link to="/register">Signup</router-link></p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
`,
  data: function () {
    return {
      email: "",
      password: "",
      showmessage: false,
      msg: "",
      role: "",
    };
  },
  methods: {
    getroles() {
      fetch("/getroles", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.role = data;
          if (this.role === "student") {
            this.$router.push("/home");
          } else if (this.role === "admin") {
            this.$router.push("/admin_home");
          }
          console.log(this.role);
        });
    },
    login() {
      const data = {
        email: this.email,
        password: this.password,
      };
      console.log(data);
      fetch("http://127.0.0.1:8080/login?include_auth_token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Invalid email/password");
          }
        })
        .then((data) => {
          localStorage.setItem(
            "auth_token",
            data.response.user.authentication_token
          );
          // Redirect to another route after successful login
          this.getroles();
        })
        .catch((error) => {
          this.showmessage = true;
          setTimeout(() => {
            this.showmessage = false;
          }, 3000);
          this.msg = "Invalid email/password";
          console.error(error);
        });
    },
  },
});

export default login;
