const contactnl = {
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
            <div class="contact-container">
                <div class="contact-image">
                    <img class="contact-image" src="static/js/contact.png" alt="contact-us">
                </div>
                <form class="contact-form">
                    <div class="alert alert-info" v-if="showmessage">
                        <p>{{ showmessage }}</p>
                    </div>
                    <div class="alert alert-danger" v-if="errormessage">
                        <p>{{ errormessage }}</p>
                    </div>
                    <h2 class="contact-h2">CONTACT US</h2>
                    <p class="contact-p" type="Name:"><input class="contact-input" v-model="name" placeholder="Write your name here.."></p>
                    <p class="contact-p" type="Email:"><input class="contact-input" v-model="email" placeholder="Let us know how to contact you back.."></p>
                    <p class="contact-p" type="Message:"><input class="contact-input" v-model="message" placeholder="What would you like to tell us.."></p>
                    <button class="contact-button" @click="send">Send Message</button>
                </form>
            </div>
        </div>
    `,
  data() {
    return {
      name: "",
      email: "",
      message: "",
      showmessage: "",
      errormessage: "",
    };
  },
  methods: {
    send() {
      fetch("/email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: this.name,
          email: this.email,
          message: this.message,
        }),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else if (response.status == 500) {
            throw new Error("Message not sent");
          }
        })
        .then((data) => {
          this.name = "";
          this.email = "";
          this.message = "";
          this.showmessage = data.message;
          setTimeout(() => {
            this.showmessage = "";
          }, 5000);
          console.log(data);
        })
        .catch((error) => {
          this.errormessage = error.message;
          setTimeout(() => {
            this.errormessage = "";
          }, 5000);
        });
    },
  },
};

export default contactnl;
