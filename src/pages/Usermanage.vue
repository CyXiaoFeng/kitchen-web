<template>
  <q-page style="margin-top: 10px" padding class="justify-center">
    <div class="row justify-center">
      <q-btn
        @click="newUser"
        color="blue"
        round
        :title="$t('createNewUser')"
        icon="add"
      />
      <q-btn-group push>
        <q-btn
          color="blue"
          @click="filterRole('')"
          glossy
          text-color="black"
          :label="$t('all')"
          icon="done_all"
        />
        <q-btn
          color="blue"
          @click="filterRole('管理员')"
          glossy
          text-color="black"
          :label="$t('admin')"
        />
        <q-btn
          color="blue"
          @click="filterRole('厨师')"
          glossy
          text-color="black"
          :label="$t('chef')"
        />
        <q-btn
          color="blue"
          @click="filterRole('服务员')"
          glossy
          text-color="black"
          :label="$t('waiter')"
        />
      </q-btn-group>
    </div>
    <div class="row justify-center">
      <q-input
        v-model="search_name"
        :debounce="600"
        :placeholder="$t('searchUser')"
        :float-label="$t('searchUser')"
      >
        <template v-slot:prepend>
          <q-icon name="search" />
        </template>
      </q-input>
    </div>
    <div class="row justify-center" style="margin-top: 20px">
      <q-list highlight inset-separator style="width: 300px">
        <q-item v-for="item in user_items" v-bind:key="item.user_id">
          <q-item-section top avatar>
            <q-avatar>
              <img v-if="roleImages[item.role_name]" :src="roleImages[item.role_name]" />
            </q-avatar>
          </q-item-section>
          <q-item-section style="min-width: 120px" :label="item.username">
            <q-item-tile sublabel>{{ item.username }}</q-item-tile>
          </q-item-section>
          <q-item-section right v-if="item.username !== 'admin'">
            <q-btn flat dense icon="more_vert">
              <q-menu>
                <q-list link>
                  <q-item v-close-overlay>
                    <q-item-section
                      :label="$t('role')"
                      @click="assignRole(item.user_id, item.role_id)"
                      >{{ $t("role") }}</q-item-section
                    >
                  </q-item>
                  <q-item v-close-overlay>
                    <q-item-section
                      :label="$t('resetPassword')"
                      @click="passwordReset(item.user_id)"
                      >{{ $t("resetPassword") }}</q-item-section
                    >
                  </q-item>
                  <q-item v-close-overlay>
                    <q-item-section
                      icon="delete"
                      :label="$t('delete')"
                      @click="deleteUser(item.user_id, item.username)"
                      >{{ $t("delete") }}</q-item-section
                    >
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </q-item-section>
        </q-item>
      </q-list>
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
          <span>{{ $t("createNewUser") }}</span>
        </q-card-section>
        <q-card-section>
          <q-field icon="account_circle" :label="$t('username')" :label-width="4">
            <q-input v-model="username" />
          </q-field>
          <q-select
            v-model="role_id"
            :float-label="$t('selectRole')"
            radio
            :options="role_list"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn color="primary" :label="$t('create')" @click="executeNewUser()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style></style>

<script>
import base from "../mixins/base"
export default {
  name: "UserManage",
  mixins: [base],
  data() {
    return {
      search_name: "",
      current_page: 1,
      page_size: 1,
      role_id: "",
      username: "",
      total: 0,
      customDialogModel: false,
      role_list: [],
      user_items: [],
      filter_role_name: "",
      pickRole: "",
      roleImages: {
        服务员: "src/statics/waiter.png",
        厨师: "src/statics/cook.png",
        管理员: "src/statics/admin.png",
      },
    }
  },
  watch: {
    search_name(val) {
      this.loadUsers()
    },
  },
  methods: {
    executeAssignRole(uid, roleId) {
      this.$api
        .put("/api/v1/user/assign-role", {
          user_id: uid,
          role_id: roleId,
        })
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
          } else {
            this.notifyFail(response.data.message)
          }
          this.loadUsers()
        })
        .catch((e) => {
          this.notifyFail(e.response.data)
        })
    },
    assignRole(uid, roleId) {
      this.$q
        .dialog({
          title: this.$t("permissionRole"),
          options: {
            type: "radio",
            model: "",
            items: this.role_list,
          },
          cancel: true,
          preventClose: true,
          color: "secondary",
        })
        .then((data) => {
          console.log(data)
          if (data == null || data.length < 1) {
            this.$q.notify({
              color: "orange",
              textColor: "white",
              icon: "thumb_up",
              message: this.$t("selectARole"),
              position: "top-right",
              avatar: "statics/sad.png",
            })
          } else {
            this.executeAssignRole(uid, data)
          }
        })
        .catch((e) => {
          console.log(e)
        })
    },
    passwordReset(userId) {
      this.$api
        .put("/api/v1/user/password-reset/" + userId)
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
          } else {
            this.notifyFail(response.data.message)
          }
        })
        .catch((e) => {
          this.notifyFail(e.response.data.message)
        })
    },
    deleteUser(userId, username) {
      this.$q
        .dialog({
          title: this.$t("confirm"),
          message: `${this.$t("deleteConfirmation")}:${username}?`,
          ok: this.$t("yes"),
          cancel: this.$t("no"),
        })
        .onOk(() => {
          this.executeDeleteUser(userId)
        })
        .catch(() => {
          // do nothing
        })
    },
    executeDeleteUser(userId) {
      this.$api
        .delete("/api/v1/user/" + userId)
        .then((response) => {
          if (response.data.ok === true) {
            this.notifySuccess(response.data.message)
          } else {
            this.notifyFail(response.data.message)
          }
          this.loadUsers()
        })
        .catch((e) => {
          this.notifyFail(e.response.data.message)
        })
    },
    filterRole(val) {
      this.filter_role_name = val
      this.loadUsers()
    },
    reloadPage(val) {
      this.current_page = val
      this.loadUsers()
    },
    loadUsers() {
      var params = {}
      params.page = this.current_page
      params.filterRoleName = this.filter_role_name
      params.searchName = this.search_name
      this.$api
        .get("/api/v1/user", {
          params: params,
        })
        .then((response) => {
          this.user_items = response.data.data
          this.total = response.data.total
          this.page_size = response.data.pageSize
          this.current_page = response.data.currentPage
        })
        .catch((e) => {
          console.log(e)
        })
    },
    executeNewUser(val) {
      if (
        this.username == null ||
        this.username.length < 1 ||
        this.role_id == null ||
        this.role_id.length < 1
      ) {
        this.$q.notify({
          color: "red",
          textColor: "white",
          icon: "thumb_up",
          message: this.$t("usernameAndRoleRequired"),
          position: "top-right",
          avatar: "statics/sad.png",
        })
        return
      }
      this.$api
        .post("/api/v1/user/new", {
          username: this.username,
          role_id: this.role_id.value,
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
            this.loadUsers()
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
          this.customDialogModel = false
          this.role_id = ""
          this.username = ""
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
    newUser() {
      this.loadRoles()
      this.customDialogModel = true
    },
    loadRoles() {
      this.$api
        .get("/api/v1/role")
        .then((response) => {
          this.role_list = []
          for (var i in response.data) {
            var item = {}
            item.label = response.data[i]["role_name"]
            item.value = response.data[i]["id"]
            this.role_list.push(item)
          }
        })
        .catch((e) => {
          console.info(e)
        })
    },
  },
  mounted() {
    this.loadUsers()
    this.loadRoles()
  },
}
</script>
