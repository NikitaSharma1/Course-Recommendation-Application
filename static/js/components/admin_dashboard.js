import admin_navbar from "./admin_navbar.js";
const admin_dashboard = {
  template: `
    <div>
      <admin_navbar></admin_navbar>
      <div class="dashboard-container">
        <h4 style="margin-left: 20px;">Average Grade Scored :</h4>
        <div class="dashboard-course-section">
          <div class="card dashboard-card" v-for="(courses, category) in courseData" :key="category">
            <div class="card-header dashboard-card-header" :style="{ backgroundColor: '#5b3e88', color: '#fff' }">
              {{ category }}
            </div>
            <ul class="list-group list-group-flush">
              <li class="dashboard-list-group-item" v-for="course in courses" :key="course.name">
                {{ course.name }} : {{ course.grade }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="dashboard-container">
  <h4 style="margin-left: 20px;">Additional Insights:</h4>
  <div class="dashboard-course-section">
    <div v-for="insight in insights" class="card dashboard-insights-card" :key="insight.label">
      <div class="card-header" :style="{ backgroundColor: '#5b3e88', color: '#fff' }">
        {{ insight.label }}
      </div>
      <div class="card-body">
        {{ insight.value }}
      </div>
    </div>

    <!-- Chart containers with equal sizing and spacing -->
    <div class="chart-container" style="width: 20%; margin-right: 10%;">
      <canvas id="totalStudentsChart"></canvas>
    </div>

    <!-- Chart for Student Distribution -->
    <div class="chart-container" style="width: 20%; margin-right: 10%;">
      <canvas id="studentDistributionChart"></canvas>
    </div>

    <!-- Chart for Grade Distribution -->
    <div class="chart-container" style="width: 30%;">
      <canvas id="gradeDistributionChart"></canvas>
    </div>
  </div>
</div>

      </div>
    </div>
  `,
  data() {
    return {
      courseData: {
        "Foundational Courses": [
          { name: "Mathematics", grade: "A" },
          { name: "Statistics", grade: "A" },
          { name: "Computational Thinking", grade: "A" },
          { name: "Programming in Python", grade: "A" },
          { name: "English", grade: "A" },
        ],
        "Degree Level Courses": [
          { name: "Deep Learning", grade: "A" },
          { name: "Artificial Intelligence", grade: "A" },
          { name: "Software Engineering", grade: "A" },
          { name: "Software Testing", grade: "A" },
          { name: "Strategies for Professional Growth", grade: "A" },
        ],
        "Diploma in Data Science": [
          { name: "Machine Learning Techniques", grade: "A" },
          { name: "Business Data Management", grade: "S" },
          { name: "Business Analytics", grade: "B" },
          { name: "Tools in Data Science", grade: "A" },
          { name: "Machine Learning Practice", grade: "B" },
        ],
        "Diploma In Programming": [
          { name: "DSA", grade: "A" },
          { name: "DBMS", grade: "A" },
          { name: "Application Development", grade: "A" },
          { name: "Java", grade: "A" },
          { name: "System Commands", grade: "A" },
        ],
      },
      total_students: 18966,
      complete_profile: 8885,
      working_professionals: 4000,
      college_students: 4041,
      standalone_students: 2040,
      gradeDistribution: {
        ">9": 1253,
        "8-9": 8854,
        "<8": 9562,
      },
    };
  },
  components: { admin_navbar: admin_navbar },
  mounted() {
    this.initTotalStudentsChart();
    this.initStudentDistributionChart();
    this.initGradeDistributionChart();
  },

  methods: {
    initTotalStudentsChart() {
      const ctx = document
        .getElementById("totalStudentsChart")
        .getContext("2d");
      this.initChart(
        ctx,
        ["Incomplete Profile", "Complete Profile"],
        [this.total_students, this.complete_profile],
        ["rgba(75, 192, 192, 0.2)", "rgba(255, 99, 132, 0.2)"]
      );
    },

    initStudentDistributionChart() {
      const ctx = document
        .getElementById("studentDistributionChart")
        .getContext("2d");
      this.initChart(
        ctx,
        ["Working Professionals", "College Students", "Standalone Students"],
        [
          this.working_professionals,
          this.college_students,
          this.standalone_students,
        ],
        ["#FF6384", "#36A2EB", "#FFCE56"]
      );
    },

    initChart(ctx, labels, data, backgroundColor) {
      new Chart(ctx, {
        type: "pie", // You can customize this based on your chart type
        data: {
          labels,
          datasets: [
            {
              label: "Number of Students",
              data,
              backgroundColor,
              borderColor: backgroundColor.map((color) => `${color}1`),
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
    initGradeDistributionChart() {
      const ctx = document
        .getElementById("gradeDistributionChart")
        .getContext("2d");
      const grades = Object.keys(this.gradeDistribution);
      const counts = Object.values(this.gradeDistribution);

      new Chart(ctx, {
        type: "bar",
        data: {
          labels: grades,
          datasets: [
            {
              label: "CGPA Distribution",
              data: counts,
              backgroundColor: "rgba(54, 162, 235, 0.2)", // Customize the color as needed
              borderColor: "rgba(54, 162, 235, 1)", // Customize the color as needed
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
  },
};
export default admin_dashboard;
