<template>
  <div class="section">
    <div class="section-title">Projects</div>
    <div class="project" v-for="(project, index) in sortedProjects" :key="index">
      <div class="project-header">
        <div v-if="project.links" class="project-title mylink" v-html="project.title" @click="openLink(project.links[0].link)" />
        <div v-else class="project-title" v-html="project.title" />
        <div class="date">{{ project.end_date}}</div>
      </div>
      <div class="project-body">
        <div class="project-body-text">
          <div>
            <span v-if="project.context" class="project-context" >{{ project.context }}<span v-if="project.affiliation">, </span></span>
            <span class="affilation">{{ project.affiliation }}</span>
          </div>  
          <div class="description" v-html="project.description" />
          <div class="collaborators" v-if="project.collaborators">Collaborators : {{ project.collaborators.join(', ') }}</div>
        </div>
        <qrcode-vue class="qr-code" v-if="project.links" :value="project.links[0].link" :size="30" />
      </div>
    </div>
  </div>  
</template>

<script>
import QrcodeVue from 'qrcode.vue';

export default {
  name: "Projects",
  components: {
    QrcodeVue
  },
  props: {
    projects: Array
  },
  computed: {
    sortedProjects() {
      console.log([...this.projects].sort((a, b) => 
        this.parseDate(a.end_date) > this.parseDate(b.end_date)).map(d => d.end_date));
      return [...this.projects].sort((a, b) => 
        this.parseDate(a.end_date) > this.parseDate(b.end_date)
      );
    },
  },
  methods: {
    openLink(link) {
      window.open(link, '_blank');
    },
    parseDate(d) {
      let parts = d.split('/');
      console.log(`${parts[1]}${parts[0]}`);
      return `${parts[1]}{${parts[0]}}`
    }
  }
}
</script> 

<style>
  .project-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .project-title {
    font-weight: bold;
  }

  .project-body {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 2em;
  }

  .project-context {
    font-style: italic;
  }

  .qr-code {
    margin-top: 1em;
  }

  .mylink:hover {
    text-decoration: underline;
    cursor: pointer;
  }
</style>