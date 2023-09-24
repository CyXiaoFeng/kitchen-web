<template>
  <q-page class="flex flex-center">
    <div style="width: 500px; max-width: 90vw; border: 1px dashed #000">
      <q-btn
        :title="$t('back')"
        :label="$t('back')"
        color="purple-7"
        @click="back"
        style="margin-top: 15px; margin-left: 10px; margin-bottom: 10px"
        icon="keyboard_return"
      />
      <q-btn
        :disabled="order_status === 'finished'"
        :title="$t('addDish')"
        :label="$t('addDish')"
        color="primary"
        @click="addItem"
        style="margin-top: 15px; margin-left: 10px; margin-bottom: 10px"
        icon="add"
      />
      <q-select
        filter
        :readonly="order_status === 'finished'"
        :label="$t('tableNumber')"
        v-model="table_option"
        :options="table_options"
      />
      <q-select
        :readonly="order_status === 'finished'"
        filter
        :label="$t('dish')"
        v-model="dish_option"
        :options="dish_options"
      />
      <!-- <q-input style="width:30px;margin-left: 10px;" v-model="count" type="number" :float-label="$t('quantity')" /> -->
      <div
        style="width: 100px; margin-left: 10px; margin-top: 15px"
        class="row items-center no-wrap"
      >
        <q-btn
          size="sm"
          :disabled="order_status === 'finished'"
          round
          dense
          color="secondary"
          icon="remove"
          @click="changeCount(-1)"
          class="q-mr-xs"
        />
        <q-btn
          size="sm"
          :disabled="order_status === 'finished'"
          round
          dense
          color="secondary"
          icon="add"
          @click="changeCount(1)"
          class="q-mr-sm"
        />
        {{ count }}{{ $t("portion") }}
      </div>
      <q-input style="margin-left: 15px" v-model="description" :label="$t('note')" />
    </div>
  </q-page>
</template>

<style></style>

<script>
import base from "../mixins/base"
export default {
  name: "AddDishItem4Order",
  data() {
    return {
      order_id: "",
      dish_options: [],
      table_option: "",
      dish_option: "",
      created_by: "",
      order_status: "",
      table_options: [],
      description: "",
      count: 1,
    }
  },
  mixins: [base],
  mounted() {
    this.order_id = this.$route.params.id
    this.loadOrderDetail(this.order_id)
    this.loadAllTables()
    this.loadAllDishes()
    this.table_option = this.$store.tableId
  },
  methods: {
    back() {
      this.goPage("/order-detail/" + this.order_id)
    },
    addItem() {
      this.$store.updateTableId(this.table_option)
      console.log(this.table_option)
      // todo check null
      if (
        this.checkStringNull(this.$route.params.id) ||
        this.checkStringNull(this.table_option) ||
        this.checkStringNull(this.dish_option) ||
        this.checkStringNull(this.count)
      ) {
        this.notifyFail(this.$t("pleaseCheckEntries"))
        return
      }
      this.$api
        .post("/api/v1/order-item", {
          order_id: this.$route.params.id,
          table_id: this.table_option.value,
          dish_id: this.dish_option.value,
          dish_count: this.count,
          description: this.description,
        })
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
            this.back()
            this.description = ""
          } else {
            this.notifyFail(response.data.message)
          }
        })
        .catch((e) => {
          this.$q.notify({
            color: "red",
            textColor: "white",
            icon: "thumb_up",
            messag: this.$t("unknownError"),
            position: "top-right",
            avatar: "statics/sad.png",
          })
        })
    },
    changeCount(val) {
      this.count = this.count + val
      if (this.count < 1) {
        this.count = 1
      }
    },
    loadAllDishes() {
      this.$api
        .get("/api/v1/dish/option")
        .then((response) => {
          var dishes = response.data
          this.dish_options = dishes.map((dish) => {
            return {
              label: dish.name,
              icon: "filter_vintage",
              value: dish.id,
            }
          })
        })
        .catch((e) => {
          this.notifyFail(`${$t("unknownError")}oc`)
        })
    },
    loadAllTables() {
      this.$api
        .get("/api/v1/table/all")
        .then((response) => {
          var tables = response.data
          this.table_options = tables.map((table) => {
            return {
              label: table.table_number,
              icon: "filter_vintage",
              value: table.id,
            }
          })
        })
        .catch((e) => {
          this.notifyFail(`${$t("unknownError")}oa`)
        })
    },
    loadOrderDetail(orderId) {
      this.$api
        .get("/api/v1/order/" + orderId)
        .then((response) => {
          var order = response.data
          this.order_no = order.order_number
          this.created_by = order.created_by
          this.order_status = order.order_status
        })
        .catch((e) => {
          this.notifyFail(`${$t("unknownError")}oc`)
        })
    },
  },
}
</script>
