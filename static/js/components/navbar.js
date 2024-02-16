const navbar = {
  template: `
    <div>
    <nav class="navbar">
    <router-link to="/login" class="navbar-brand">Course Recommendation</router-link>
      <div class="nav-links">
        <router-link to="/home" class="nav-link">Home</router-link>
        <router-link to="/profile" class="nav-link">Profile</router-link>
        <router-link to="/faq" class="nav-link">FAQs</router-link>
        <router-link to="/contact" class="nav-link">Contact Us</router-link>
        <router-link to="/logout" class="nav-link"><i class="fas fa-sign-out-alt"></i> Logout</router-link>
      </div>
    </nav>
    </div>
    `,
};

export default navbar;
