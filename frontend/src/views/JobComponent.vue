<template>
  <div class="profile-container">
    <profile-head></profile-head>
    <div class="container">      
      <div class="main">
        <div class="return-to-home" @click="BackToHome"><strong>{{ '↩️返回主页' }}</strong></div>
        <div class="up">
          <div class="keyword-filter">
            <h3>选择关键词筛选：</h3>
            <form @submit.prevent="filterJobs">
              <div class="keywords-container">
                <label v-for="(keyword, index) in all_keywords" :key="index" class="keyword-label">
                  <input type="checkbox" :value="keyword" v-model="selected_keywords" class="keyword-checkbox" />
                  <span class="keyword-text">{{ keyword }}</span>
                </label>
              </div>
              <!-- 筛选按钮 -->
              <button type="submit" class="filter-button">筛选</button>
            </form>
          </div>
        </div>

        <div class="down">
          <h1>招聘信息列表</h1>
          <div id="job-list">
            <div v-for="job in paginatedJobs" :key="job.id" class="job-container">
              <a :href="job.job_card_link" target="_blank">
                <div class="job-header">
                  <span class="job-title">{{ job.title }}</span>
                  <span class="salary">({{ job.salary_min }}-{{ job.salary_max }}元/天)</span>
                </div>
                <div class="job-keywords">
                  <span v-for="(keyword, index) in job.key_words" :key="index" class="keyword">
                    {{ keyword }}
                  </span>
                </div>
                <div class="job-detail">
                  <span class="job-label">通勤时间:</span> {{ job.duration_hours_minutes }}
                  <span class="job-label">通勤费用:</span> {{ job.cost }}元
                </div>
                <div class="job-detail">
                  <span class="job-label">到岗要求:</span> {{ job.internship_days }} 天/周 {{ job.internship_months }} 个月
                </div>
                <div class="job-detail">
                  <span class="job-label">地址:</span> {{ job.address }}
                </div>
              </a>
            </div>
          </div>

          <!-- 分页控件 -->
          <div class="pagination">
            <button
              :disabled="currentPage === 1"
              @click="changePage(currentPage - 1)"
              class="pagination-button"
            >
              上一页
            </button>
            <span class="page-number">{{ currentPage }} / {{ Math.ceil(totalJobs / pageSize) }}</span>
            <button
              :disabled="currentPage === Math.ceil(totalJobs / pageSize)"
              @click="changePage(currentPage + 1)"
              class="pagination-button"
            >
              下一页
            </button>
          </div>
        </div>
      </div>

      <div class="side">
        <h1>关键词频率分析</h1>
        <div class="chart-container" id="pie-chart"></div>
        <div class="chart-container" id="bar-chart"></div>
        <h1>关键词对应的平均薪资</h1>
        <div class="chart-container" id="salary-bar-chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import profileHead from './profile_box/profile_head.vue'
import axios from 'axios';
import * as echarts from 'echarts';
import router from '@/router/Router.js';

export default {
  name: 'JobComponent',
  components: {
    profileHead,
  },
  data() {
    return {
      jobs: [], // 所有的招聘信息
      all_keywords: [],
      selected_keywords: [],
      currentPage: 1, // 当前页码
      pageSize: 5, // 每页显示的招聘信息数量
      totalJobs: 0, // 总招聘信息数量
      paginatedJobs: [], // 当前页显示的招聘信息
      pieChart: null,
      barChart: null,
      salaryBarChart: null,
    };
  },
  setup() {
    const BackToHome = () => {
      router.push({ path: '/home' });
    };
    return {
      BackToHome,
    }
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('/job', {
          params: { keywords: this.selected_keywords },
        });
        this.jobs = response.data.jobs;
        this.all_keywords = response.data.all_keywords;
        this.totalJobs = this.jobs.length; // 更新总数据量
        this.paginateJobs(); // 根据当前页码更新显示的招聘信息
        this.renderPieChart(JSON.parse(response.data.pie_html));
        this.renderBarChart(JSON.parse(response.data.bar_html));
        this.renderSalaryBarChart(JSON.parse(response.data.salary_bar_html));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },

    // 根据当前页码获取当前页的招聘信息
    paginateJobs() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.paginatedJobs = this.jobs.slice(start, end); // 获取当前页的招聘信息
    },

    // 改变页码时重新加载数据
    changePage(pageNumber) {
      this.currentPage = pageNumber;
      this.paginateJobs();
    },

    filterJobs() {
      this.fetchData();
    },

    renderPieChart(pieChartData) {
      const chartDom = document.getElementById('pie-chart');
      if (!this.pieChart) {
        this.pieChart = echarts.init(chartDom);
      }
      this.pieChart.setOption(pieChartData);
    },

    renderBarChart(barChartData) {
      const chartDom = document.getElementById('bar-chart');
      if (!this.barChart) {
        this.barChart = echarts.init(chartDom);
      }
      this.barChart.setOption(barChartData);
    },

    renderSalaryBarChart(salaryBarChartData) {
      const chartDom = document.getElementById('salary-bar-chart');
      if (!this.salaryBarChart) {
        this.salaryBarChart = echarts.init(chartDom);
      }
      this.salaryBarChart.setOption(salaryBarChartData);
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.profile-container {
  display: flex;
  width: 100%;
  margin: 0 auto;
  flex-direction: column;
  height: 100vh;
}

.container {
  width: 80%;
  margin: 0 auto;
  display: flex;
  flex: 1;
  padding: 15px;
}

.main {
  flex: 7;
  display: flex;
  flex-direction: column;
  margin-right: 60px;
}

.side {
  flex: 3;
}

.up {
  margin-bottom: 10px;
}

.down {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-size: 14px; /* 全局字体大小调整 */
}

.job-container {
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 15px;
  margin-bottom: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.job-container:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.job-title {
  font-size: 1.4em;  
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}

.salary {
  color: #e7643c;
  font-weight: 600;
  font-size: 1.2em;  
}

.job-keywords {
  font-size: 1em;  
  color: #757373;
  margin-bottom: 12px;
  margin-top: 12px;
}

.keyword {
  background-color: #e1f0f6;
  padding: 6px 10px;
  margin-right: 8px;
  border-radius: 5px;
  font-size: 13px;  
}

.job-detail {
  margin-top: 10px;
  font-size: 1em;  
  color: #555;
}

.job-label {
  font-weight: bold;
  color: #333;
}

.chart-container {
  width: 100%;
  height: 350px; /* 适当调整高度 */
  gap: 15px;
  margin-bottom: 25px;
  padding: 12px;
  border: 1px solid #ddd;
  background-color: #fafafa;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.keyword-filter {
  width: 100%;
  padding: 18px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.keywords-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.keyword-label {
  display: flex;
  align-items: center;
}

.keyword-checkbox {
  margin-right: 6px;
}

.filter-button {
  background-color: #4CAF50;
  color: white;
  padding: 8px 12px;
  font-size: 1em;  
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.filter-button:hover {
  background-color: #45a049;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;
}

.pagination-button {
  background-color: #4CAF50;
  color: white;
  font-size: 1em;  
  padding: 6px 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin: 0 8px;
}

.pagination-button:hover {
  background-color: #45a049;
}

.pagination-button:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

.page-number {
  font-size: 1em;
  font-weight: bold;
  color: #555;
}
a {
  color: inherit;
  text-decoration: none; /* 去掉下划线 */
}

.return-to-home {
  font-size: 16px;
  padding: 10px;
  cursor: pointer;
}
</style>
