<template>
  <q-page class="flex flex-center">
    <div style="width: 500px; max-width: 90vw">
      <q-input
        v-model="form.password"
        type="password"
        @blur="$v.form.password.$touch"
        :float-label="$t('oldPassword')"
      />
      <q-input
        v-model="form.newPassword"
        type="password"
        @blur="$v.form.newPassword.$touch"
        :float-label="$t('newPassword')"
      />
      <q-input
        v-model="form.re_newPassword"
        type="password"
        :float-label="$t('newPassword')"
        @keyup.enter="changePass"
      />
      <q-btn
        @click="changePass"
        color="primary"
        class="full-width"
        :label="$t('update')"
      />
    </div>
  </q-page>
</template>

<style>
.q-btn {
  margin: 5px;
}
</style>

<script>
import { required, minLength } from "vuelidate/lib/validators"
export default {
  name: "PageChangepass",
  data() {
    return {
      username: "",
      form: {
        password: "",
        newPassword: "",
        re_newPassword: "",
      },
    }
  },
  validations: {
    form: {
      password: {
        required,
      },
      newPassword: {
        required,
        minLength: minLength(4),
      },
    },
  },
  methods: {
    changePass() {
      this.$v.form.$touch()
      if (this.$v.form.$error) {
        this.$q.notify({
          message: `${$t("newPasswordLength")}4${$t("characters")}`,
          position: "top-right",
          avatar: "statics/sad.png",
        })
        return
      }

      if (this.form.newPassword !== this.form.re_newPassword) {
        this.$q.notify({
          message: this.$t("newPasswordsMismatch"),
          position: "top-right",
          avatar: "statics/sad.png",
        })
        return
      }

      if (this.form.newPassword !== this.form.re_newPassword) {
        this.$q.notify({
          color: "red",
          textColor: "white",
          icon: "thumb_up",
          message: this.$t("inputsMismatch"),
          position: "top-right",
          avatar: "statics/sad.png",
          timeout: Math.random() * 5000 + 3000,
        })
        return
      }

      this.$api
        .put("/api/v1/user/change-pass", {
          password: this.form.password,
          new_password: this.form.newPassword,
        })
        .then((response) => {
          if (response.data.ok === true) {
            this.$q.notify({
              color: "green",
              textColor: "white",
              icon: "thumb_up",
              message: response.data.message,
              position: "top-right",
              avatar: "statics/huaji.png",
              timeout: Math.random() * 5000 + 3000,
            })
          } else {
            this.$q.notify({
              color: "red",
              textColor: "white",
              icon: "thumb_up",
              message: response.data.message,
              position: "top-right",
              avatar: "statics/sad.png",
              timeout: Math.random() * 5000 + 3000,
            })
          }
        })
        .catch((e) => {
          this.$q.notify({
            color: "red",
            textColor: "white",
            icon: "thumb_up",
            message: this.$t("invalidInput"),
            position: "top-right",
            avatar: "statics/sad.png",
            timeout: Math.random() * 5000 + 3000,
          })
        })
    },
  },
}
</script>
