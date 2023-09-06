<template>
  <q-page style="margin-top: 10px" class="row justify-center">
    <div style="max-width: 90vw">
      <div class="row justify-center">
        <h4>菜品管理</h4>
      </div>
      <div class="row justify-center">
        <q-btn
          @click="newDish"
          color="blue"
          label="录入菜品"
          title="录入菜品"
          icon="playlist_add"
        />
      </div>
      <div class="row justify-center">
        <q-select
          use-input
          filled
          use-chips
          multiple
          @update:modelValue="selectChange"
          color="purple"
          label="按标签过滤"
          v-model="multi_select_tags"
          :options="dish_tags"
        />
      </div>
      <div class="q-pa-md row items-start q-gutter-md">
        <q-card
          class="my-card"
          flat
          bordered
          style="max-width: 200px"
          v-for="dish in dishes"
          v-bind:key="dish.id"
          inline
        >
          <q-card-section>
            <img
              :src="dish.thumbnail === null ? 'src/statics/dish.png' : dish.thumbnail"
              style="cursor: pointer"
              @click="goPage('/edit-dish/' + dish.id)"
            />
          </q-card-section>
          <div>
            <a href="javascript:" @click.prevent="goPage('/edit-dish/' + dish.id)"
              >{{ dish.name }}({{ dish.price }}元)</a
            >
          </div>
          <q-card-section>
            {{ dish.description }}
          </q-card-section>
          <q-separator />
          <q-card-section v-if="!checkStringNull(dish.tags)">
            <q-chip
              v-for="tag in dish.tags.split(',')"
              v-bind:key="tag"
              small
              color="cyan-6"
              >{{ tag }}</q-chip
            >
          </q-card-section>
          <q-separator />
          <q-card-actions>
            <q-btn @click="deleteDish(dish.id)" flat color="primary">删除</q-btn>
          </q-card-actions>
        </q-card>
      </div>
      <div class="row justify-center" style="margin-top: 5px">
        <q-pagination
          v-if="total > 0"
          @input="reloadPage"
          v-model="current_page"
          color="blue"
          :min="1"
          :max="Math.floor(total / page_size) + 1"
          boundary-links
        />
      </div>
    </div>
  </q-page>
</template>
<script>
import base from "../mixins/base.js"
export default {
  name: "DishManage",
  mixins: [base],
  data() {
    return {
      dishes: [],
      dish_tags: [],
      multi_select_tags: [],
      current_page: 1,
      total: 0,
      page_size: 1,
    }
  },
  mounted() {
    this.loadDish()
    this.loadDishTags()
  },
  methods: {
    deleteDish(id) {
      this.$q
        .dialog({
          title: "删除确认",
          ok: "是",
          cancel: "否",
        })
        .onOk(() => {
          this.$api
            .delete("/api/v1/dish/" + id)
            .then((response) => {
              if (response.data.ok === true) {
                this.notifySuccess(response.data.message)
              } else {
                this.notifyFail(response.data.message)
              }
              this.loadDish()
            })
            .catch((e) => {
              console.log(e.response.data.message)
              this.notifyFail(e.response.data.message)
            })
        })
    },
    selectChange(tags) {
      const curTags = tags
        .map((tag) => {
          return tag.value
        })
        .join(",")
      this.loadDish(curTags)
    },
    loadDishTags() {
      this.$api
        .get("/api/v1/dish/tag-all")
        .then((response) => {
          var tags = response.data
          this.dish_tags = tags.map((tag) => {
            return {
              label: tag.name,
              icon: "filter_vintage",
              value: tag.name,
            }
          })
        })
        .catch((e) => {
          console.log(e)
        })
    },
    reloadPage(val) {
      this.current_page = val
      this.loadDish("")
    },
    loadDish(tags) {
      var params = {}
      params.page = this.current_page
      params.tags = tags
      this.$api
        .get("/api/v1/dish", {
          params: params,
        })
        .then((response) => {
          this.dishes = response.data.data
          this.current_page = response.data.currentPage
          this.total = response.data.total
          this.page_size = response.data.pageSize
        })
        .catch((e) => {
          console.log(e)
        })
    },
    newDish() {
      this.goPage("/new-dish")
    },
  },
}
</script>
