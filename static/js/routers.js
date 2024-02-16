import login from "./components/login.js";
import register from "./components/register.js";
import home from "./components/home.js";
import coursepage from "./components/coursepage.js";
import feedback from "./components/feedback.js";
import Logout from "./components/logout.js";
import faq from "./components/faq.js";
import contact from "./components/contact.js";
import editProfile from "./components/editprofile.js";
import profile from "./components/profile.js";
import admin_home from "./components/admin_home.js";
import admin_dashboard from "./components/admin_dashboard.js";
import admin_coursepage from "./components/admin_coursepage.js";
import admin_editcoursepage from "./components/admin_editcoursepage.js";
import faqnl from "./components/faqnotlogin.js";
import contactnl from "./components/contactnotlogin.js";
import explorepage from "./components/explorepage.js";
import exploreCourses from "./components/explorecourses.js";

const router = new VueRouter({
  routes: [
    { path: "/", component: login, name: "login" },
    { path: "/register", component: register, name: "register" },
    { path: "/editprofile", component: editProfile, name: "editprofile" },
    { path: "/home", component: home, name: "home" },
    { path: "/coursepage/:course", component: coursepage, name: "coursepage" },
    { path: "/feedback/:course_name", component: feedback, name: "feedback" },
    { path: "/logout", component: Logout, name: "logout" },
    { path: "/faq", component: faq, name: "faq" },
    { path: "/contact", component: contact, name: "contact" },
    { path: "/profile", component: profile, name: "profile" },
    { path: "/admin_home", component: admin_home, name: "admin_home" },
    { path: "/faqnl", component: faqnl, name: "faqnl" },
    { path: "/contactnl", component: contactnl, name: "contactnl" },
    { path: "/explorepage", component: explorepage, name: "explorepage" },
    {
      path: "/explorecourses/:course",
      component: exploreCourses,
      name: "explorecourses",
    },
    {
      path: "/admin_dashboard",
      component: admin_dashboard,
      name: "admin_dashboard",
    },
    {
      path: "/admin_coursepage/:course",
      component: admin_coursepage,
      name: "admin_coursepage",
    },
    {
      path: "/admin_editcoursepage/:course",
      component: admin_editcoursepage,
      name: "admin_editcoursepage",
    },

    { path: "*", redirect: "/" },
  ],
  base: "/",
});

export default router;
