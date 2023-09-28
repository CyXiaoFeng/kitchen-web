<template>
  <q-page style="margin-top: 10px" class="row justify-center">
    <div style="width: 400px; max-width: 90vw">
      <h4>{{ $t("createDish") }}</h4>
      <q-field icon="short_text">
        <q-input v-model="dish_name" :placeholder="$t('dishName')" />
      </q-field>
      <q-field icon="description">
        <template v-slot:prepend>
          <q-icon name="description" />
        </template>
        <q-input v-model="description" :placeholder="$t('dishDescription')" />
      </q-field>
      <q-field>
        <template v-slot:prepend>
          <q-icon name="tag_faces" />
        </template>
        <q-select
          :label="$t('addDishTag')"
          filled
          v-model="dish_tags"
          use-input
          use-chips
          multiple
          hide-dropdown-icon
          input-debounce="0"
          new-value-mode="add-unique"
        />
        <q-autocomplete :min-characters="1" @search="search" @selected="selected" />
      </q-field>
      <q-field :label="$t('averagePreparationTime') + $t('minutes')" :label-width="5">
        <template v-slot:prepend>
          <q-icon name="timer" />
        </template>
        <q-input type="number" max-length="16" v-model="expected_cooking_time" />
      </q-field>
      <q-field :label="$t('price')" label-width="5">
        <template v-slot:prepend>
          <q-icon name="price_check" />
        </template>
        <q-input type="number" max-length="16" v-model="price" />
      </q-field>
      <q-field>
        <q-btn
          @click="goPage('/dish-manage')"
          icon="keyboard return"
          color="purple-7"
          :label="$t('backToDishList')"
        />
        <q-btn
          @click="createDish"
          icon="add"
          color="blue"
          style="margin-left: 10px"
          :label="$t('createDish')"
        />
      </q-field>
    </div>
  </q-page>
</template>

<style></style>

<script>
import base from "../mixins/base"
export default {
  name: "NewDish",
  data() {
    return {
      expected_cooking_time: 20,
      dish_name: "",
      dish_tags: [],
      description: "",
      price: 1.0,
    }
  },
  mixins: [base],
  methods: {
    createDish() {
      if (this.checkStringNull(this.dish_name)) {
        this.notifyWarn(this.getResponseMsg("dishNameRequired"))
        return
      }
      this.$api
        .post("/api/v1/dish/", {
          name: this.dish_name,
          description: this.description,
          tags: this.dish_tags.join(","),
          expected_cooking_time: this.expected_cooking_time,
          price: this.price,
        })
        .then((response) => {
          if (response.data.ok === true) {
            this.$q.notify({
              color: "green",
              textColor: "white",
              icon: "thumb_up",
              message: this.resMsg(response.data.message),
              position: "top-right",
              avatar: "statics/huaji.png",
            })
            this.goPage("/dish-manage")
          } else {
            this.$q.notify({
              color: "red",
              textColor: "white",
              icon: "thumb_up",
              message: this.resMsg(response.data.message),
              position: "top-right",
              avatar: "statics/sad.png",
            })
          }
        })
        .catch((e) => {
          this.$q.notify({
            color: "red",
            textColor: "white",
            icon: "thumb_up",
            message: this.$t("unknownError"),
            position: "top-right",
            avatar: "statics/sad.png",
          })
        })
    },
    selected(item) {
      console.log(item.label)
    },
    duplicate(label) {
      this.$q.notify(`"${label}" "this.$t('duplicateTag')"`)
    },
    search(terms, done) {
      var searchParams = {}
      searchParams.search_field = terms
      this.$api
        .get("/api/v1/dish/tag", {
          params: searchParams,
        })
        .then((response) => {
          let tags = response.data
          var results = tags.map((tag) => {
            return {
              label: tag.name,
              icon: "filter_vintage",
              value: tag.name,
            }
          })
          // Call done and pass the result set
          done(results)
        })
    },
  },
}
</script>
