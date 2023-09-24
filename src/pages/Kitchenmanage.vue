<template>
  <q-page style="margin-top: 10px" class="row justify-center">
    <div style="width: 700px; max-width: 90vw">
      <div class="row justify-center">
        <h4>{{ $t("kitchenManagement") }}</h4>
      </div>
      <div class="row justify-center">
        <q-btn
          @click="newPosition"
          color="blue"
          :title="$t('createNewKitchenStation')"
          :label="$t('createNewKitchenStation')"
          icon="playlist_add"
        />
      </div>
      <div class="row justify-center">
        <q-card
          v-bind:class="{
            'offline-card': position.status === 'offline',
            'online-card': position.status === 'online',
            'blocking-card': position.status === 'blocking',
          }"
          v-for="position in positions"
          v-bind:key="position.id"
          inline
          class="q-ma-sm"
        >
          <q-card>
            <img src="src/statics/chuwei.png" />
            <q-card-section>
              {{ position.producer_number }}
              <span>{{ position.description }}</span>
            </q-card-section>
          </q-card>
          <q-card-actions>
            <q-btn @click="deletePosition(position.id)" flat>{{ $t("delete") }}</q-btn>
            <q-btn @click="editPosition(position.id)" flat>{{ $t("edit") }}</q-btn>
          </q-card-actions>
          <q-item>
            <q-item-section>
              <q-btn-toggle
                @update:modelValue="
                  (val) => {
                    toggleStatus(val, position.id)
                  }
                "
                v-model="position.status"
                push
                glossy
                toggle-color="primary"
                :options="[
                  { label: $t('online'), value: 'online' },
                  { label: $t('blocked'), value: 'blocking' },
                  { label: $t('offline'), value: 'offline' },
                ]"
              />
            </q-item-section>
          </q-item>
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
    <q-dialog
      v-model="customDialogModel"
      @ok="onOk"
      @cancel="onCancel"
      @show="onShow"
      @hide="onHide"
    >
      <!-- 这里可能使用<q-dialog>的"title"属性 -->
      <q-card style="width: 700px; max-width: 80vw">
        <q-card-section>
          <div class="text-h6">{{ $t("createNewKitchenStation") }}</div>
        </q-card-section>
        <q-card-section>
          <div>
            <q-field
              icon="settings_input_composite"
              :label="`${$t('kitchenStationNumber')}(${$t('required')})`"
              :label-width="5"
            >
              <q-input v-model="k_position_no" />
            </q-field>
            <q-field icon="description" :label="$t('description')" :label-width="4">
              <q-input v-model="k_description" />
            </q-field>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            color="primary"
            :label="$t('create')"
            @click="executeNewPosition()"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="editDishProducerDialog"
      @ok="onOk"
      @cancel="onCancel"
      @show="onShow"
      @hide="onHide"
    >
      <!-- 这里可能使用<q-dialog>的"title"属性 -->
      <span>{{ $t("editKitchenStation") }}</span>
      <div>
        <q-field
          icon="settings_input_composite"
          :label="`${$t('tableNumber')}}(${$t('required')}})`"
          :label-width="5"
        >
          <q-input v-model="k_dish_producer_no" />
        </q-field>
        <q-field icon="description" :label="$t('description')" :label-width="4">
          <q-input v-model="k_dish_producer_description" />
        </q-field>
      </div>
      <q-card-actions>
        <q-btn color="primary" :label="$t('update')" @click="executeEditDishProducer()" />
      </q-card-actions>
    </q-dialog>
  </q-page>
</template>

<style>
.offline-card {
  background-color: #e0e0e0;
  opacity: 0.8;
}
.online-card {
  background-color: #d3ff93;
}
.blocking-card {
  background-color: #ffed97;
}
</style>

<script>
import base from "../mixins/base"
export default {
  name: "KitchenManage",
  data() {
    return {
      k_dish_producer_no: "",
      k_dish_producer_description: "",
      k_dish_producer_id: "",
      editDishProducerDialog: false,
      selected: {},
      current_page: 1,
      k_description: "",
      k_position_no: "",
      customDialogModel: false,
      positions: [],
      total: 0,
      page_size: 1,
    }
  },
  mixins: [base],
  mounted() {
    this.loadKPositions()
  },
  methods: {
    toggleStatus(status, id) {
      this.$api
        .put("/api/v1/dish-producer/status/" + id, {
          status: status,
        })
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
          } else {
            this.notifyFail(response.data.message)
          }
          this.loadKPositions()
        })
        .catch((e) => {
          this.notifyFail(e.response.data.message)
        })
    },
    reloadPage(val) {
      this.current_page = val
      this.loadKPositions()
    },
    executeEditDishProducer() {
      if (this.checkStringNull(this.k_dish_producer_no)) {
        this.notifyWarn(this.$t("kitchenStationNumberRequired"))
        return
      }
      this.$api
        .put("/api/v1/dish-producer/" + this.k_dish_producer_id, {
          producer_number: this.k_dish_producer_no,
          description: this.k_dish_producer_description,
        })
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
          } else {
            this.notifyFail(response.data.message)
          }
          this.loadKPositions()
          this.editDishProducerDialog = false
        })
        .catch((e) => {
          this.notifyFail(e.response.data.message)
        })
    },
    editPosition(id) {
      this.$api
        .get("/api/v1/dish-producer/" + id)
        .then((response) => {
          this.k_dish_producer_no = response.data.producer_number
          this.k_dish_producer_description = response.data.description
          this.k_dish_producer_id = response.data.id
        })
        .catch((e) => {
          this.notifyFail(e.response.data.message)
        })
      this.editDishProducerDialog = true
    },
    deletePosition(id) {
      this.$q
        .dialog({
          title: this.$t("deleteConfirmation"),
          ok: this.$t("yes"),
          cancel: this.$t("no"),
        })
        .onOk(() => {
          this.$api
            .delete("/api/v1/dish-producer/" + id)
            .then((response) => {
              if (response.data.ok === true) {
                this.notifySuccess(response.data.message)
              } else {
                this.notifyFail(response.data.message)
              }
              this.loadKPositions()
            })
            .catch((e) => {
              this.notifyFail(e.response.data.message)
            })
        })
        .catch((e) => {
          console.log(e)
        })
    },
    loadKPositions() {
      var params = {}
      params.page = this.current_page
      this.$api
        .get("/api/v1/dish-producer", {
          params: params,
        })
        .then((response) => {
          this.positions = response.data.data
          this.current_page = response.data.currentPage
          this.page_size = response.data.pageSize
          this.total = response.data.total
        })
        .catch((e) => {
          console.log(e)
        })
    },
    onOk() {
      console.log("ok")
    },
    onCancel() {
      console.log("cancel")
    },
    onShow() {
      console.log("show")
    },
    onHide() {
      console.log("hide")
    },
    executeNewPosition() {
      this.$api
        .post("/api/v1/dish-producer", {
          producer_number: this.k_position_no,
          description: this.k_description,
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
            this.customDialogModel = false
            this.loadKPositions()
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
            message: this.$t("unknownError"),
            position: "top-right",
            avatar: "statics/sad.png",
          })
        })
    },
    newPosition() {
      this.customDialogModel = true
    },
  },
}
</script>
