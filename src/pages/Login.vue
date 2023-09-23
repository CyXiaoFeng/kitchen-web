<template>
  <q-page class="flex flex-center">
    <div style="width: 500px; max-width: 90vw">
      <q-input v-model="username" :label="$t('username')" @keyup.enter="login" />
      <q-input
        v-model="password"
        type="password"
        :label="$t('password')"
        @keyup.enter="login"
      />
      <q-btn @click="login" color="primary" class="full-width" :label="$t('login')" />
    </div>
  </q-page>
</template>

<style>
.q-btn {
  margin: 5px;
}
</style>

<script>
import Qs from "qs"
export default {
  name: "PageLogin",
  data() {
    return {
      username: "",
      password: "",
    }
  },
  methods: {
    login() {
      var data = { username: this.username, password: this.password, timeout: 1000 }
      this.$api
        .post("/login", Qs.stringify(data), {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        })
        .then((response) => {
          // location.reload();
          window.location.href = "/"
          // this.$router.push('/working');
        })
        .catch((e) => {
          this.$q.notify({
            color: "red",
            textColor: "white",
            icon: "thumb_up",
            message: this.$t("incorrectUsernameOrPassword"),
            position: "top-right",
            avatar: "statics/sad.png",
          })
        })
    },
  },
}
</script>
