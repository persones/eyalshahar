<template>
  <div class="gallery">
    <div id="gallery-prev" class="gallery-nav" v-if="currentImage > 0" @click="prev">&lt;&lt;</div>
    <div class="image-strip">
      <div v-for="image in images" :key=image.file class="captioned-image">
        <img v-if=image.file v-bind:src="image.file">
        <div class="video-container" v-if=image.youtube>
          <iframe v-bind:src="'https://www.youtube.com/embed/'+ image.youtube" frameborder="0" allow="accelerometer; autoplay; encrypted-media; " allowfullscreen></iframe>
        </div>
        <div v-if="image.caption" class="image-caption" v-html="image.caption"></div>
      </div>
    </div>
    <div id="gallery-next" class="gallery-nav" @click="next" v-if="currentImage < images.length - 1"> &gt;&gt;</div>
  </div>
</template>
<style>

  .image-strip {  
    overflow: hidden;
    display: flex;
    flex-direction: row;
  }
  
  @media only screen and (max-width: 1000px) {
    .image-strip {
      width: 100%;
    }
  }

  .gallery {
    display: flex;
    flex-direction: row;
    margin: 1em;
    align-items: center;
    justify-content: center;
  }

  

  .captioned-image {
    width: 100%;
    display: flex;
    flex-direction: column;
    flex-grow: 0; 
    flex-shrink: 0;
  }

  .captioned-image img {
    width: 100%;
  }

  .image-caption {
    text-align: center;
    font-style: italic;
  }

  .gallery-nav {
    font-size: 2em;
  }

  .video-container {
	position:relative;
	padding-bottom:56.25%;
	padding-top:30px;
	height:0;
	overflow:hidden;
}

.video-container iframe, .video-container object, .video-container embed {
	position:absolute;
	top:0;
	left:0;
	width:100%;
	height:100%;
}

</style>
<script>
export default {
  name: 'Gallery',
  data() {
    return {
      currentImage: 0
    }
  },
  props: {
    images: Array
  },
  methods: {
    prev() { 
      this.currentImage = Math.max(0, --this.currentImage)
      console.log('prev', this.currentImage);
      
    },
    next() {
     this.currentImage = Math.min(this.images.length, ++this.currentImage)
      console.log('next', this.currentImage);
    }
  }
};
</script>