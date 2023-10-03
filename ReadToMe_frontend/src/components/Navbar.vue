<script>
export default {
    data() {
    return {
      isDarkmode: false
    }
  },
  methods: {
    themeSwitch() {
        if (document.documentElement.classList.contains("dark")) {
            document.documentElement.classList.remove("dark")
            localStorage.setItem("theme", "light")
            this.isDarkmode = !this.isDarkmode
            return
        }
        document.documentElement.classList.add("dark")
        localStorage.setItem("theme", "dark")
        this.isDarkmode = !this.isDarkmode
    }
  },
  created() {
    const userTheme = localStorage.getItem("theme")
    this.isDarkmode = userTheme == "dark" ? false : true
    const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches

    const themeCheck = () => {
        if (userTheme === "dark" || (!userTheme && systemTheme)) {
            document.documentElement.classList.add("dark")
            return
        }
    }
  }
}
</script>
<template>
    <div class="top-0 w-full border-b-2 dark:border-gray-300 bg-white text-black dark:bg-black dark:text-white z-50">
        <div class="max-w-7xl mx-auto p-4">
            <div class="flex justify-between items-center">
                <div>
                    <span class="font-thin">파일을</span>
                    <span class="font-black">읽어줘</span>
                </div>
                <div @click="themeSwitch" v-if="!isDarkmode" class="flex">
                    <div class="p-2 rounded bg-black text-white cursor-pointer">다크모드 전환</div>
                </div>
                <div @click="themeSwitch" v-if="isDarkmode" class="flex">
                    <div class="p-2 rounded bg-white text-black cursor-pointer">라이트모드 전환</div>
                </div>
            </div>
        </div>
    </div>
</template>