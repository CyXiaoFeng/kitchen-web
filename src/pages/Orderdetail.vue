<template>
  <q-page style="margin-top: 10px" class="row justify-center">
    <div style="max-width: 90vw; margin-top: 10px">
      <p class="caption">{{ $t("orderNumber") }}：{{ order_no }}</p>
      <p class="caption">{{ $t("creator") }}: {{ created_by }}</p>
      <div class="row justify-center" style="margin-top: 10px">
        <q-table
          style="max-width: 90vw"
          :rows="order_items"
          :columns="columns"
          row-key="id"
          color="secondary"
          :loading="loading"
        >
          <template v-slot:top-right="props">
            <span v-if="props != null" style="margin-left: 10px"
              ><q-chip color="blue-grey-6"
                >{{ $t("totalPrice") }}:{{ totalPrice }}</q-chip
              ></span
            >
          </template>
          <template v-slot:top-left="props">
            <div class="q-pa-md q-gutter-sm">
              <q-btn
                v-if="props != null && order_status !== 'finished'"
                :title="$t('backToOngoingOrders')"
                color="purple-7"
                icon="keyboard_return"
                :label="$t('back')"
                @click="goPage('/order-manage')"
              />
              <q-btn
                v-if="props != null && order_status === 'finished'"
                :title="$t('backToHistoricalOrders')"
                color="purple-7"
                icon="keyboard_return"
                :label="$t('back')"
                @click="goPage('/report-manage')"
              />
              <q-btn
                :disabled="order_status === 'finished'"
                v-if="props != null"
                :title="$t('assignDishToKitchenStation')"
                color="teal-6"
                :label="$t('assignToKitchenStation')"
                @click="assignItems"
                icon="assignment_returned"
              />
              <q-btn
                v-if="props != null && order_status !== 'finished'"
                :title="`${$t('endOrder')}(${$t('paid')})`"
                color="positive"
                :label="$t('endOrder')"
                @click="finishOrder"
                icon="done_all"
              />
              <q-btn
                style="margin-left: 10px"
                v-if="props != null && order_status !== 'finished'"
                :title="$t('addDish')"
                color="blue"
                :label="$t('addDish')"
                @click="toAddDishPage"
                icon="add"
              />
              <q-chip
                color="blue-grey-13"
                v-if="props != null && order_status === 'finished'"
                style="margin-left: 10px"
                >{{ $t("completed") }}</q-chip
              >
              <q-btn
                v-if="props != null"
                style="margin-left: 10px"
                :title="$t('refreshList')"
                round
                color="blue"
                @click="refreshItems"
                icon="refresh"
              />
            </div>
          </template>
          <template v-slot:body-cell-Status="props">
            <q-td style="min-width: 115px" :props="props">
              <q-chip v-if="props.value === 'unassigned'" small color="brown-4">{{
                $t("unassigned")
              }}</q-chip>
              <q-chip v-else-if="props.value === 'waiting_assign'" small color="yellow">{{
                $t("pendingAssignment")
              }}</q-chip>
              <q-chip v-else-if="props.value === 'failed_assign'" small color="red">{{
                $t("assignmentFailed")
              }}</q-chip>
              <q-chip v-else-if="props.value === 'assigned'" small color="lime-14">{{
                $t("inProgress")
              }}</q-chip>
              <q-chip
                v-else-if="props.value === 'readytoserve'"
                small
                color="deep-orange-6"
                >{{ $t("readyForPickup") }}</q-chip
              >
              <q-chip v-else-if="props.value === 'served'" small color="green">{{
                $t("served")
              }}</q-chip>
              <q-chip v-else small color="green">props.value</q-chip>
            </q-td>
          </template>
          <template v-slot:body-cell-DishCount="props">
            <q-td style="min-width: 150px" :props="props">
              <q-btn
                :disable="props.row.status !== 'unassigned'"
                size="sm"
                round
                dense
                color="secondary"
                icon="remove"
                @click="updateUnassignedItemCount(props.row.id, props.value - 1)"
                class="q-mr-xs"
              />
              <q-btn
                :disable="props.row.status !== 'unassigned'"
                size="sm"
                round
                dense
                color="secondary"
                icon="add"
                @click="updateUnassignedItemCount(props.row.id, props.value + 1)"
                class="q-mr-sm"
              />
              {{ props.value }}
            </q-td>
          </template>
          <template v-slot:body-cell-Price="props">
            <q-td style="max-width: 120px" key="Price" :props="props">
              <q-chip>{{ props.value }}￥</q-chip>
            </q-td>
          </template>
          <template v-slot:body-cell-Description="props">
            <q-td style="max-width: 300px" :props="props">
              <q-btn
                v-if="props.row.status !== 'served'"
                @click="openEditDescriptionDialog(props.row.id, props.value)"
                size="sm"
                class="q-mr-sm"
                icon="mode_edit"
                dense
              />{{ props.value }}
            </q-td>
          </template>
          <template v-slot:body-cell-Action="props">
            <q-td style="max-width: 150px" :props="props">
              <q-btn
                v-if="props.row.status === 'readytoserve'"
                @click="served(props.row.id)"
                icon="speaker_notes_off"
                dense
                glossy
                color="purple-13"
                :label="$t('markAsCooked')"
              />
            </q-td>
          </template>
          <template v-slot:body-cell-TableNumber="props">
            <q-td style="width: 100px; max-width: 200px" :props="props">
              <a
                @click.prevent="goPage('/order-detail-by-table/' + props.row.table_id)"
                href="javascript:"
                >{{ props.value }}</a
              >
            </q-td>
          </template>
        </q-table>
      </div>
    </div>
  </q-page>
</template>

<style>
.q-table td,
.q-table th {
  /* don't shorten cell contents */
  white-space: normal !important;
}
</style>

<script>
import base from "../mixins/base"
export default {
  name: "OrderDetail",
  interval: null,
  data() {
    return {
      loading: false,
      columns: [
        {
          name: "DishName",
          required: true,
          label: this.$t("dishName"),
          align: "left",
          field: "dish_name",
          sortable: false,
        },
        {
          name: "Status",
          required: true,
          label: this.$t("status"),
          align: "left",
          field: "status",
          sortable: false,
        },
        {
          name: "TableNumber",
          required: true,
          label: this.$t("tableNumber"),
          align: "left",
          field: "table_number",
          sortable: false,
        },
        {
          name: "Description",
          required: false,
          label: this.$t("note"),
          align: "left",
          field: "description",
          sortable: false,
        },
        {
          name: "DishCount",
          required: true,
          label: this.$t("quantity"),
          align: "left",
          field: "dish_count",
          sortable: false,
        },
        {
          name: "Price",
          required: true,
          label: this.$t("unitPrice"),
          align: "left",
          field: "price",
          sortable: false,
        },
        {
          name: "ProducerNumber",
          required: true,
          label: this.$t("assignKitchenStation"),
          align: "left",
          field: "producer_number",
          sortable: false,
        },
        {
          name: "Action",
          required: true,
          label: this.$t("operation"),
          align: "left",
          sortable: false,
        },
        {
          name: "LastUpdateTime",
          required: true,
          label: this.$t("updateTime"),
          align: "left",
          field: "last_update_time",
          sortable: false,
        },
      ],
      total: 0,
      order_status: "",
      page_size: 1,
      description: "",
      table_page_size: 100,
      order_id: "",
      order_no: "",
      created_by: "",
      order_items: [],
    }
  },
  mixins: [base],
  computed: {
    totalPrice: function () {
      var tPrice = 0.0

      console.log(this.order_items)
      for (var i in this.order_items) {
        console.log(this.order_items[i].price)
        tPrice = tPrice + this.order_items[i].price * this.order_items[i].dish_count
      }
      return tPrice
    },
  },

  mounted() {
    this.order_id = this.$route.params.id
    this.loadOrderDetail(this.order_id)
    this.loadOrderItemsByOrderId(this.order_id, this.table_page_size)
    this.interval = setInterval(() => {
      this.refreshItems()
      console.log("refresh order detail items list")
    }, 20000)
  },
  unmounted() {
    console.log("clear refresh items list")
    clearInterval(this.interval)
  },
  methods: {
    toAddDishPage() {
      this.goPage("/add-dish-item-4-order/" + this.order_id)
    },
    served(itemId) {
      this.$api
        .put("/api/v1/order-item/served/" + itemId)
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
          } else {
            this.notifyFail(response.data.message)
          }
          this.refreshItems()
        })
        .catch((e) => {
          this.notifyFail(this.$t("unknownError"))
        })
    },
    finishOrder() {
      this.$api
        .put("/api/v1/order/finish/" + this.order_id)
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
          } else {
            this.notifyFail(response.data.message)
          }
          this.loadOrderDetail(this.order_id)
        })
        .catch((e) => {
          this.notifyFail(e.response.data.message)
        })
    },
    openEditDescriptionDialog(itemId, value) {
      this.$q
        .dialog({
          title: this.$t("modifyNote"),
          prompt: {
            model: value,
            type: "text", // optional
          },
          cancel: true,
          color: "secondary",
        })
        .onOk((data) => {
          this.updateItemDescription(itemId, data)
        })
        .catch(() => {
          //   this.$q.notify('Ok, no mood for talking, right?')
        })
    },
    updateItemDescription(itemId, newDescription) {
      this.$api
        .put("/api/v1/order-item/description", {
          item_id: itemId,
          description: newDescription,
        })
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
            this.refreshItems()
          } else {
            this.notifyFail(response.data.message)
          }
        })
        .catch((e) => {
          this.notifyFail(this.$t("unknownError"))
        })
    },
    updateUnassignedItemCount(itemId, count) {
      if (count < 0) {
        count = 0
      }
      this.$api
        .put("/api/v1/order-item/unassigned-count", {
          item_id: itemId,
          count: count,
        })
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
            this.refreshItems()
          } else {
            this.notifyFail(response.data.message)
          }
        })
        .catch((e) => {
          this.notifyFail(this.$t("unknownError"))
        })
    },
    assignItems() {
      this.$api
        .post("/api/v1/assignment/" + this.order_id)
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
            //TODO 旧代码采用setInterval定时刷新，用于更新不断变化的状态
            this.refreshItems()
          } else {
            this.notifyFail(response.data.message)
          }
        })
        .catch((e) => {
          this.notifyFail(this.$t("unknownError"))
        })
    },
    refreshItems() {
      this.loadOrderItemsByOrderId(this.order_id, this.table_page_size)
    },
    request(props) {
      console.log(props)
      this.serverPagination = props.pagination
      this.loadOrderItemsByOrderId(this.order_id, this.table_page_size)
    },
    reloadPage(val) {
      this.serverPagination.page = val
      this.loadOrderItemsByOrderId(this.order_id, this.table_page_size)
    },
    loadOrderItemsByOrderId(orderId, pageSize) {
      this.loading = true
      var params = {}
      params.orderId = orderId
      this.$api
        .get("/api/v1/order-item", {
          params: params,
        })
        .then((response) => {
          this.order_items = response.data
          this.loading = false
        })
        .catch((e) => {
          console.log("===failed loading order items")
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
          this.notifyFail(this.$t("unknownError"))
        })
    },
  },
}
</script>
