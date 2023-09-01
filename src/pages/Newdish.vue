<template>
  <q-page style="margin-top: 10px" class="row justify-center">
    <div style="width: 400px; max-width: 90vw">
      <h4>新建菜品</h4>
      <q-field icon="short_text">
        <q-input v-model="dish_name" placeholder="菜名" />
      </q-field>
      <q-field icon="description">
        <template v-slot:prepend>
          <q-icon name="description" />
        </template>
        <q-input v-model="description" placeholder="菜品描述" />
      </q-field>
      <q-field>
        <template v-slot:prepend>
          <q-icon name="tag_faces" />
        </template>
        <q-select
          label="添加菜品标签"
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
      <q-field label="平均制作工时(分钟)" :label-width="5">
        <template v-slot:prepend>
          <q-icon name="timer" />
        </template>
        <q-input type="number" max-length="16" v-model="expected_cooking_time" />
      </q-field>
      <q-field label="价格" label-width="5">
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
          label="返回菜品列表"
        />
        <q-btn
          @click="createDish"
          icon="add"
          color="blue"
          style="margin-left: 10px"
          label="创建菜品"
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
        this.notifyWarn("菜名不得为空")
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
              message: response.data.message,
              position: "top-right",
              avatar: "statics/huaji.png",
            })
            this.goPage("/dish-manage")
          } else {
            this.$q.notify({
              color: "red",
              textColor: "white",
              icon: "thumb_up",
              message: response.data.message,
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
            message: "未知错误",
            position: "top-right",
            avatar: "statics/sad.png",
          })
        })
    },
    selected(item) {
      console.log(item.label)
    },
    duplicate(label) {
      this.$q.notify(`"${label}" 重复标签`)
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
