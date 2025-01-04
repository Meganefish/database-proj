<template>
    <div class="container">
      <!-- 左侧：招聘信息列表 -->
      <div class="left">
        <h1>招聘信息列表</h1>
        <div id="job-list">
          <div v-for="job in jobs" :key="job.id" class="job-container">
            <a :href="job.job_card_link" target="_blank">
              <div>
                <span class="job-title">{{ job.title }}</span>
                <span class="salary">({{ job.salary_min }}-{{ job.salary_max }}元/天)</span>
              </div>
              <div class="job-keywords">
                <span v-for="(keyword, index) in job.key_words.slice(0, 3)" :key="index" class="keyword">{{ keyword }}</span>
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
      </div>
  
      <!-- 右侧：图表 -->
      <div class="right">
        <div class="keyword-filter">
          <h3>选择关键词筛选：</h3>
          <form @submit.prevent="filterJobs">
            <div class="keywords-container">
              <label v-for="(keyword, index) in all_keywords" :key="index">
                <input type="checkbox" :value="keyword" v-model="selected_keywords"> {{ keyword }}
              </label>
            </div>
          </form>
        </div>
        <h1>关键词频率分析</h1>
        <div v-html="pie_html"></div>
        <div v-html="bar_html"></div>
        <h1>关键词对应的平均薪资</h1>
        <div v-html="salary_bar_html"></div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        jobs: [],
        all_keywords: [],
        selected_keywords: [],
        pie_html: '',
        bar_html: '',
        salary_bar_html: '',
      };
    },
    methods: {
      async fetchData() {
        try {
          const response = await axios.get('/api/jobs', {
            params: { keywords: this.selected_keywords },
          });
          this.jobs = response.data.jobs;
          this.all_keywords = response.data.all_keywords;
          this.pie_html = response.data.pie_html;
          this.bar_html = response.data.bar_html;
          this.salary_bar_html = response.data.salary_bar_html;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      filterJobs() {
        this.fetchData();
      }
    },
    mounted() {
      this.fetchData();
    }
  };
  </script>
  
  <style scoped>
  /* 你的样式保持不变 */
  </style>
  