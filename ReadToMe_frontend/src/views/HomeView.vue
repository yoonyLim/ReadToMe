<script>
import axios from 'axios';

export default {
  data() {
    return {
      isDragged: false,
      file: null,
      uploadedFile: null,
      processing: false,
      showProgress: false,
      sound: null
    }
  },
  methods: {
    onDragenter(event) {
      this.isDragged = true;
    },
    onDragleave(event) {
      this.isDragged = false;
    },
    onDragover(event) {
      event.preventDefault();
    },
    onDrop(event) {
      console.log(event.dataTransfer.files);
      event.preventDefault();
      this.isDragged = false;
      this.uploadFile(event.dataTransfer.files);
    },
    selectFile(event) {
      this.uploadFile(event.target.files);
    },
    uploadFile(files) {
      if (files.length > 1) {
        alert("파일을 하나만 선택해 주세요!");
        return;
      }

      const file = files[0];
  
      if (!file) {
        alert("파일을 선택해 주세요!");
        return;
      }

      const fileName = (file.name.length >= 12) ? file.name.substring(0, 13) + '...' + file.name.split('.')[1] : file.name;
      const formData = new FormData();
      formData.append("file", file);
      this.file = {name: fileName, loading: 0};
      this.processing = true
      this.showProgress = true;

      console.log('this file: ' + this.file);

      axios.post('http://127.0.0.1:8000/processFile/', formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        responseType: 'blob',
        onUploadProgress: ({loaded, total}) => {
          this.file.loading = Math.floor((loaded * 100) / total);
          if (loaded == total) {
            const fileSize = (total < 1024) ? total + 'KB' : (loaded / (1024 * 1024)).toFixed(2) + 'MB';
            this.uploadedFile = {name: fileName, size: fileSize};
            this.file = null;
            this.showProgress = false;
          }
        }
      }).then( res => {
        console.log(res)
        console.log(res.data)
        console.log(typeof(res.data))
        this.sound = res.data;
      }).catch(console.error);
    },
    play(sound) {
      var blob = new Blob([sound], {type: 'audio/mp3'})
      var url = URL.createObjectURL(blob)
      var audio = new Audio(url)
      audio.play();
    },
    download(sound) {
      const blob = new Blob([sound], {type: 'audio/mp3'})
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = this.uploadedFile.name.split('.')[0] + '.mp3'
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    }
  }
}
</script>

<template>
  <main class="flex justify-center h-full dark:bg-black dark:text-white">
    <div class="flex-1 max-w-7xl p-4">
      <div class="flex flex-col justify-between w-full h-full">
        <div class="flex-[0.2] flex items-center">
          <div>파일을 드래그 혹은 업로드하면 파일을 읽어드립니다!</div>
        </div>
        <div class="flex-[0.7] w-full h-full flex justify-center p-2 rounded shadow dark:shadow-gray-300" :class="isDragged ? 'bg-blue-100 dark:bg-gray-600' : ''"> <!-- [] can contain arbitrary value -->
          <!-- drag and drop area -->
          <div v-if="!processing" class="flex-1 w-full flex justify-center items-center border-dashed border-blue-200 border-2"
          @dragenter="onDragenter"
          @dragover="onDragover"
          @dragleave="onDragleave"
          @drop="onDrop">
            <div class="flex">
              <div class="p-2">파일을 드래그</div>
              <span class="px-8 py-2">-혹은-</span>
              <input type="file" name="file" ref="fileInput" hidden @change="selectFile"/>
              <div @click="$refs.fileInput.click()" class="p-2 bg-blue-400 text-white rounded border-solid cursor-pointer hover:bg-blue-600 focus:bg-blue-900">파일 업로드</div>
            </div>
          </div>
          <div v-if="showProgress || uploadedFile" class="flex-1 flex justify-center items-center max-w-4xl">
            <div class="flex justify-center w-full">
              <div v-if="showProgress" class="flex flex-col justify-center items-start w-full">
                <span class="mb-4">업로드 중: {{ file.name }}</span>
                <span class="mb-4">업로드 완료까지 {{ file.loading + '%' }}</span>
                <div class="bg-gray-200 w-full h-8 rounded">
                  <div class="bg-blue-300 h-full rounded" :style="{ width: file.loading + '%'}"></div>
                </div>
              </div>
              <div v-if="uploadedFile && !sound" class="flex flex-col items-center">
                <span class="mb-8 text-sm">업로드된 파일:</span>
                <div class="flex flex-col">
                  <span>이름: {{ uploadedFile.name }}</span>
                  <span>사이즈: {{ uploadedFile.size }}</span>
                </div>
                <div class="animate-bounce bg-blue-400 text-white rounded p-2 mt-8">
                  <span>서버에서 파일 변환 중...</span>
                </div>
              </div>
              <div v-if="sound">
                <div @click="play(sound)" class="bg-blue-300 rounded cursor-pointer p-4 mr-8">오디오 재생</div>
              </div>
              <div v-if="sound">
                <div @click="download(sound)" class="bg-blue-300 rounded cursor-pointer p-4">오디오 다운로드</div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex-[0.2] flex items-center">
          <a href="https://github.com/yoonyLim" target="_blank" class="flex items-center">
            <img class="w-10" src="../assets/github-mark.png">
            <span class="w-2"></span>
            <span>Link to Github</span>
          </a>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
&.dragged {
  opacity: 0.5;
}
</style>