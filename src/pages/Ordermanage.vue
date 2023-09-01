<template>
  <q-page style="margin-top: 10px" padding class="docs-table">
    <div class="row justify-center">
      <h4>进行中订单</h4>
    </div>
    <q-table
      :rows="orders"
      :columns="columns"
      row-key="id"
      color="secondary"
      v-model:pagination="serverPagination"
      @request="request"
      :loading="loading"
    >
      <template v-slot:top-right="props">
        <q-btn
          v-if="props != null"
          title="刷新订单"
          round
          color="blue"
          @click="refreshItems"
          icon="refresh"
        />
      </template>
      <template v-slot:top-left="props">
        <q-btn
          v-if="props != null"
          color="primary"
          @click="newOrder"
          icon-right="playlist_add"
          label="新订单"
        />
      </template>
      <template v-slot:body-cell-OrderNumber="props">
        <q-td :props="props">
          <a href="javascript:" @click.prevent="goPage('/order-detail/' + props.row.id)"
            >{{ props.value }}
          </a>
        </q-td>
      </template>
      <template v-slot:body-cell-Action="props">
        <q-td style="min-width: 150px" :props="props">
          <q-btn
            v-if="props != null"
            color="primary"
            @click="deleteOrderIfNoItems(props.row.id)"
            dense
            icon="delete"
            label="删除订单"
          />
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script>
import base from "../mixins/base"
export default {
  name: "OrderManage",
  data() {
    return {
      table_page_size: 100,
      loading: false,
      orders: [],
      serverPagination: {
        page: 1,
        rowsPerPage: 100,
        rowsNumber: 10, // specifying this determines pagination is server-side
      },
      columns: [
        {
          name: "OrderNumber",
          required: true,
          label: "订单号",
          align: "left",
          field: "order_number",
          sortable: false,
        },
        {
          name: "CreatedBy",
          required: true,
          label: "创建人",
          align: "left",
          field: "created_by",
          sortable: false,
        },
        {
          name: "OrderStatus",
          required: true,
          label: "订单状态",
          align: "left",
          field: "order_status",
          sortable: false,
          format: (val) => (val == "active" ? "进行中" : "完结"),
        },
        {
          name: "StartTime",
          required: true,
          label: "创建时间",
          align: "left",
          field: "start_time",
          sortable: false,
        },
        {
          name: "Action",
          required: true,
          label: "操作",
          align: "left",
          sortable: false,
          format: (val) => (val ? "" : val),
        },
      ],
    }
  },
  mixins: [base],
  mounted() {
    this.loadActiveOrders()
  },
  methods: {
    deleteOrderIfNoItems(orderId) {
      this.$q
        .dialog({
          title: "确认删除订单",
          ok: "是",
          cancel: "否",
        })
        .onOk(() => {
          this.$api
            .delete("/api/v1/order/active/" + orderId)
            .then((response) => {
              if (response.data.ok === true) {
                this.notifySuccess(response.data.message)
              } else {
                this.notifyFail(response.data.message)
              }
              this.loadActiveOrders()
            })
            .catch((e) => {
              this.notifyFail(e.response.data.message)
            })
        })
    },
    refreshItems() {
      this.loadActiveOrders(this.table_page_size)
    },
    request(props) {
      this.serverPagination = props.pagination
      this.loadActiveOrders(this.table_page_size)
    },
    loadActiveOrders() {
      var params = {}
      params.page = this.serverPagination.page
      params.pageSize = this.serverPagination.rowsPerPage
      this.loading = true
      this.$api
        .get("/api/v1/order/active", {
          params: params,
        })
        .then((response) => {
          this.orders = response.data.data
          this.serverPagination.page = response.data.currentPage
          this.serverPagination.rowsNumber = response.data.total
          this.serverPagination.rowsPerPage = response.data.pageSize
          this.loading = false
        })
        .catch((e) => {
          this.notifyFail(e.response.data.message)
        })
    },
    newOrder() {
      this.$api
        .post("/api/v1/order/new")
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
            this.goPage("/order-detail/" + response.data.data)
          }
        })
        .catch((e) => {
          console.log(e)
        })
    },
  },
}
</script>
