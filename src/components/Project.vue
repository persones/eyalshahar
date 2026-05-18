<template>
  <div class="project-container">
    <transition name="component-fade" mode="out-in">
      <div class="project border-box" :key="title">
        <h1 v-html="title"></h1>
        <div class="project-field project-subtitle">
          <span id="project-affiliation">{{ affiliation }}</span>
          <span v-if="context" id="project-context"> / {{ context }}</span>
          <span v-if="dates" id="project-dates"> / {{ dates }}</span>
        </div>
        <div class="project-content">
          <div class="project-content-text">
            <div class="project-field" v-if="role" id="role">
              <strong>Role:</strong>
              {{ role }}
            </div>
            <div id="project-description" class="project-field" v-html="description"></div>
            
            <div class="project-field" v-if="collaborators">
              <strong>Collaborators: </strong>
              <span v-for="c in collaborators" :key="c" class="collaborator">{{ c }}</span>
            </div>
            <div v-if="links" id="project-links" class="project-field">
              <strong>Links:</strong>
              <table>
                <tr v-for="link in links" :key="link.link">
                  <td>&gt;</td>
                  <td>
                    <a :href="link.link" target="_blank">{{ link.text }}</a>
                  </td>
                </tr>
              </table>
            </div>
          </div>
          <Gallery v-bind:images="calcImages"></Gallery>
        </div>
      </div>
    </transition>
  </div>
</template>

<style>
td {
  vertical-align: top;
}

h1 {
  margin: 0;
}

.collaborator:not(:last-child):after {
  content: " // ";
}

strong {
  text-transform: uppercase;
}

.project-field {
  margin: 0.7em 0;
}

.project-subtitle {
  font-style: italic;
}

</style>
<script>
var months = [
  "Jan'",
  "Feb'",
  "Mar'",
  "Apr'",
  "May",
  "Jun'",
  "Jul'",
  "Aug'",
  "Sep'",
  "Oct'",
  "Nov'",
  "Dec'"
];
function parseDate(d) {
  let parts = d.split("/");
  if (parts.length === 2) {
    return `${months[parseInt(parts[0] - 1)]} ${parts[1]}`;
  } else {
    return `${parts[0]} ${months[parseInt(parts[1])]} ${parts[2]}`;
  }
}
import Gallery from "./Gallery.vue";

export default {
  name: "Project",
  components: {
    Gallery
  },
  props: {
    title: String,
    affiliation: String,
    context: String,
    description: String,
    links: Array,
    start_date: String,
    end_date: String,
    role: String,
    collaborators: Array,
    images: Array
  },
  computed: {
    dates() {
      console.log(this.title);
      if (this.start_date) {
        return `${parseDate(this.start_date)} - ${parseDate(this.end_date)}`;
      } else if (this.end_date) {
        return parseDate(this.end_date);
      } else {
        return null;
      }
    },
    calcImages() {
      return this.images || [];
    }
  }
};
</script>