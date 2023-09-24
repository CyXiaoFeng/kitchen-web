<template>
  <q-page style="margin-top: 10px" class="row justify-center">
    <div style="max-width: 90vw; margin-top: 10px">
      <div class="row justify-center">
        <h4>{{ $t("tableNumber") }}:{{ table_no }} {{ $t("historicalOrdersOf") }}</h4>
      </div>
      <div class="row justify-center">
        <q-table
          style="max-width: 90vw"
          :rows="orders"
          :columns="columns"
          row-key="id"
          color="secondary"
          v-model:pagination="serverPagination"
          @request="request"
          :loading="loading"
        >
          <!-- <template slot="top-right">
          <q-btn :title="$t('refreshList')" round color="secondary" @click="refreshItems" style="margin-top:15px;margin-left:10px;" icon="refresh" />
        </template> -->
          <template v-slot:top-left="props">
            <q-btn
              v-if="props != null"
              :label="$t('back')"
              color="purple-7"
              icon="keyboard_backspace"
              @click="goPage('/report-by-table')"
            />
          </template>
          <template v-slot:top-right="props">
            <q-btn
              v-if="props != null"
              :title="$t('refreshList')"
              round
              color="blue"
              @click="refreshItems"
              icon="refresh"
            />
          </template>
          <template v-slot:body-cell-OrderStatus="props">
            <q-td>
              <q-chip v-if="props.value === 'active'" small color="brown-4">{{
                $t("ongoing")
              }}</q-chip>
              <q-chip v-else-if="props.value === 'finished'" small color="green">{{
                $t("completed")
              }}</q-chip>
              <q-chip v-else small color="amber">{{ props.value }}</q-chip>
            </q-td>
          </template>
          <template v-slot:body-cell-OrderNumber="props">
            <q-td>
              <a
                href="javascript:"
                @click.prevent="goPage('/order-detail/' + props.row.id)"
                >{{ props.value }}</a
              >
            </q-td>
          </template>
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
              color="tertiary"
              icon="add"
              @click="updateUnassignedItemCount(props.row.id, props.value + 1)"
              class="q-mr-sm"
            />
            {{ props.value }}
          </q-td>
          <template v-slot:body-cell-Description="props">
            <q-td>
              style="max-width: 300px" >
              <span>{{ props.value }}</span>
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
  name: "HistoryorderdetailByTable",
  data() {
    return {
      table_no: "",
      tableId: "",
      serverPagination: {
        page: 1,
        rowsPerPage: 100,
        rowsNumber: 10, // specifying this determines pagination is server-side
      },
      loading: false,
      columns: [
        {
          name: "OrderNumber",
          required: true,
          label: this.$t("orderNumber"),
          align: "left",
          field: "order_number",
          sortable: false,
        },
        {
          name: "CreatedBy",
          required: true,
          label: this.$t("creator"),
          align: "left",
          field: "created_by",
          sortable: false,
        },
        {
          name: "OrderStatus",
          required: true,
          label: this.$t("orderStatus"),
          align: "left",
          field: "order_status",
          sortable: false,
        },
        {
          name: "StartTime",
          required: true,
          label: this.$t("creationTime"),
          align: "left",
          field: "start_time",
          sortable: false,
        },
        {
          name: "EndTime",
          required: true,
          label: this.$t("completionTime"),
          align: "left",
          field: "end_time",
          sortable: false,
        },
      ],
      total: 0,
      page_size: 1,
      description: "",
      count: 1,
      table_page_size: 100,
      order_no: "",
      table_options: [],
      table_option: "",
      dish_options: [],
      dish_option: "",
      created_by: "",
      order_items: [],
      orders: [],
    }
  },
  mixins: [base],
  mounted() {
    this.table_id = this.$route.params.id
    this.loadHistoryOrderByTable()
    this.loadTableInfo()
  },
  methods: {
    loadHistoryOrderByTable() {
      var params = {}
      params.page = this.serverPagination.page
      params.pageSize = this.serverPagination.rowsPerPage
      this.$api
        .get("/api/v1/order/history-by-table/" + this.table_id, {
          params: params,
        })
        .then((response) => {
          this.orders = response.data.data
          this.serverPagination.page = response.data.currentPage
          this.serverPagination.rowsNumber = response.data.total
          this.serverPagination.rowsPerPage = response.data.pageSize
        })
        .catch((e) => {
          this.notifyFail(e.response.data.message)
        })
    },
    refreshItems() {
      this.loadHistoryOrderByTable()
    },
    request(props) {
      this.serverPagination = props.pagination
      this.loadHistoryOrderByTable()
    },
    loadTableInfo() {
      this.$api
        .get("/api/v1/table/" + this.table_id)
        .then((response) => {
          this.table_no = response.data.table_number
        })
        .catch((e) => {
          this.notifyFail(this.$t("failedToLoadTableInfo"))
        })
    },
  },
}
</script>
