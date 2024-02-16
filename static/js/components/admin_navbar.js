const admin_navbar = {
  template: `
      <div>
      <nav class="navbar">
        <h1 class="navbar-brand">Course Recommendation</h1>
        <div class="nav-links">
          <router-link to="/admin_home" class="nav-link">Home</router-link>
          <router-link to="/admin_dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/logout" class="nav-link"><i class="fas fa-sign-out-alt"></i> Logout</router-link>
        </div>
      </nav>
      </div>
      `,
};

export default admin_navbar;
