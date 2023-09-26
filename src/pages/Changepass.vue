<!-- 
  TODO:下面的连接专门讲解了vuelidate的用法，比较详细
  https://learnvue.co/articles/intro-to-vuelidate#using-vuelidate-with-the-composition-api 
  -->
<template>
  <q-page class="flex flex-center">
    <div style="width: 500px; max-width: 90vw">
      <q-input
        v-model="state.form.password"
        type="password"
        @blur="v$.form.password.$touch"
        :label="$t('oldPassword')"
      />
      <q-input
        v-model="state.form.newPassword"
        type="password"
        @blur="v$.form.newPassword.$touch"
        :label="$t('newPassword')"
      />
      <q-input
        v-model="state.form.confirmPassword"
        type="password"
        @blur="v$.form.confirmPassword.$touch"
        :label="$t('newPassword')"
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
import { reactive, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { minLength, required, sameAs } from "@vuelidate/validators"

export default {
  name: "PageChangepass",
  data: () => {
    return {
      username: "",
      form: {
        password: "",
        confirmPassword: "",
      },
    }
  },
  setup: () => {
    const state = reactive({
      username: "",
      form: {
        password: "",
        newPassword: "",
        confirmPassword: "",
      },
    })
    const rules = computed(() => {
      return {
        form: {
          password: { required },
          newPassword: {
            required,
            minLength: minLength(4),
          },
          confirmPassword: {
            required,
            sameAs: sameAs(state.form.newPassword),
          },
        },
      }
    })
    const v$ = useVuelidate(rules, state)
    return { state, v$ }
  },
  methods: {
    changePass() {
      if (this.v$.form.newPassword.$error) {
        this.$q.notify({
          message: `${this.$t("newPasswordLength")} 4 ${this.$t("characters")}`,
          position: "top-right",
          avatar: "statics/sad.png",
        })
        return
      }
      if (this.v$.form.confirmPassword.$error) {
        console.log(this.state.form.newPassword)
        console.log(this.state.form.confirmPassword)
        this.$q.notify({
          message: this.$t("newPasswordsMismatch"),
          position: "top-right",
          avatar: "statics/sad.png",
        })
        return
      }

      this.$api
        .put("/api/v1/user/change-pass", {
          password: this.state.form.password,
          new_password: this.state.form.newPassword,
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
